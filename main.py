#!/usr/bin/env python3

import os
import shutil
import ipsw
import restore
import sys
import device
import platform
from contextlib import contextmanager


@contextmanager
def silence_stdout():
    new_target = open(os.devnull, "w")
    old_target = sys.stdout
    sys.stdout = new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target



def pick3264(fname):
    if "iPhone5,1" in fname or "iPhone5,2" in fname or "iPhone4,1" in fname:
        print("32 bit device detected")
        ipsw.createCustomIPSW32(fname)
    else:
        devicehehe = str(device.getmodel())
        if devicehehe == "iPhone6,1" or devicehehe == "iPhone6,2" or devicehehe == "iPad4,1" or devicehehe == "iPad4,2" or devicehehe == "iPad4,3" or devicehehe == "iPad4,4" or devicehehe == "iPad4,5":
            ipsw.createCustomIPSW64(fname, devicehehe)
        else:
            print('\033[91m' + "Not a valid device. Try again with a valid device please :). Exiting..." + '\033[0m')
            exit(2)


def removeFiles(remove):

    if os.path.exists("kernelcache.release.iphone6"):
        os.remove("kernelcache.release.iphone6")
    elif os.path.exists("kernelcache.release.iphone8b"):
        os.remove("kernelcache.release.iphone8b")
    elif os.path.exists("kernelcache.release.ipad4"):
        os.remove("kernelcache.release.ipad4")
    elif os.path.exists("kernelcache.release.ipad4b"):
        os.remove("kernelcache.release.ipad4b")
    elif os.path.exists("kernelcache.release.n42"):
        os.remove("kernelcache.release.n42")
    elif os.path.exists("ibss"):
        os.remove("ibss")
    elif os.path.exists("ibec"):
        os.remove("ibec")
    elif os.path.exists("restoreFiles/Mav7Mav8-7.60.00.Release.bbfw"):
        os.remove("restoreFiles/Mav7Mav8-7.60.00.Release.bbfw")
    elif os.path.exists("restoreFiles/sep-firmware.n53.RELEASE.im4p"):
        os.remove("restoreFiles/sep-firmware.n53.RELEASE.im4p")
    elif os.path.exists("restoreFiles/baseband.bbfw"):
        os.remove("restoreFiles/baseband.bbfw")
    elif os.path.exists("restoreFiles/sep.im4p"):
        os.remove("restoreFiles/sep.im4p")
    elif os.path.exists("restoreFiles/apnonce.shsh"):
        os.remove("restoreFiles/apnonce.shsh")
    dir_name = os.getcwd()
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".im4p"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".plist"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".dmg"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".shsh"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".shsh2"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".dfu"):
            os.remove(os.path.join(dir_name, item))
    if os.path.exists("Firmware"):
        shutil.rmtree("Firmware")
    elif os.path.exists("tsschecker"):
        shutil.move("tsschecker", "restoreFiles/tsschecker")
    elif os.path.exists("irecovery"):
        shutil.move("irecovery", "restoreFiles/irecovery")
    elif os.path.exists("futurerestore"):
        shutil.move("futurerestore", "restoreFiles/futurerestore")
    elif os.path.exists("futurerestore_32bit"):
        shutil.move("futurerestore_32bit", "restoreFiles/futurerestore_32bit")
    elif os.path.exists("igetnonce"):
        try:
            shutil.copy("igetnonce", "restoreFiles/igetnonce")
        except:
            return
    print("Files cleaned.")


if __name__ =="__main__":
    if platform.system() != 'Darwin':
        print("Sorry this OS is not supported! Only MacOS machines are support as of now.")
        exit(20)
    if os.path.exists("restoreFiles/igetnonce"):
        shutil.copy("restoreFiles/igetnonce", "igetnonce")
    elif os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    elif os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print('\033[95m' + "Matty's Python OTA Downgrader!" + '\033[0m')
    print("Still in BETA so expect issues/broken things")
    restore.pwndfumode()
    ipsw.unzipIPSW()
    done = False
    print("Cleaning up files...")
    removeFiles(done)
    print('\033[92m' + ''"Finished! Enjoy your downgraded phone :)" + '\033[0m')
    exit(0)

