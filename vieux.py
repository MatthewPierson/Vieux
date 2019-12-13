#!/usr/bin/env python3

import os
import shutil
import ipsw
import sys
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


def removeFiles(remove):

    if os.path.exists("kernelcache.release.iphone6"):
        os.remove("kernelcache.release.iphone6")
    elif os.path.exists("kernelcache.release.iphone8b"):
        os.remove("kernelcache.release.iphone8b")
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
    elif os.path.exists("resources/restoreFiles/Mav7Mav8-7.60.00.Release.bbfw"):
        os.remove("resources/restoreFiles/Mav7Mav8-7.60.00.Release.bbfw")
    elif os.path.exists("resources/restoreFiles/sep-firmware.n53.RELEASE.im4p"):
        os.remove("resources/restoreFiles/sep-firmware.n53.RELEASE.im4p")
    elif os.path.exists("resources/restoreFiles/baseband.bbfw"):
        os.remove("resources/restoreFiles/baseband.bbfw")
    elif os.path.exists("resources/restoreFiles/sep.im4p"):
        os.remove("resources/restoreFiles/sep.im4p")
    elif os.path.exists("resources/restoreFiles/apnonce.shsh"):
        os.remove("resources/restoreFiles/apnonce.shsh")
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
    print("Files cleaned.")


if __name__ =="__main__":
    if platform.system() != 'Darwin':
        print("Sorry this OS is not supported!\nOnly MacOS machines (Hackintosh or a legitimate Apple computer) are support as of now.")
        exit(20)
    if os.path.exists("resources/restoreFiles/igetnonce"):
        shutil.move("resources/restoreFiles/igetnonce", "igetnonce")
    if os.path.exists("resources/restoreFiles/tsschecker"):
        shutil.move("resources/restoreFiles/tsschecker", "tsschecker")
    if os.path.exists("resources/restoreFiles/futurerestore"):
        shutil.move("resources/restoreFiles/futurerestore", "futurerestore")
    if os.path.exists("resources/restoreFiles/irecovery"):
        shutil.move("resources/restoreFiles/irecovery", "irecovery")
    print('\033[95m' + "Vieux - A tool for 32/64 Bit OTA downgrades" + '\033[0m')
    print("Still in " + '\033[91m' + "BETA" + '\033[0m' + " so expect issues/broken things")
    print("If you are using a 64 Bit device then connect it in DFU Mode\nIf you are using a 32 Bit device then just have it connected in normal mode")
    ipsw.unzipIPSW()
    done = False
    print("Cleaning up files...")
    removeFiles(done)
    if os.path.exists("igetnonce"):
        shutil.move("igetnonce", "resources/restoreFiles/igetnonce")
    if os.path.exists("tsschecker"):
        shutil.move("tsschecker", "resources/restoreFiles/tsschecker")
    if os.path.exists("futurerestore"):
        shutil.move("futurerestore", "resources/restoreFiles/futurerestore")
    if os.path.exists("irecovery"):
        shutil.move("irecovery", "resources/restoreFiles/irecovery")
    print('\033[92m' + ''"Finished! Enjoy your downgraded phone :)" + '\033[0m')
    exit(0)

