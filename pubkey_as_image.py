import os, sys
from binascii import hexlify, unhexlify
from stegano import lsb
import requests 

def get_image(image_url, filename):
    r = requests.get(image_url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
    with open(filename, 'wb') as pb:
        #print(r.content)
        pb.write(r.content)
    return filename




def reveal(infile, outfile):
    pubkey = lsb.reveal(infile)
    pubkey = unhexlify(pubkey.strip("b'"))
    with open(outfile, 'w') as f:
        f.write(pubkey.decode())
    return pubkey.decode()

print(reveal(get_image("https://images.squarespace-cdn.com/content/v1/5e236b891195f14156d82cbc/b7347d29-2744-40cc-86d6-caf9ca0cd9e1/2.png",'logo221b.png'), 'mypubkey.asc'))
