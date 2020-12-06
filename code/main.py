from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse
import synthesize
# import textureTransfer
import sys

def LoadImage(infilename) :
    img = Image.open(infilename).convert('RGB')
    data = np.asarray(img)
    return data

def getMask(img_path, threshold):
    img_bw = Image.open(img_path).convert('LA').split()[0]
    mask = np.asarray(img_bw) > threshold
    return np.stack((mask, mask, mask), axis = 2)

def synthesis():
    try:
        img = LoadImage("../data/t7.png")
        img_size = img.shape

        # Get the generated texture
        new_h, new_w = int(2 * img_size[0]), int(2 * img_size[1])
        print(img.shape)
        new_img = synthesize.synthesize(img, [24, 24], 10 , new_h, new_w, 1)

        print(new_img.shape)
        # Save generated image if required
        # img_name = args.img_path.split("/")[-1].split(".")[0]
        img_to_save = Image.fromarray(new_img.astype('uint8'), 'RGB')
        img_to_save.save("../results/synthesis/"+"t7")
        # img_to_save.save("../results/synthesis/" + img_name + "_b=" + str(args.block_size) + "_o=" + str(args.overlap) + "_t=" + str(args.tolerance).replace(".", "_") + ".png")
    
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

synthesis()