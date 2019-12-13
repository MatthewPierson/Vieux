import os
import shutil
import bsdiff4
import device as localdevice
from pathlib import Path
from zipfile import ZipFile
from restore import restore64, restore32, pwndfumode

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

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def unzipIPSW():

    if os.path.exists("custom.ipsw"):
            os.remove("custom.ipsw")

    fname = input("Enter the path to the IPSW file (Or drag and drop the IPSW into this window):\n")
    print("Starting IPSW unzipping")
    outputFolder = os.getcwd()
    newpath = fname.rstrip()
    fname = str(newpath)
    testFile = os.path.exists(fname)

    while not testFile or not fname.endswith!=(".ipsw"):
        print("Invalid filepath/filename.\nPlease try again with a valid filepath/filename.")
        fname = input("Enter the path to the IPSW file (Or drag and drop the IPSW into this window):\n")
        newpath = fname.rstrip()
        fname = str(newpath)
        testFile = os.path.exists(fname)
    else:
        #Will now continue with new valid file
        print("Continuing...")
    if testFile and fname.endswith(".ipsw"):
        print("IPSW found at given path...")
        print("Cleaning up old files...")
        done = True
        removeFiles(done)
        print("Unzipping..")
        with ZipFile(fname, 'r') as zip_ref:
            zip_ref.extractall(outputFolder)

        source = ("Firmware/dfu/")
        dest1 = os.getcwd()

        files = os.listdir(source)

        for f in files:
            shutil.move(source + f, dest1)
        devicemodel = str(localdevice.getmodel())
        t = localdevice.pick3264(devicemodel, fname)
        if t == 32:
            createCustomIPSW32(fname)
        elif t == 64:
            pwndfumode()
            createCustomIPSW64(fname, devicemodel)
        else:
            exit(2)

    else:
        print('\033[91m' + "ERROR: Not valid filepath...")
        print("ERROR: Try again" + '\033[0m')

def createCustomIPSW32(fname):
    if os.path.exists("resources/restoreFiles/futurerestore"):
        shutil.move("resources/restoreFiles/futurerestore", "futurerestore")
    print("Starting iBSS/iBEC patching")
    kloader10location = "resources/restoreFiles/kloader10"
    kloaderlocation = "resources/restoreFiles/kloader"
    patch_folder = Path("resources/patches/")
    phone5ibss = patch_folder / "ibss.iphone5.patch"
    phone4sibss6 = patch_folder / "ibss.iphone4,1.6.1.3.patch"
    phone4sibss8 = patch_folder / "ibss.iphone4,1.8.4.1.patch"
    if "iPhone5,2" in fname or "iPhone5,1" in fname and "8.4.1" in fname:
        print("Looks like you are downgrading an iPhone 5 to 8.4.1!")
        bsdiff4.file_patch_inplace("iBSS.n42.RELEASE.dfu", phone5ibss)
        shutil.copy("iBSS.n42.RELEASE.dfu", "ibss")
        ibsslocation = "ibss"
        device = "iPhone5"
        if "iPhone5,2" in fname:
            model = "iPhone5,2"
        elif "iPhone5,1" in fname:
            model = "iPhone5,1"
    elif "6.1.3" in fname or "8.4.1" in fname and "iPhone4,1" in fname:
        device = "iPhone4s"
        model = "iPhone4,1"
    else:
        print('\033[91m' + "Im tired" + '\033[0m')
        exit(24)

    if device == "iPhone5":
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloader10location, ibsslocation)
        restore32(model, iosversion)
    elif device == "iPhone4s":
        if "8.4.1" in fname:
            print("Looks like you are downgrading an iPhone 4s to 8.4.1!")
            iosversion = "8.4.1"
            bsdiff4.file_patch_inplace("iBSS.n94.RELEASE.dfu", phone4sibss8)
            shutil.copy("iBSS.n94.RELEASE.dfu", "ibss")
            ibsslocation = "ibss"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloader10location, ibsslocation)
            restore32(model, iosversion)
        elif "6.1.3" in fname:
            print("Looks like you are downgrading an iPhone 4s to 6.1.3!")
            iosversion = "6.1.3"
            bsdiff4.file_patch_inplace("iBSS.n94ap.RELEASE.dfu", phone4sibss6)
            shutil.copy("iBSS.n94ap.RELEASE.dfu", "ibss")
            ibsslocation = "ibss"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloader10location, ibsslocation)
            restore32(model, iosversion)
        else:
            print("=(")
            exit(2)
    else:
        print("=(")
        exit(2)
def createCustomIPSW64(fname, devicemodel):
    print("Starting iBSS/iBEC patching")
    patch_folder = Path("resources/patches/")
    phoneibec = patch_folder / "ibec5s.patch"
    phoneibss = patch_folder / "ibss5s.patch"
    ipadminiibec = patch_folder / "ibec_ipad4b.patch"
    ipadminiibss = patch_folder / "ibss_ipad4b.patch"
    ipadairibec = patch_folder / "ibec_ipad4.patch"
    ipadairibss = patch_folder / "ibss_ipad4.patch"
    if "iPhone" in fname and "10.3.3" in fname:
        print("Looks like you are downgrading an iPhone 5s to 10.3.3!")
        bsdiff4.file_patch_inplace("iBEC.iphone6.RELEASE.im4p", phoneibec)
        bsdiff4.file_patch_inplace("iBSS.iphone6.RELEASE.im4p", phoneibss)
        device = "iPhone5s"
    elif "iPad" in fname and "10.3.3" in fname:
        if devicemodel == "iPad4,1" or devicemodel == "iPad4,2" or devicemodel == "iPad4,3":
            print("Looks like you are downgrading an iPad Air to 10.3.3!")
            bsdiff4.file_patch_inplace("iBEC.ipad4.RELEASE.im4p ", ipadairibec)
            bsdiff4.file_patch_inplace("iBSS.ipad4.RELEASE.im4p", ipadairibss)
            device = "iPadAir"
        elif devicemodel == "iPad4,4" or devicemodel == "iPad4,5":
            print("Looks like you are downgrading an iPad Mini 2 to 10.3.3!")
            bsdiff4.file_patch_inplace("iBEC.ipad4b.RELEASE.im4p ", ipadminiibec)
            bsdiff4.file_patch_inplace("iBSS.ipad4b.RELEASE.im4p", ipadminiibss)
            device = "iPadMini"
        else:
            print("ERROR: Unknown input. Exiting purely because you can't read and that's sad...")
            print("ERROR: Exiting...")
            exit(1)
    print("Patched iBSS/iBEC")
    print("About to re-build IPSW")

    if device == "iPhone5s":
        shutil.move("iBEC.iphone6.RELEASE.im4p", "Firmware/dfu/")
        shutil.move("iBSS.iphone6.RELEASE.im4p", "Firmware/dfu/")
        shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/restoreFiles/baseband.bbfw")
        if devicemodel == "iPhone6,1":
            shutil.move("Firmware/all_flash/sep-firmware.n51.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
        elif devicemodel == "iPhone6,2":
            shutil.move("Firmware/all_flash/sep-firmware.n53.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
        touch("Firmware/usr/local/standalone/blankfile")
        with ZipFile('custom.ipsw', 'w') as zipObj2:
            zipObj2.write('Restore.plist')
            zipObj2.write('kernelcache.release.iphone8b')
            zipObj2.write('kernelcache.release.iphone6')
            zipObj2.write('BuildManifest.plist')
            zipObj2.write('058-75381-062.dmg')
            zipObj2.write('058-74940-063.dmg')
            zipObj2.write('058-74917-062.dmg')
            zipObj2.write('._058-74917-062.dmg')
            for folderName, subfolders, filenames in os.walk("Firmware"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj2.write(filePath)
        restore64(devicemodel)

    elif device == "iPadAir" or device == "iPadMini":
        if devicemodel == "iPad4,1" or devicemodel == "iPad4,2" or devicemodel == "iPad4,3":
            shutil.move("iBEC.ipad4.RELEASE.im4p", "Firmware/dfu/")
            shutil.move("iBSS.ipad4.RELEASE.im4p", "Firmware/dfu/")
            if devicemodel == "iPad4,1":
                shutil.move("Firmware/all_flash/sep-firmware.j71.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
            elif devicemodel == "iPad4,2":
                shutil.move("Firmware/all_flash/sep-firmware.j72.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/restoreFiles/baseband.bbfw")
            elif devicemodel == "iPad4,3":
                shutil.move("Firmware/all_flash/sep-firmware.j73.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/restoreFiles/baseband.bbfw")
        elif devicemodel == "iPad4,4" or devicemodel == "iPad4,5":
            shutil.move("iBEC.ipad4b.RELEASE.im4p", "Firmware/dfu/")
            shutil.move("iBSS.ipad4b.RELEASE.im4p", "Firmware/dfu/")
            if devicemodel == "iPad4,4":
                shutil.move("Firmware/all_flash/sep-firmware.j85.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
            elif devicemodel == "iPad4,5":
                shutil.move("Firmware/all_flash/sep-firmware.j86.RELEASE.im4p", "resources/restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/restoreFiles/baseband.bbfw")
        touch("Firmware/usr/local/standalone/blankfile")

        with ZipFile('custom.ipsw', 'w') as zipObj2:
            zipObj2.write('Restore.plist')
            zipObj2.write('kernelcache.release.ipad4')
            zipObj2.write('kernelcache.release.ipad4b')
            zipObj2.write('BuildManifest.plist')
            zipObj2.write('058-75381-062.dmg')
            zipObj2.write('058-75094-062.dmg')
            zipObj2.write('058-74940-063.dmg')
            zipObj2.write('._058-75094-062.dmg')
            for folderName, subfolders, filenames in os.walk("Firmware"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj2.write(filePath)
        restore64(devicemodel)
    else:
        print('\033[91m' + "something broke lmao" + '\033[0m')
        exit(1)
