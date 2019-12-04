from ipwndfu import dfu
import re
import os
import main

def getecid():
    device = dfu.acquire_device()
    serial = device.serial_number
    with main.silence_stdout():
        print(serial)

    try:
        found = re.search('ECID:(.+?) IBFL', serial).group(1)
        print("Your ECID is :", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't find ECID in serial" + '\033[0m')


def getapnonce():
    print("Getting current ApNonce from device...")
    cmd = './igetnonce'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)

    try:
        found = re.search('ApNonce=(.+?)\nSep', so).group(1)
        print("Your current ApNonce is :", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't get ApNonce from device" + '\033[0m')

def getmodel():
    print("Getting device model...")
    cmd = './igetnonce'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)
    try:
        found = re.search(', (.+?) in DFU mode', so).group(1)
        print("Your device is an ", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't get device model information" + '\033[0m')
