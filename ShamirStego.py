import os, sys
from secretsharing import SecretSharer
import PySimpleGUI as sg
import json
from cryptosteganography import CryptoSteganography
import hashlib
from binascii import hexlify, unhexlify


def get_files(title):
    event, values = sg.Window(title).Layout([[sg.Input(key='_FILES_'), sg.FilesBrowse()], [sg.OK(), sg.Cancel()]]).Read()
    return values['_FILES_'].split(';')

def get_password(title):
    password = sg.popup_get_text(
        title, password_char='*')
    return password

def get_text(title):
    text = sg.popup_get_text(title)
    return text

def stego_share_encrypt():
    secretMessage = get_text("Enter Your Secret Message:")
    threshold = get_text("Enter Key Threshold Number:")
    numberOfKeys = get_text("Enter Number of Keys:")
    filename = get_files("Hold Shift and Choose "+str(numberOfKeys)+" PNG/JPG images:")
    password = get_password("Create a Master Password:")
    os.makedirs('shares', exist_ok=True)
    print(secretMessage, password, threshold, numberOfKeys, filename)
    shares = SecretSharer.split_secret(bytes.hex(bytes(secretMessage.encode())), int(threshold), int(numberOfKeys))
    for count, key in enumerate(shares):
        print(count, key)
        status = hide_message(key,filename[count],"shares/"+os.path.basename(filename[count]), password)
        print(status)
        
    sg.popup("Created "+numberOfKeys+" keys with a threshold min of "+threshold+" keys required.")
    #stegokey = json.loads(lsb.reveal("221blogo.png"))

def stego_share_decrypt():
    files = get_files("Hold shift and select files:")
    password = get_password("Enter your master password:")
    shares = []
    for file in files:
        shares.append(reveal_message(file,password))
    secret = bytes.fromhex(SecretSharer.recover_secret(shares))
    try:
        sg.popup("Your secret is", secret.decode())
    except UnicodeDecodeError:
        sg.popup("Your secret is", secret)
    except:
        sg.popup("Your secret is", hexlify(secret))
    return secret
        

def hide_message(message, originalfile, outputfile, password):
    crypto_steganography = CryptoSteganography(password)
    crypto_steganography.hide(originalfile, outputfile, message)
    return {'status': True, 'filename': outputfile, "password": password, 'secret_size': len(message)}

def reveal_message(image_filename, password=None):
    crypto_steganography = CryptoSteganography(password)
    return crypto_steganography.retrieve(image_filename)

#stego_share_encrypt()
secret = stego_share_decrypt()
print(hexlify(secret))
