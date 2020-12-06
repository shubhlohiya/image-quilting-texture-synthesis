import numpy as np 
from minErrorBoundaryCut import *

def create_blocks(source_img, row_s, col_s, block_size):
    blocks = []
    #creating blocks of specified size from given texture image
    for i in range(row_s-block_size[0]):
        for j in range(col_s-block_size[1]):
            blocks.append(source_img[i:i+block_size[0],j:j+block_size[1],:])                              
    blocks = np.array(blocks)
    return blocks

def SSDerror(Block, final_crop, target_crop, alpha):
    #updating the SSDerror function used in image quilting for texture synthesis for texture transfer 
    #The error term in image quilting is modified by weighted a weighted sum,ɑ times the block overlap matching error
    #plus (1-ɑ) times squared error between the correspondence map pixels within the source texture block and those at current target image position.
    [m,n,p] = final_crop.shape
    Block = Block[0:m,0:n,0:p]
    #correspondance map in our case in the luminance of intensities
    #taking mean intenisty for each pixel for all the channels
    GrayBlock = np.mean(Block, axis = 2)
    Graytarget_crop = np.mean(target_crop, axis = 2)
    Grayfinal_crop = np.mean(final_crop, axis = 2)

    #block overlap matching error
    e1 = np.sqrt(np.sum(((final_crop)>-1)*(Block - final_crop)**2))
    #the second term as mentioned above
    e2 = np.sqrt(np.sum((Grayfinal_crop>-1)*(GrayBlock - Graytarget_crop)**2))
    #weighted sum
    error = alpha*e1 + (1-alpha)*e2

    return error

def best_block(blocks, final_crop, target_crop, block_size, alpha, tolerance):
    #same function as used in texture synthesis 
    #only change in aruments of error function
    h, w, c = final_crop.shape
    errors = [(SSDerror(block[0:h, 0:w, 0:c], final_crop, target_crop, alpha)) for block in blocks]
    min_error = np.min(errors)
    matches = [block[0:h, 0:w, 0:c] for i, block in enumerate(blocks)
               if errors[i]<=(1+tolerance)*min_error]
    return matches[np.random.randint(len(matches))]


def texturize(source_img, target_crop_img, block_size, overlap, alpha, tolerance):

	#this function takes a source image, target image, block size, tolerance, overlap and alpha as its arguments and calculates an
	#texture transferd image

	#this function is similar to the one used for synthesis
    #converting images to arrays
    source_img = np.asarray(source_img)
    target_crop_img = np.asarray(target_crop_img)

    if len(source_img.shape) == 3:
        [row_s, col_s, ch_s] = source_img.shape
    else:
        [row_s, col_s] = source_img.shape

    if len(target_crop_img.shape) == 3:
        [row_t, col_t, ch_t] = target_crop_img.shape
    else:
        [row_t, col_t] = target_crop_img.shape

    #creating blocks from the given source image with given block size
    blocks = create_blocks(source_img, row_s, col_s, block_size)    

    #initializing the final image with -1s and dimensions same as that of target image
    final_img = -np.ones([row_t, col_t, ch_t])
    
    #calculating the number of blocks which can fir in a row and column of final image
    nRowBlocks = int(np.ceil((row_t - block_size[0]) / (block_size[0] - overlap)) + 1)
    nColBlocks = int(np.ceil((col_t - block_size[1]) / (block_size[1] - overlap)) + 1)

    for i in range(nRowBlocks):
        for j in range(nColBlocks):
            if i == 0 and j == 0:
                #top_left corner of source image is assigned to top_left corner of final image
                #in the case of texture synthesis random block is chosen
                final_img[0:block_size[0],0:block_size[1],:] = source_img[0:block_size[0],0:block_size[1],:]
                continue

            #coordinates of corner of block
            startX = int(i * (block_size[0] - overlap))
            startY = int(j * (block_size[1] - overlap))
            endX = int(min(startX + block_size[0], row_t))
            endY = int(min(startY + block_size[1], col_t))

            #subsets of final and target image under consideration
            final_crop = final_img[startX : endX, startY : endY, :]
            target_crop = target_crop_img[startX : endX, startY : endY, :]


            #the best block is such that the SSDerror is within the tolerance given
            #if the shape of subset of target image is same as that of block size
            if target_crop.shape == blocks.shape[1:]:
                Best_block = best_block(blocks, final_crop, target_crop, block_size, alpha, tolerance)
            else:
            #if the shape if target's subset is not same as that of block size, this can happen in corner/edge cases
                new_block_lst = create_blocks(source_img, row_s, col_s, target_crop.shape)
                Best_block = best_block(new_block_lst, final_crop, target_crop, block_size, alpha, tolerance)
            
            #coordinates of corners of new blocks on the final image 
            NB_startX = startX + overlap - Best_block.shape[0]
            NB_startY = startY + overlap - Best_block.shape[1]
            NB_endX = startX + overlap
            NB_endY = startY + overlap
            
            #for only vertical overlap
            if i == 0:      
                ov_type = 'v'
                Bl = final_img[startX : endX,NB_startY : NB_endY, :]
                Bl = Bl[:,:,0]
                Bt = 0
            #for only horizaontal overlap
            elif j == 0:          
                ov_type = 'h'
                Bl = 0
                Bt = final_img[NB_startX : NB_endX, startY : endY, :]
                Bt = Bt[:,:,0]
            #for all other cases
            else:
                ov_type = 'b'
                Bl = final_img[startX:endX,NB_startY:NB_endY,:]
                Bl = Bl[:,:,0]
                Bt = final_img[NB_startX:NB_endX, startY:endY, :]
                Bt = Bt[:,:,0]

            #mask with the best cut
            mask = minCostMask(Best_block[:,:,0],Bl,Bt,ov_type,overlap)
            mask = np.repeat(np.expand_dims(mask,axis=2),3,axis=2)
            #negation of the mask
            maskNegate = mask==0
            #updating final image with new patch/block
            final_img[startX:endX,startY:endY,:] = maskNegate*final_img[startX:endX,startY:endY,:]
            final_img[startX:endX,startY:endY,:] = Best_block*mask+final_img[startX:endX,startY:endY,:]
            progress = 100 * (i + j / nColBlocks) / nRowBlocks
            print("{0:.2f}% complete...".format(progress), end="\r", flush=True)

            if endY == col_t:
                break
        if endX == row_t:
            break
        #print(i, end=' ')
    return final_img