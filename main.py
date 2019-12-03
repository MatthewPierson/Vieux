#!/usr/bin/env python3

import os
import shutil
import ipsw
import restore

def pick3264(fname):
    if "iPhone5,1" in fname or "iPhone5,2" in fname or "iPhone4,1" in fname:
        print("32 bit device detected")
        ipsw.createCustomIPSW32(fname)
    else:
        devicehehe = input("What device do you want to downgrade? E.G : iPhone4,1 iPhone6,2 iPad4,3\n")
        if devicehehe == "iPhone6,1" or devicehehe == "iPhone6,2" or devicehehe == "iPad4,1" or devicehehe == "iPad4,2" or devicehehe == "iPad4,3" or devicehehe == "iPad4,4" or devicehehe == "iPad4,5":
            ipsw.createCustomIPSW64(fname, devicehehe)
        else:
            print("Not a valid device. Try again with a valid device please :). Exiting...")
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
    elif os.path.exists("restoreFiles/Mav7Mav8-7.60.00.Release.bbfw"):
        os.remove("restoreFiles/Mav7Mav8-7.60.00.Release.bbfw")
    elif os.path.exists("restoreFiles/sep-firmware.n53.RELEASE.im4p"):
        os.remove("restoreFiles/sep-firmware.n53.RELEASE.im4p")
    elif os.path.exists("custom.ipsw"):
        if remove:
            os.remove("custom.ipsw")
            if os.path.exists("restoreFiles/baseband.bbfw"):
                os.remove("restoreFiles/baseband.bbfw")
            elif os.path.exists("restoreFiles/sep.im4p"):
                os.remove("restoreFiles/sep.im4p")

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
    if os.path.exists("Firmware"):
        shutil.rmtree("Firmware")
    print("Files deleted.")


if __name__ =="__main__":
    print("Matty's Python OTA Downgrader!")
    print("Please connect a device in DFU mode...")
    print("Still in BETA so expect issues/broken things")
    restore.pwndfumode()
    ipsw.unzipIPSW()
    done = False
    print("Deleting unneeded files...")
    removeFiles(done)
    print("Done!")
    exit(0)

