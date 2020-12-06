import numpy as np 
from minErrorBoundaryCut import *
import cv2 as cv

def create_block_list(source_img, row_s, col_s, block_size):
	#dividing the given source image into square blocks of specified size and storing them into an array/listt
	blocks = []
	for i in range(row_s-block_size[0]):
		for j in range(col_s-block_size[1]):
			blocks.append(source_img[i : i + block_size[0], j : j + block_size[1], :])
	return np.asarray(blocks)

def Error(Block, final, target, alpha):

	#The error term in image quilting is modified by weighted a weighted sum,ɑ times the block overlap matching error
	#plus (1-ɑ) times squared error between the correspondence map pixels within the source texture block and those at current target image position.

	#block overlap matching error
	e1 =  np.sqrt(np.sum((final != -1)*((Block-final)**2)))
	#squared error between the correspondence map pixels within the source texture block and those at current target image position.
	e2 = np.sqrt(np.sum(((np.mean(final,axis=2) != -1)*(np.mean((Block-target), axis = 2))**2)))

	error = alpha * e1 + (1 - alpha) * e2
	#print(error)
	return error

def next_block(blocks, final, target, blocksize, alpha, tolerance):
	#creating an error array to store errors with all the blocls
	error = []
	row_f, col_f, ch_f = final.shape
	errors = [(Error(block[0:row_f, 0:col_f, 0:ch_f], final, target, alpha)) for block in blocks]
	min_error = np.min(errors)
	matches = [block[0:row_f, 0:col_f, 0:ch_f] for i, block in enumerate(blocks)
               if errors[i]<=(1+tolerance)*min_error]
	return matches[np.random.randint(len(matches))]

def Texture_Trasfer(source_img, target_img, block_size, tolerance, alpha, overlap=None):
	
	#setting the overlap size to length of box / 6, if not specified
	#assuming square blocks
	if overlap == None:
		overlap = block_size[0]//6

	#converting images into numpy arrays
	source_img = np.asarray(source_img)
	target_img = np.asarray(target_img)

	if len(source_img.shape) == 3:
		[row_s, col_s, ch_s] = source_img.shape
	else:
		[row_s, col_s] = source_img.shape

	if len(target_img.shape) == 3:
		[row_t, col_t, ch_t] = target_img.shape
	else:
		[row_t, col_t] = target_img.shape


	#initializing final image with -1s
	final_img = np.ones(target_img.shape)*-1

	#creaing a list of blocks
	print('.')
	blocks = create_block_list(source_img, row_s, col_s, block_size)
	print('.')
	#assigning the top left corner of final image with random block
	final_img[0:block_size[0], 0:block_size[1], :] = blocks[0]

	nRowBlocks = int(np.ceil((row_t - block_size[0])/(block_size[0] - overlap)) + 1)
	nColBlocks = int(np.ceil((col_t - block_size[1])/(block_size[1] - overlap)) + 1)


	for i in range(nRowBlocks):
		for j in range(nColBlocks):
			print(i,j)
			#we shall skip the top left block as it is already assignmed
			if i == 0 and j == 0:
				continue
			else:
				#print('.')
				#the corner indices of block, top-left and bottom-right
				TL_X = int(i*(block_size[0]-overlap))
				TL_Y = int(j*(block_size[1]-overlap))
				#taking care of corner cases
				BR_X = int(min(TL_X + block_size[0], row_t))
				BR_Y = int(min(TL_Y + block_size[1], col_t))


				#block corresponding to these values in the target image and final image
				target = target_img[TL_X:BR_X, TL_Y:BR_Y, :]
				final = final_img[TL_X:BR_X, TL_Y:BR_Y, :]
				#print('going to next')
				#if the block size is same as that of corresponding block in targer image
				#here the next_Block representes the block which satisfies given constraints and
				#has minimum error
				if block_size[0] == target.shape[0] and block_size[1] == target.shape[1]:
					next_Block = next_block(blocks, final, target, block_size, alpha, tolerance)
				else:
					#if the block size is not same as the corresponding block in target image
					#we need to make new blocks of the required dimensions
					new_blocks = create_block_list(source_img, row_s, col_s, target.shape)

					next_Block = next_block(new_blocks, final, target, target.shape, alpha, tolerance)
				#print('next_done')
				#the next_Block will be overlapping with the previous blocks
				#its corners can be given as follows where NB represents the new_Block
				NB_TL_X = TL_X + overlap - (next_Block.shape[0])
				NB_TL_Y = TL_Y + overlap - (next_Block.shape[1])
				NB_BR_X = TL_X + overlap 
				NB_BR_Y = TL_Y + overlap 
				#print(NB_TL_X, NB_TL_Y, NB_BR_X,NB_BR_Y)
				#according to overlap conditions and their minimum cut boundry conditions we can create masks
				#print('start mask')
				#for vertical overlaps
				if i == 0:
					Bl = final_img[TL_X : BR_X, NB_TL_Y : NB_BR_Y, :]
					Bl = Bl[:,:,0]
					Bt = 0
					#Bt = np.expand_dims(Bt, axis = 0)
					ov_type = 'v'
				#for horizontal overlaps
				elif j == 0:
					Bl = 0
					#Bl = np.expand_dims(Bl, axis = 0)
					Bt = final_img[NB_TL_X : NB_BR_X, TL_Y : BR_Y, :]
					Bt = Bt[:,:,0]
					ov_type = 'h'
				#for both overlaps
				else:
					Bl = final_img[TL_X : BR_X, NB_TL_Y : NB_BR_Y, :]
					Bl = Bl[:,:,0]
					Bt = final_img[NB_TL_X : NB_BR_X, TL_Y : BR_Y, :]
					Bt = Bt[:,:,0]
					ov_type = 'b'
				#calculating the mask from predefined function
				# print(Bl)
				# print(Bt)
				mask = minCostMask(next_Block[:,:,0], Bl, Bt, ov_type, overlap)
				#adjusting the dimensions of the mask
				mask = np.repeat(np.expand_dims(mask,axis=2),3,axis=2)
				neg_mask = mask == 0
				#print('done mask')
				#updating the final image by pasting the new block
				final_img[TL_X:BR_X, TL_Y:BR_Y, :] = neg_mask * final
				final_img[TL_X:BR_X, TL_Y:BR_Y, :] = mask * next_Block + final

		

	return final_img


target_img = cv.imread('/home/prathmesh/Desktop/CS663/image-quilting-texture-synthesis/data/lincoln.jpg')
source_img = cv.imread('/home/prathmesh/Desktop/CS663/image-quilting-texture-synthesis/data/t4.jpg')
alpha = 0.1
tolerance = 0.1
block_size = [30,30]
overlap = 15

for k in range(6):
	f = Texture_Trasfer(source_img, target_img, block_size, tolerance, alpha, overlap)
	source_img = f
	alpha = 0.8 * (k-1)/5 + 0.1
	block_size = [block_size[0] - 3, block_size[1] - 3]

cv.imwrite('f.jpg', f)