import os
import shutil
import bsdiff4
import plistlib
import sys
import device as localdevice
from pathlib import Path
from zipfile import ZipFile, is_zipfile
from restore import restore64, restore32, pwndfumode

def readmanifest(path, flag):
    fn = path
    with open(fn, 'rb') as f:
        pl = plistlib.load(f)

    if flag:
        result = pl['ProductVersion']
    else:
        supportedModels = str(pl['SupportedProductTypes'])
        supportedModels1 = supportedModels.replace("[", "")
        supportedModels2 = supportedModels1.replace("'", "")
        result = supportedModels2.replace("]", "")

    return result


def removeFiles():

    randomfiles = [

    'errorlogshsh.txt', 'errorlogrestore.txt', 'ibss', 'ibec', 'resources/other/baseband.bbfw',
    'resources/other/sep.im4p', 'resources/other/apnonce.shsh'

    ]

    for item in randomfiles:
        if os.path.isfile(item):
            os.remove(item)

    if os.path.exists("IPSW"):
        shutil.rmtree("IPSW")
    if os.path.exists("Firmware"):
        shutil.rmtree("Firmware")
    if os.path.exists("custom"):
        shutil.rmtree('custom')

    if os.path.exists("igetnonce"):
        os.remove("igetnonce")

    if os.path.exists("tsschecker"):
        os.remove("tsschecker")

    if os.path.exists("futurerestore"):
        os.remove("futurerestore")

    if os.path.exists("irecovery"):
        os.remove("irecovery")

    if os.path.exists("custom.ipsw"):
        os.remove("custom.ipsw")

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

    print("Files cleaned.")


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def unzipIPSW(fname):
    armv7 = ['iPhone4,1', 'iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4', 'iPad2,5', 'iPad2,6', 'iPad2,7', 'iPod5,1']
    armv7s = ['iPhone5,1', 'iPhone5,2', 'iPad3,4', 'iPad3,5', 'iPad3,6', 'iPad3,1', 'iPad3,2', 'iPad3,3']

    if is_zipfile(fname): # First of all, check to see if fname is an actual ipsw, by verifying the file is a zip archive (ipsw's are just zip files).
        print(f'{fname} is a zip archive!')
    else:
        sys.exit(f'"{fname}" is not a zip archive! Are you sure you inserted the correct ipsw path?')

    if os.path.exists("custom.ipsw"):
        os.remove("custom.ipsw")

    print("Starting IPSW unzipping")
    outputFolder = "IPSW"
    newpath = fname.rstrip()
    fname = str(newpath)
    testFile = os.path.exists(fname)

    if os.path.exists('IPSW'):
        shutil.rmtree('IPSW')
        os.mkdir('IPSW')
    elif not os.path.exists('IPSW'):
        os.mkdir('IPSW')

    while not testFile or not fname.endswith!=(".ipsw"):
        print("Invalid filepath/filename.\nPlease try again with a valid filepath/filename.")
        fname = input("Enter the path to the IPSW file (Or drag and drop the IPSW into this window):\n")
        newpath = fname.rstrip()
        fname = str(newpath)
        testFile = os.path.exists(fname)

    else:
        print("Continuing...")

    if testFile and fname.endswith(".ipsw"):

        print("IPSW found at given path...")
        print("Cleaning up old files...")
        removeFiles()
        print("Unzipping..")

        with ZipFile(fname, 'r') as zip_ref:
            zip_ref.extractall(outputFolder)
        source = ("IPSW/Firmware/dfu/")
        dest1 = os.getcwd()

        files = os.listdir(source)

        for f in files:
            shutil.move(source + f, dest1)
        devicemodel = str(localdevice.getmodel())
        version = False
        supportedModels = str(readmanifest("IPSW/BuildManifest.plist", version))

        if supportedModels in armv7:
            createCustomIPSW32(fname)

        else:
            if supportedModels in armv7s:
                createCustomIPSW32(fname)

            else:
                arm64check = ('iPhone6,1', 'iPhone6,2', 'iPad4,1', 'iPad4,2', 'iPad4,3', 'iPad4,4', 'iPad4,5')

                if any(ext in supportedModels for ext in arm64check):
                    if any(ext in devicemodel for ext in arm64check):
                        pwndfumode()
                        createCustomIPSW64(fname, devicemodel)

                    else:
                        print("ERROR: Unsupported model...\nExiting...")
                        exit(82)

                else:
                    print("ERROR: Unsupported model...\nExiting...")
                    exit(82)

    else:
        print('\033[91m' + "ERROR: Not valid filepath...")
        print("ERROR: Try again" + '\033[0m')


def createCustomIPSW32(fname):

    print("Starting iBSS/iBEC patching")
    kloaderlocation = "resources/bin/kloader"
    kloaderlocation10 = "resources/bin/kloader10"
    patch_folder = Path("resources/patches/")
    phone52ibss = patch_folder / "ibss.iphone52.patch"
    phone51ibss = patch_folder / "ibss.iphone51.patch"
    phone4sibss6 = patch_folder / "ibss.iphone4,1.613.patch"
    phone4sibss8 = patch_folder / "ibss.iphone4,1.841.patch"
    pad21ibss6 = patch_folder / "ibss.ipad2,1.613.patch"
    pad22ibss6 = patch_folder / "ibss.ipad2,2.613.patch"
    pad23ibss6 = patch_folder / "ibss.ipad2,3.613.patch"
    pad21ibss8 = patch_folder / "ibss.ipad2,1.841.patch"
    pad22ibss8 = patch_folder / "ibss.ipad2,2.841.patch"
    pad23ibss8 = patch_folder / "ibss.ipad2,3.841.patch"
    pad24ibss8 = patch_folder / "ibss.ipad2,4.841.patch"
    pad31ibss = patch_folder / "ibss.ipad31.patch"
    pad32ibss = patch_folder / "ibss.ipad32.patch"
    pad33ibss = patch_folder / "ibss.ipad33.patch"
    pad34ibss = patch_folder / "ibss.ipad34.patch"
    pad35ibss = patch_folder / "ibss.ipad35.patch"
    pad36ibss = patch_folder / "ibss.ipad36.patch"
    pad25ibss = patch_folder / "ibss.ipad25.patch"
    pad26ibss = patch_folder / "ibss.ipad26.patch"
    pad27ibss = patch_folder / "ibss.ipad27.patch"
    podibss = patch_folder / "ibss.ipod51.patch"


    version = True
    versionManifest = readmanifest("IPSW/BuildManifest.plist", version)
    version = False
    deviceManifest = readmanifest("IPSW/BuildManifest.plist", version)

    if "iPhone5,2" in deviceManifest and "8.4.1" in versionManifest or "iPhone5,1" in deviceManifest and "8.4.1" in versionManifest:
        print("Looks like you are downgrading an iPhone 5 to 8.4.1!")

        if "iPhone5,2" in deviceManifest:
            bsdiff4.file_patch_inplace("iBSS.n42.RELEASE.dfu", phone52ibss)
            shutil.copy("iBSS.n42.RELEASE.dfu", "ibss")
            model = "iPhone5,2"

        elif "iPhone5,1" in deviceManifest:
            bsdiff4.file_patch_inplace("iBSS.n41.RELEASE.dfu", phone51ibss)
            shutil.copy("iBSS.n41.RELEASE.dfu", "ibss")
            model = "iPhone5,1"
        ibsslocation = "ibss"
        device = "iPhone5"

    elif "6.1.3" in versionManifest and "iPhone4,1" in deviceManifest:
        device = "iPhone4s"
        model = "iPhone4,1"
    elif "8.4.1" in versionManifest and "iPhone4,1" in deviceManifest:
        device = "iPhone4s"
        model = "iPhone4,1"

    elif "8.4.1" in versionManifest and "iPad3,4" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p101.RELEASE.dfu", pad34ibss)
        shutil.copy("iBSS.p101.RELEASE.dfu", "ibss")
        model = "iPad3,4"
        ibsslocation = "ibss"
        device = "iPad4"
    elif "8.4.1" in versionManifest and "iPad3,5" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p102.RELEASE.dfu", pad35ibss)
        shutil.copy("iBSS.p102.RELEASE.dfu", "ibss")
        model = "iPad3,5"
        ibsslocation = "ibss"
        device = "iPad4"
    elif "8.4.1" in versionManifest and "iPad3,6" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p103.RELEASE.dfu", pad36ibss)
        shutil.copy("iBSS.p103.RELEASE.dfu", "ibss")
        model = "iPad3,6"
        ibsslocation = "ibss"
        device = "iPad4"
    elif "6.1.3" in versionManifest and "iPad2,1" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k93ap.RELEASE.dfu", pad21ibss6)
        shutil.copy("iBSS.k93ap.RELEASE.dfu", "ibss")
        model = "iPad2,1"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "6.1.3" in versionManifest and "iPad2,2" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k94ap.RELEASE.dfu", pad22ibss6)
        shutil.copy("iBSS.k94ap.RELEASE.dfu", "ibss")
        model = "iPad2,2"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "6.1.3" in versionManifest and "iPad2,3" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k95ap.RELEASE.dfu", pad23ibss6)
        shutil.copy("iBSS.k95ap.RELEASE.dfu", "ibss")
        model = "iPad2,3"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "8.4.1" in versionManifest and "iPad2,1" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k93.RELEASE.dfu", pad21ibss8)
        shutil.copy("iBSS.k93.RELEASE.dfu", "ibss")
        model = "iPad2,1"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "8.4.1" in versionManifest and "iPad2,2" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k94.RELEASE.dfu", pad22ibss8)
        shutil.copy("iBSS.k94.RELEASE.dfu", "ibss")
        model = "iPad2,2"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "8.4.1" in versionManifest and "iPad2,3" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k95.RELEASE.dfu", pad23ibss8)
        shutil.copy("iBSS.k95.RELEASE.dfu", "ibss")
        model = "iPad2,3"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "8.4.1" in versionManifest and "iPad2,4" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.k93a.RELEASE.dfu", pad24ibss8)
        shutil.copy("iBSS.k93a.RELEASE.dfu", "ibss")
        model = "iPad2,4"
        ibsslocation = "ibss"
        device = "iPad2"
    elif "8.4.1" in versionManifest and "iPad3,1" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.j1.RELEASE.dfu", pad31ibss)
        shutil.copy("iBSS.j1.RELEASE.dfu", "ibss")
        model = "iPad3,1"
        ibsslocation = "ibss"
        device = "iPad3"
    elif "8.4.1" in versionManifest and "iPad3,2" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.j2.RELEASE.dfu", pad32ibss)
        shutil.copy("iBSS.j2.RELEASE.dfu", "ibss")
        model = "iPad3,2"
        ibsslocation = "ibss"
        device = "iPad3"
    elif "8.4.1" in versionManifest and "iPad3,3" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.j3.RELEASE.dfu", pad33ibss)
        shutil.copy("iBSS.j3.RELEASE.dfu", "ibss")
        model = "iPad3,3"
        ibsslocation = "ibss"
        device = "iPad3"
    elif "8.4.1" in versionManifest and "iPod5,1" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.n78.RELEASE.dfu", podibss)
        shutil.copy("iBSS.n78.RELEASE.dfu", "ibss")
        model = "iPod5,1"
        ibsslocation = "ibss"
        device = "iPod5"
    elif "8.4.1" in versionManifest and "iPad2,5" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p105.RELEASE.dfu", pad25ibss)
        shutil.copy("iBSS.p105.RELEASE.dfu", "ibss")
        model = "iPad2,5"
        ibsslocation = "ibss"
        device = "iPadmini"
    elif "8.4.1" in versionManifest and "iPad2,6" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p106.RELEASE.dfu", pad26ibss)
        shutil.copy("iBSS.p106.RELEASE.dfu", "ibss")
        model = "iPad2,6"
        ibsslocation = "ibss"
        device = "iPadmini"
    elif "8.4.1" in versionManifest and "iPad2,7" in deviceManifest:
        bsdiff4.file_patch_inplace("iBSS.p107.RELEASE.dfu", pad27ibss)
        shutil.copy("iBSS.p107.RELEASE.dfu", "ibss")
        model = "iPad2,7"
        ibsslocation = "ibss"
        device = "iPadmini"
    else:
        print('\033[91m' + "Im tired" + '\033[0m')
        exit(24)

    if device == "iPhone5":
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
        restore32(model, iosversion)

    elif device == "iPhone4s":
        if "8.4.1" in versionManifest:
            print("Looks like you are downgrading an iPhone 4s to 8.4.1!")
            iosversion = "8.4.1"
            bsdiff4.file_patch_inplace("iBSS.n94.RELEASE.dfu", phone4sibss8)
            shutil.copy("iBSS.n94.RELEASE.dfu", "ibss")
            ibsslocation = "ibss"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
            restore32(model, iosversion)

        elif "6.1.3" in versionManifest:
            print("Looks like you are downgrading an iPhone 4s to 6.1.3!")
            iosversion = "6.1.3"
            bsdiff4.file_patch_inplace("iBSS.n94ap.RELEASE.dfu", phone4sibss6)
            shutil.copy("iBSS.n94ap.RELEASE.dfu", "ibss")
            ibsslocation = "ibss"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
            restore32(model, iosversion)

        else:
            print("=(")
            exit(2)
    elif device == "iPad4":
        print("Looks like you are downgrading an iPad4 to 8.4.1!")
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
        restore32(model, iosversion)
    elif device == "iPadmini":
        print("Looks like you are downgrading an iPad Mini 1 to 8.4.1!")
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
        restore32(model, iosversion)
    elif device == "iPad3":
        print("Looks like you are downgrading an iPad3 to 8.4.1!")
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
        restore32(model, iosversion)
    elif device == "iPad2":
        if "8.4.1" in versionManifest:
            print("Looks like you are downgrading an iPad2 to 8.4.1!")
            iosversion = "8.4.1"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
            restore32(model, iosversion)
        elif "6.1.3" in versionManifest:
            print("Looks like you are downgrading an iPad2 to 6.1.3!")
            iosversion = "6.1.3"
            shutil.copy(fname, "custom.ipsw")
            localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
            restore32(model, iosversion)
        else:
            exit(2)
    elif device == "iPod5":
        print("Looks like you are downgrading an iPod5 to 8.4.1!")
        iosversion = "8.4.1"
        shutil.copy(fname, "custom.ipsw")
        localdevice.enterkdfumode(kloaderlocation, kloaderlocation10, ibsslocation)
        restore32(model, iosversion)
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
    version = True
    versionManifest = readmanifest("IPSW/BuildManifest.plist", version)
    version = False
    deviceManifest = readmanifest("IPSW/BuildManifest.plist", version)

    if "iPhone" in deviceManifest and "10.3.3" in versionManifest:
        print("Looks like you are downgrading an iPhone 5s to 10.3.3!")
        bsdiff4.file_patch_inplace("iBEC.iphone6.RELEASE.im4p", phoneibec)
        bsdiff4.file_patch_inplace("iBSS.iphone6.RELEASE.im4p", phoneibss)
        device = "iPhone5s"

    elif "iPad" in deviceManifest and "10.3.3" in versionManifest:
        if devicemodel == "iPad4,1" or devicemodel == "iPad4,2" or devicemodel == "iPad4,3":
            print("Looks like you are downgrading an iPad Air to 10.3.3!")
            bsdiff4.file_patch_inplace("iBEC.ipad4.RELEASE.im4p", ipadairibec)
            bsdiff4.file_patch_inplace("iBSS.ipad4.RELEASE.im4p", ipadairibss)
            device = "iPadAir"

        elif devicemodel == "iPad4,4" or devicemodel == "iPad4,5":
            print("Looks like you are downgrading an iPad Mini 2 to 10.3.3!")
            bsdiff4.file_patch_inplace("iBEC.ipad4b.RELEASE.im4p", ipadminiibec)
            bsdiff4.file_patch_inplace("iBSS.ipad4b.RELEASE.im4p", ipadminiibss)
            device = "iPadMini"

        else:
            print("ERROR: Unknown input. Exiting purely because you can't read and that's sad...")
            print("ERROR: Exiting...")
            exit(1)

    else:
        print("Varible 'device' was not set. Please make sure IPSW file name is default/device is connected and try again")
        exit(55555)

    print("Patched iBSS/iBEC")
    print("About to re-build IPSW")

    if device == "iPhone5s":
        shutil.move("iBEC.iphone6.RELEASE.im4p", "IPSW/Firmware/dfu/")
        shutil.move("iBSS.iphone6.RELEASE.im4p", "IPSW/Firmware/dfu/")
        shutil.move("IPSW/Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/other/baseband.bbfw")

        if devicemodel == "iPhone6,1":
            shutil.move("IPSW/Firmware/all_flash/sep-firmware.n51.RELEASE.im4p", "resources/other/sep.im4p")
        elif devicemodel == "iPhone6,2":
            shutil.move("IPSW/Firmware/all_flash/sep-firmware.n53.RELEASE.im4p", "resources/other/sep.im4p")
        touch("IPSW/Firmware/usr/local/standalone/blankfile")

        with ZipFile('custom.ipsw', 'w') as zipObj2:
            os.chdir("IPSW")
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

            if os.path.exists("IPSW/custom.ipsw"):
                shutil.move("IPSW/custom.ipsw", "custom.ipsw")
            os.chdir("..")
        restore64(devicemodel)

    elif device == "iPadAir" or device == "iPadMini":
        if devicemodel == "iPad4,1" or devicemodel == "iPad4,2" or devicemodel == "iPad4,3":
            shutil.move("iBEC.ipad4.RELEASE.im4p", "IPSW/Firmware/dfu/")
            shutil.move("iBSS.ipad4.RELEASE.im4p", "IPSW/Firmware/dfu/")

            if devicemodel == "iPad4,1":
                shutil.move("IPSW/Firmware/all_flash/sep-firmware.j71.RELEASE.im4p", "resources/other/sep.im4p")
            elif devicemodel == "iPad4,2":
                shutil.move("IPSW/Firmware/all_flash/sep-firmware.j72.RELEASE.im4p", "resources/other/sep.im4p")
                shutil.move("IPSW/Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/other/baseband.bbfw")
            elif devicemodel == "iPad4,3":
                shutil.move("IPSW/Firmware/all_flash/sep-firmware.j73.RELEASE.im4p", "resources/other/sep.im4p")
                shutil.move("IPSW/Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/other/baseband.bbfw")

        elif devicemodel == "iPad4,4" or devicemodel == "iPad4,5":
            shutil.move("iBEC.ipad4b.RELEASE.im4p", "IPSW/Firmware/dfu/")
            shutil.move("iBSS.ipad4b.RELEASE.im4p", "IPSW/Firmware/dfu/")
            if devicemodel == "iPad4,4":
                shutil.move("IPSW/Firmware/all_flash/sep-firmware.j85.RELEASE.im4p", "resources/other/sep.im4p")
            elif devicemodel == "iPad4,5":
                shutil.move("IPSW/Firmware/all_flash/sep-firmware.j86.RELEASE.im4p", "resources/other/sep.im4p")
                shutil.move("IPSW/Firmware/Mav7Mav8-7.60.00.Release.bbfw", "resources/other/baseband.bbfw")
        touch("IPSW/Firmware/usr/local/standalone/blankfile")

        with ZipFile('custom.ipsw', 'w') as zipObj2:
            os.chdir("IPSW")
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

            os.chdir("..")

            if os.path.exists("IPSW/custom.ipsw"):
                shutil.move("IPSW/custom.ipsw", "custom.ipsw")
        restore64(devicemodel)
        
    else:
        print('\033[91m' + "something broke lmao" + '\033[0m')
        exit(1)
