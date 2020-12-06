from PIL import Image
import numpy as np
import sys, argparse
parser = argparse.ArgumentParser()
from synthesize import  synthesize
from transfer import texturize

def synthesis(args):
    try:
        img = np.asarray(Image.open(args.img).convert('RGB'))
        if args.height and args.width:
            h_out, w_out = args.height, args.width
        else:
            h_out, w_out =int(args.scale*img.shape[0]), int(args.scale*img.shape[1])
        overlap = args.overlap
        if not args.overlap:
            overlap = int(args.block_size/6)
        result = synthesize(img, (args.block_size, args.block_size),
                            overlap, h_out, w_out, args.tolerance)
        result = Image.fromarray(result.astype('uint8'), 'RGB')
        result.show()
        if args.save:
            name = args.img.split("/")[-1].split(".")[0]
            result.save("../results/synthesis/"+name+"_b="+str(args.block_size)+"_o="+
                        str(overlap)+"_t="+str(args.tolerance).replace(".", "_")+".png")
    except Exception as E:
        print("ERROR: ", E)
        sys.exit(1)

def transfer(args):
    try:
        texture = np.asarray(Image.open(args.texture).convert('RGB'))
        target = np.asarray(Image.open(args.img).convert('RGB'))

        overlap = args.overlap
        if not args.overlap:
            overlap = int(args.block_size / 2)
        result = texturize(texture, target, (args.block_size, args.block_size),
                           overlap, args.alpha, args.tolerance)
        result = Image.fromarray(result.astype('uint8'), 'RGB')
        result.show()
        if args.save:
            texture_name = args.texture.split("/")[-1].split(".")[0]
            target_name = args.img.split("/")[-1].split(".")[0]
            result.save("../results/transfer/"+texture_name+"_"+target_name+"_b="+str(args.block_size)+"_o="+
                        str(overlap)+"_a="+str(args.alpha).replace(".", "_")+"_t="+
                        str(args.tolerance).replace(".", "_")+".png")
    except Exception as E:
        print("ERROR: ", E)
        sys.exit(1)

if __name__ == "__main__":
    parser.add_argument("--synthesis", action="store_true", help="perform texture synthesis")
    parser.add_argument("--transfer", action="store_true", help="perform texture transfer")
    parser.add_argument("--save", action="store_true", help="save result")
    parser.add_argument("--img", "-i", type=str, help="path of input image for synthesis/transfer")
    parser.add_argument("--texture", "-t", type=str, help="path of texture image for transfer")
    parser.add_argument("--block_size", "-b", type=int, default=100, help="block size in pixels")
    parser.add_argument("--overlap", "-o", type=int, default=None,
                        help="overlap size in pixels (defaults to block_size/6)")
    parser.add_argument("-sc", "--scale", type=float, default=2, help="scaling w.r.t. to input texture")
    parser.add_argument("--height", "-oh", type=int, default=None, help="output height")
    parser.add_argument("--width", "-ow", type=int, default=None, help="output width")
    parser.add_argument("--tolerance", "-tol", type=float, default=0.1, help="tolerance fraction")
    parser.add_argument("--alpha", "-a", type=float, default=0.1,
                        help="weightage of target image intensity error wrt texture boundary error")
    args = parser.parse_args()

    if args.synthesis and args.transfer:
        print("ERROR: Either synthesis or transfer can be performed at once")
        sys.exit(1)
    elif args.synthesis:
        synthesis(args)
    elif args.transfer:
        transfer(args)
    else:
        print("ERROR: Either synthesis or transfer must be selected")