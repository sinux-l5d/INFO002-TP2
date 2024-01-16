#!/usr/bin/env python3

from PIL import Image
import argparse
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256


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


def genkey(name: str, passphrase: str):
    """Generate a key for signing operations"""
    key = RSA.generate(4096)
    private_key = key.export_key(
        passphrase=passphrase, pkcs=8, protection="scryptAndAES256-CBC")
    public_key = key.publickey().export_key()
    with open(f"{name}.priv.pem", "wb") as f:
        f.write(private_key)
    with open(f"{name}.pub.pem", "wb") as f:
        f.write(public_key)


def sign(msg: str, privkey: str, passphrase: str, output: str):
    """Sign a message with a private key"""
    with open(privkey, "r") as f:
        privkey = RSA.import_key(f.read(), passphrase=passphrase)
    signature = pkcs1_15.new(privkey).sign(SHA256.new(msg.encode()))
    with open(output, "wb") as f:
        f.write(signature)


def verify(msg: str, pubkey: str, signature: str) -> bool:
    """Verify a message with a public key"""
    with open(pubkey, "r") as f:
        pubkey = RSA.import_key(f.read())
    with open(signature, "rb") as f:
        sig = f.read()
    try:
        pkcs1_15.new(pubkey).verify(SHA256.new(msg.encode()), sig)
        return True
    except (ValueError, TypeError):
        return False


def askpass(confirm: bool = False) -> str:
    """Ask for a passphrase"""
    if not confirm:
        return input("Enter passphrase: ")
    passphrase = ""
    while passphrase == "":
        prompt = input("Enter passphrase: ")
        prompt2 = input("Enter passphrase again: ")
        if prompt == prompt2:
            passphrase = prompt
        else:
            print("Passphrases do not match")
    return passphrase


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
    elif args.command == 'genkey':
        passphrase = askpass(True)
        genkey(args.name, passphrase)
    elif args.command == 'sign':
        passphrase = askpass()
        sign(args.message, args.key, passphrase, args.output)
    elif args.command == 'verify':
        if verify(args.message, args.key, args.signature):
            print("Signature is valid")
        else:
            print("Signature is invalid")


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

    genkey_parser = subparsers.add_parser(
        'genkey', help='Generate key for signing operations')
    genkey_parser.add_argument(
        "--name", help="Name of the key used to generate files", required=True)

    sign_parser = subparsers.add_parser(
        'sign', help='Sign a message with a private key')
    sign_parser.add_argument(
        "--message", help="Message to sign", required=True)
    sign_parser.add_argument(
        "--key", help="Private key to use", required=True)
    sign_parser.add_argument(
        "--output", help="Output file", required=True)

    verify_parser = subparsers.add_parser(
        'verify', help='Verify a message with a public key')
    verify_parser.add_argument(
        "--message", help="Message to verify", required=True)
    verify_parser.add_argument(
        "--key", help="Public key to use", required=True)
    verify_parser.add_argument(
        "--signature", help="Signature file to verify", required=True)

    args = parser.parse_args()
    main(args)
