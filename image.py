#!/usr/bin/env python3

from PIL import Image
import argparse


def walk(width, height):
    """Generate x, y coordinates for an image"""
    for y in range(height):
        for x in range(width):
            yield x, y


def hide(img: Image, msg: str) -> Image:
    """Hide a message in an image"""
    nimg = img.copy()
    px = nimg.load()
    for x, y in walk(img.width, img.height):
        if x + y * img.width >= len(msg):
            break
        r, g, b = px[x, y]
        c = ord(msg[x + y * img.width])
        r = (r & 0b11111110) | ((c >> 6) & 0b1)
        g = (g & 0b11111000) | ((c >> 3) & 0b111)
        b = (b & 0b11111000) | (c & 0b111)
        px[x, y] = r, g, b
    return nimg


def unveil(img: Image, length: int) -> str:
    """Unveil a message from an image"""
    msg = ""
    px = img.load()
    for x, y in walk(img.width, img.height):
        if x + y * img.width >= length:
            break
        r, g, b = px[x, y]
        c = ((r & 0b1) << 6) | ((g & 0b111) << 3) | (b & 0b111)
        msg += chr(c)
    return msg


def main(args):
    if args.command == 'hide':
        img = Image.open(args.image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        nimg = hide(img, args.message)
        nimg.save(args.output)
    elif args.command == 'unveil':
        img = Image.open(args.image)
        msg = unveil(img, args.length)
        print(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', required=True)

    hide_parser = subparsers.add_parser('hide', help='Hide message in image')
    hide_parser.add_argument("--image", help="Image to process", required=True)
    hide_parser.add_argument("--output", help="Output file", required=True)
    hide_parser.add_argument(
        "--message", help="Message to hide", required=True)

    unveil_parser = subparsers.add_parser(
        'unveil', help='Unveil message from image')
    unveil_parser.add_argument(
        "--image", help="Image to process", required=True)
    unveil_parser.add_argument(
        "--length", type=int, help="Length of message", required=True)

    args = parser.parse_args()
    main(args)
