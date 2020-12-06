import numpy as np

def synthesize(img, blockSize, overlap, h_out, w_out, tolerance):
    """
    :param img: Array containing the input image
    :param blockSize: size of each block for texture synthesis
    :param overlap: size of overlap between blocks
    :param h_out: height of output
    :param w_out: width of output
    :param tolerance: fraction tolerance for neighbour block matching
    :return: synthesized texture
    """

    h,w,c = img.shape
    blocks = [] # list to contain all blocks of blockSize
    for i in range(h-blockSize[0]):
        for j in range(w-blockSize[1]):
            blocks.append(img[i:i + blockSize[0], j:j + blockSize[1], :])
    # intitialize output image array
    out_img = -np.ones((h_out, w_out, c))
    # dimensions of block indexing - i,j th block is in ith row, jth column
    nRowBlocks = np.ceil((h_out - blockSize[0])/(blockSize[0] - overlap)) + 1
    nColBlocks = np.ceil((w_out - blockSize[1])/(blockSize[1] - overlap)) + 1

    for i in range(nRowBlocks):
        for j in range(nColBlocks):
            if i==0 and j==0:
                out_img[0:blockSize[0], 0:blockSize[1], :] = np.random.choice(blocks)
                continue
            # get current block location
            startX = j * (blockSize[1] - overlap)
            endX = min(startX + blockSize[1], w_out)
            startY = i * (blockSize[0] - overlap)
            endY = min(startY + blockSize[0], h_out)
            curr_block = out_img[startY:endY, startX:endX, :]

            matched_block = get_match(blocks, curr_block, blockSize, tolerance)


def get_match(blocks, curr_block, blockSize, tolerance):
    """Function that returns a good block match for the current overlap."""
    h, w, c = curr_block.shape
    errors = [(SSDerror(block[0:h, 0:w, 0:c], curr_block)) block in blocks]
    min_error = np.min(errors)
    matches = [block[0:h, 0:w, 0:c] for i, block in enumerate(blocks)
               if errors[i]<=(1+tolerance)*min_error]
    return np.random.choice(matches)

def SSDerror(block1, block0):
    """Function that returns sum of squared differences between block1 and block0."""
    return np.sum((block0 != -1)*(block1-block0)**2)