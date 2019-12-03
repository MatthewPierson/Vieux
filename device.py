from ipwndfu import dfu
import re
import os


def getecid():
    device = dfu.acquire_device()
    serial = device.serial_number
    print(serial)

    try:
        found = re.search('ECID:(.+?) IBFL', serial).group(1)
        print("Your ECID is :", found)
        return found
    except AttributeError:
        print("ERROR: Couldn't find ECID in serial")


def getapnonce():
    print("Getting current ApNonce from device...")
    cmd = './igetnonce'
    so = os.popen(cmd).read()
    print(so)

    try:
        found = re.search('ApNonce=(.+?)\nSep', so).group(1)
        print("Your current ApNonce is :", found)
        return found
    except AttributeError:
        print("ERROR: Couldn't get ApNonce from device")
