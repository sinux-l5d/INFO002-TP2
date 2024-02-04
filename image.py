#!/usr/bin/env python3

from PIL import Image
import argparse
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import diplome
from datetime import datetime
import base64


def walk(width, height):
    """Generate x, y coordinates for an image"""
    for y in range(height):
        for x in range(width):
            yield x, y


def hide(img: Image, msg: str) -> Image:
    """Hide a message in an image
        This function doesn't check if the message fits in the image!
    """
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


def genkey(passphrase: str, name: str = "diploma"):
    """Generate a key for signing operations"""
    key = RSA.generate(4096)
    private_key = key.export_key(
        passphrase=passphrase, pkcs=8, protection="scryptAndAES256-CBC")
    public_key = key.publickey().export_key()
    with open(f"{name}.priv.pem", "wb") as f:
        f.write(private_key)
    with open(f"{name}.pub.pem", "wb") as f:
        f.write(public_key)


def sign(msg: str, privkey: str, passphrase: str) -> bytes:
    """Sign a message with a private key"""
    with open(privkey, "r") as f:
        privkey = RSA.import_key(f.read(), passphrase=passphrase)
    return pkcs1_15.new(privkey).sign(SHA256.new(msg.encode()))


def verify(msg: str, pubkey: str, signature: str | bytes) -> bool:
    """Verify a message with a public key"""
    with open(pubkey, "r") as f:
        pubkey = RSA.import_key(f.read())
    if isinstance(signature, str):
        try:
            with open(signature, "rb") as f:
                sig = f.read()
        except (FileNotFoundError, ValueError):
            print("Invalid signature file")
            return False
    elif isinstance(signature, bytes):
        sig = signature
    else:
        print("Invalid signature type")
        return False
    try:
        pkcs1_15.new(pubkey).verify(SHA256.new(msg.encode()), sig)
        return True
    except (ValueError, TypeError):
        return False


def diploma(name: str, moyenne: int, diplome_name="master en alchimie", privkeypath="./diploma.priv.pem") -> Image:
    """Create a diploma"""
    DIPLOMA_NAME = diplome_name
    date = datetime.now().date().strftime("%d/%m/%Y")

    base = diplome.generate_diploma(
        DIPLOMA_NAME, name, date, moyenne)
    to_sign = DIPLOMA_NAME + name.lower().replace(" ", "") + date + str(moyenne)
    try:
        signature = sign(to_sign, privkeypath, askpass())
    except ValueError as e:
        print("Invalid passphrase: ", e)
        return

    infos = diplome.picklestr(DIPLOMA_NAME, name, date, moyenne, signature)
    base = diplome.write_length(base, len(infos))
    signed = hide(base, infos)
    print("Infos:", infos)
    print("Length:", len(infos))
    return signed


def verify_diploma(img: Image, length: int, pubkey: str = "./diploma.pub.pem") -> bool:
    """Verify a diploma"""
    try:
        diplomename, name, date, moyenne, signature = diplome.unpicklestr(
            unveil(img, length))
    except:
        print("Could not unveil the diploma infos")
        return False
    print("Diploma:", diplomename)
    print("Name:", name)
    print("Date:", date)
    print("Moyenne:", moyenne)
    print("Signature:", signature)
    to_sign = diplomename + name.lower().replace(" ", "") + date + str(moyenne)
    ok = verify(to_sign, pubkey, signature)
    if not ok:
        print("SIGNATURE IS INVALID!")
    else:
        print("Signature is valid, but check the infos are the same as expected")
    return ok


def askpass(confirm: bool = False) -> str:
    """Ask for a passphrase"""
    if not confirm:
        return input("Enter passphrase: ").strip()
    passphrase = ""
    while passphrase == "":
        prompt = input("Enter passphrase: ").strip()
        prompt2 = input("Enter passphrase again: ").strip()
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
        msg = unveil(img)
        print(msg)
    elif args.command == 'genkey':
        passphrase = askpass(True)
        genkey(passphrase, args.name)
    elif args.command == 'sign':
        passphrase = askpass()
        signature = sign(args.message, args.key, passphrase)
        with open(args.output, "wb") as f:
            f.write(signature)
    elif args.command == 'verify':
        if verify(args.message, args.key, args.signature):
            print("Signature is valid")
        else:
            print("Signature is invalid")
    elif args.command == 'diploma':
        img = diploma(args.student, args.moyenne, args.name, args.privkey)
        if img:
            img.save(args.output)
    elif args.command == 'verify_diploma':
        img = Image.open(args.image)
        verify_diploma(img, args.length, args.key)


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

    genkey_parser = subparsers.add_parser(
        'genkey', help='Generate key for signing operations')
    genkey_parser.add_argument(
        "--name", help="Name of the key", required=False, default="diploma")

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

    diploma_parser = subparsers.add_parser(
        'diploma', help='Generate a diploma')
    diploma_parser.add_argument(
        "--name", help="Name of the diploma", required=False, default="master en alchimie")
    diploma_parser.add_argument(
        "--student", help="Student obtaining the diploma", required=True)
    diploma_parser.add_argument(
        "--output", help="Output file (default diploma.png)", required=False, default="diploma.png")
    diploma_parser.add_argument(
        "--moyenne", type=float, help="Average grade", required=False, default=10)
    diploma_parser.add_argument(
        "--privkey", help="Private key to use", required=False, default="./diploma.priv.pem")

    verify_diploma_parser = subparsers.add_parser(
        'verify_diploma', help='Verify a diploma')
    verify_diploma_parser.add_argument(
        "--image", help="Image to process", required=True)
    verify_diploma_parser.add_argument(
        "--key", help="Public key to use", required=False, default="./diploma.pub.pem")
    verify_diploma_parser.add_argument(
        "--length", type=int, help="Length written in the top left corner", required=True)

    args = parser.parse_args()
    main(args)
