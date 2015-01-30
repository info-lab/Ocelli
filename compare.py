# Orthrus Carver
# Copyright (C) 2014 InFo-Lab
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# coding=utf-8

from PIL import Image, ImageChops
import os
import numpy as np
import sys


def ImageCompare(i1, i2, resize=True):
    """
    Receives two PIL images and compares them calculating the difference and measuring the 
    similarity in a range between 0 (no difference) and 1 (absolute difference).
    A value of 1 is the result of comparing a full white image against a full black image. A value
    of 0 is obtained when comparing two identical images.
    
    
    """
    if resize:
        i1 = i1.resize((500, 500), Image.BICUBIC)
        i2 = i2.resize((500, 500), Image.BICUBIC)
    i3 = ImageChops.difference(i1, i2)
    i3.show()
    arr = np.array(i3)
    return float(arr.sum()) / (500*500*(255*3))


class ImageData(object):
    """A data holding object, it stores a PIL image and its path."""
    def __init__(self, image, path):
        self.image = image
        self.path = path


def WalkCompare(args):
    images = []
    for root, dirs, files in os.walk(args.ofolder):
        for filename in files:
            extension = os.path.splitext(filename)[1].lower()
            if extension in args.formats:
                path = os.path.join(root, filename)
                im = Image.open(path)
                im = im.resize((500, 500), Image.BICUBIC)
                images.append(ImageData(im, path))
        #for file
    #for root
    for root, dirs, files in os.walk(args.ifolder):
        for filename in files:
            extension = os.path.splitext(filename)[1].lower()
            if extension in args.formats:
                path = os.path.join(root, filename)
                im1 = Image.open(path)
                im1 = im1.resize((500, 500), Image.BICUBIC)
                for i in images:
                    im2 = i.image
                    res = ImageCompare(im1, im2, False)
                    if res <= args.threshold:
                        print "%s, %s, %f" % (path, i.path, res)
        #for file
    #for root
    

def ArgParse():
    # parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description='compare: Compares two directorys looking for visually similar images.')
    parser.add_argument(
        'ofolder',
        help="The directory with the original images.")
    parser.add_argument(
        'ifolder',
        help="The directory that will be analysed.")
    parser.add_argument(
        "-t", 
        dest="threshold",
        type=float,
        default=0.1,
        help="The similarity threshold that determines if two images are similar.")
    args = parser.parse_args()
    return args


def main():
    args = ArgParse()
    args.formats = ['.jpg', '.png', '.bmp']
    if os.path.isdir(args.ifolder) and os.path.isdir(args.ofolder):
        WalkCompare(args)
    else:
        print "One of the specified directories is not a directory or does not exist."
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())