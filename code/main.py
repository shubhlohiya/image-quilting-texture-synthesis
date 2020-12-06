from PIL import Image
import numpy as np
import argparse
parser = argparse.ArgumentParser()
from synthesize import  synthesize
from transfer import transfer
import sys

args = parser.parse_args()

def synthesis(args):
    try:
        img = np.asarray(Image.open(args.img).convert('RGB'))
        if args.height and args.width:
            h_out, w_out = args.height, args.width
        else:
            h_out, w_out =int(args.scale*img.shape[0]), int(args.scale*img.shape[1])
        result = synthesize(img, (args.block_size, args.block_size),
                            args.overlap, h_out, w_out, args.tolerance)
        result = Image.fromarray(result.astype('uint8'), 'RGB')
        result.show()
    except Exception as E:
        print("ERROR: ", E)
        sys.exit(1)

def transfer(args):
    try:
        pass
    except Exception as E:
        print("ERROR: ", E)
        sys.exit(1)

if __name__ == "__main__":
    parser.add_argument("--synthesis", action="store_true", help="perform texture synthesis")
    parser.add_argument("--transfer", action="store_true", help="perform texture transfer")
    parser.add_argument("-i", "--img", type=str, help="path of input image for synthesis/transfer")
    parser.add_argument("-tex", "--texture", type=str, help="path of texture image for transfer")
    # parser.add_argument("-tar", "--target", type=str, help="path of target image for transfer")
    parser.add_argument("-bs", "--block_size", type=int, default=100, help="block size in pixels")
    parser.add_argument("-ov", "--overlap", type=int, default=None,
                        help="overlap size in pixels (defaults to block_size/6)")
    parser.add_argument("-sc", "--scale", type=float, default=2, help="scaling w.r.t. to input texture")
    parser.add_argument("-h", "--height", type=int, default=None, help="output height")
    parser.add_argument("-w", "--width", type=int, default=None, help="output width")
    parser.add_argument("-t", "--tolerance", type=float, default=0.1, help="tolerance fraction")
    parser.add_argument("-a", "--alpha", type=float, default=0.1,
                        help="weightage of target image intensity error wrt texture boundary error")
    args = parser.parse_args()