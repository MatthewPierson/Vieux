import os, shutil, bsdiff4
from pathlib import Path
from zipfile import ZipFile
from main import removeFiles, pick3264
from restore import restore64, restore32


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def unzipIPSW():
    fname = input("Enter the path to the zip file:\n")
    print("Starting IPSW unzipping")
    outputFolder = os.getcwd()
    testFile = os.path.exists(fname)

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

        pick3264(fname)

    else:
        print("ERROR: Not valid filepath...")
        print("ERROR: Exiting...")
        exit(1)

def createCustomIPSW32(fname):
    print("Starting iBSS/iBEC patching")
    patch_folder = Path("patches/")
    phone5ibec = patch_folder / "make them"
    phone5ibss = patch_folder / "make them"
    phone4sibec = patch_folder / "make them"
    phone4sibss = patch_folder / "make them"
    if "iPhone5,2" in fname or "iPhone5,1" in fname and "8.4.1" in fname:
        print("Looks like you are downgrading an iPhone 5 to 8.4.1 using OTA blobs!")
        bsdiff4.file_patch_inplace("iBEC.n42.RELEASE.dfu", phone5ibec)
        bsdiff4.file_patch_inplace("iBSS.n42.RELEASE.dfu", phone5ibss)
        device = "iPhone5"
    elif "6.1.3" in fname or "8.4.1" in fname and "iPhone4,1" in fname:
        print("Looks like you are downgrading an iPhone 4s using OTA blobs!")
        bsdiff4.file_patch_inplace("make them", phone4sibec)
        bsdiff4.file_patch_inplace("make them", phone4sibss)
        device = "iPhone4s"
    else:
        print("Im tired")
        exit(24)

    if device == "iPhone5":
        deviceSpecific = input("Which model of iPhone do you have? (iPhone5,1 or iPhone5,2)...\n")
        shutil.move("iBEC.n42.RELEASE.dfu", "Firmware/dfu/")
        shutil.move("iBSS.n42.RELEASE.dfu", "Firmware/dfu/")
        shutil.copy("Firmware/Mav5-8.02.00.Release.bbfw", "restoreFiles/baseband.bbfw")
        touch("Firmware/usr/local/standalone/blankfile")
        with ZipFile('custom.ipsw', 'w') as zipObj2:
            zipObj2.write('Restore.plist')
            zipObj2.write('kernelcache.release.n42')
            zipObj2.write('BuildManifest.plist')
            zipObj2.write('058-24110-023.dmg')
            zipObj2.write('058-24024-023.dmg')
            zipObj2.write('058-23947-023.dmg')
            for folderName, subfolders, filenames in os.walk("Firmware"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj2.write(filePath)
        restore32(deviceSpecific)
    elif device == "iPhone4s":
        if "8.4.1" in fname:
            deviceSpecific = "iPhone4,1"
            shutil.move("iBEC.n94.RELEASE.dfu", "Firmware/dfu/")
            shutil.move("iBSS.n94.RELEASE.dfu", "Firmware/dfu/")
            shutil.copy("Firmware/Trek-5.5.00.Release.bbfw", "restoreFiles/baseband.bbfw")
            touch("Firmware/usr/local/standalone/blankfile")
            with ZipFile('custom.ipsw', 'w') as zipObj2:
                zipObj2.write('Restore.plist')
                zipObj2.write('kernelcache.release.n94')
                zipObj2.write('BuildManifest.plist')
                zipObj2.write('058-24033-023.dmg')
                zipObj2.write('058-24104-023.dmg')
                zipObj2.write('058-24341-023.dmg')
                for folderName, subfolders, filenames in os.walk("Firmware"):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj2.write(filePath)
            restore32(deviceSpecific)
        elif "6.1.3" in fname:
            deviceSpecific = "iPhone4,1"
            shutil.move("iBEC.n94ap.RELEASE.dfu", "Firmware/dfu/")
            shutil.move("iBSS.n94ap.RELEASE.dfu", "Firmware/dfu/")
            shutil.copy("Firmware/Trek-3.4.03.Release.bbfw", "restoreFiles/baseband.bbfw")
            touch("Firmware/usr/local/standalone/blankfile")
            with ZipFile('custom.ipsw', 'w') as zipObj2:
                zipObj2.write('Restore.plist')
                zipObj2.write('kernelcache.release.n94')
                zipObj2.write('BuildManifest.plist')
                zipObj2.write('048-2516-005.dmg')
                zipObj2.write('048-2613-005.dmg')
                zipObj2.write('048-2679-005.dmg')
                for folderName, subfolders, filenames in os.walk("Firmware"):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj2.write(filePath)
            restore32(deviceSpecific)
def createCustomIPSW64(fname, devicemodel):
    print("Starting iBSS/iBEC patching")
    patch_folder = Path("patches/")
    phoneibec = patch_folder / "ibec5s.patch"
    phoneibss = patch_folder / "ibss5s.patch"
    ipadminiibec = patch_folder / "ibec_ipad4b.patch"
    ipadminiibss = patch_folder / "ibss_ipad4b.patch"
    ipadairibec = patch_folder / "ibec_ipad4.patch"
    ipadairibss = patch_folder / "ibss_ipad4.patch"
    if "iPhone" in fname and "10.3.3" in fname:
        print("Looks like you are downgrading an iPhone 5s to 10.3.3 using OTA blobs!")
        bsdiff4.file_patch_inplace("iBEC.iphone6.RELEASE.im4p", phoneibec)
        bsdiff4.file_patch_inplace("iBSS.iphone6.RELEASE.im4p", phoneibss)
        device = "iPhone5s"
    elif "iPad" in fname and "10.3.3" in fname:
        if devicemodel == "iPad4,1" or devicemodel == "iPad4,2" or devicemodel == "iPad4,3":
            print("Looks like you are downgrading an iPad Air!")
            bsdiff4.file_patch_inplace("iBEC.ipad4.RELEASE.im4p ", ipadairibec)
            bsdiff4.file_patch_inplace("iBSS.ipad4.RELEASE.im4p", ipadairibss)
            device = "iPadAir"
        elif devicemodel == "iPad4,4" or devicemodel == "iPad4,5":
            print("Looks like you are downgrading an iPad Mini 2!")
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
        deviceSpecific = devicemodel
        shutil.move("iBEC.iphone6.RELEASE.im4p", "Firmware/dfu/")
        shutil.move("iBSS.iphone6.RELEASE.im4p", "Firmware/dfu/")
        shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "restoreFiles/baseband.bbfw")
        shutil.move("Firmware/all_flash/sep-firmware.n53.RELEASE.im4p", "restoreFiles/sep.im4p")
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
        restore64(deviceSpecific)

    elif device == "iPadAir" or device == "iPadMini":
        deviceSpecific = devicemodel
        if deviceSpecific == "iPad4,1" or deviceSpecific == "iPad4,2" or deviceSpecific == "iPad4,3":
            shutil.move("iBEC.ipad4.RELEASE.im4p", "Firmware/dfu/")
            shutil.move("iBSS.ipad4.RELEASE.im4p", "Firmware/dfu/")
            if deviceSpecific == "iPad4,1":
                shutil.move("Firmware/all_flash/sep-firmware.j71.RELEASE.im4p", "restoreFiles/sep.im4p")
            if deviceSpecific == "iPad4,2":
                shutil.move("Firmware/all_flash/sep-firmware.j72.RELEASE.im4p", "restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "restoreFiles/baseband.bbfw")
            if deviceSpecific == "iPad4,3":
                shutil.move("Firmware/all_flash/sep-firmware.j73.RELEASE.im4p", "restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "restoreFiles/baseband.bbfw")
        if deviceSpecific == "iPad4,4" or deviceSpecific == "iPad4,5":
            shutil.move("iBEC.ipad4b.RELEASE.im4p", "Firmware/dfu/")
            shutil.move("iBSS.ipad4b.RELEASE.im4p", "Firmware/dfu/")
            if deviceSpecific == "iPad4,4":
                shutil.move("Firmware/all_flash/sep-firmware.j85.RELEASE.im4p", "restoreFiles/sep.im4p")
            if deviceSpecific == "iPad4,5":
                shutil.move("Firmware/all_flash/sep-firmware.j86.RELEASE.im4p", "restoreFiles/sep.im4p")
                shutil.move("Firmware/Mav7Mav8-7.60.00.Release.bbfw", "restoreFiles/baseband.bbfw")
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
        restore64(deviceSpecific)
    else:
        print("something broke lmao")
        exit(1)
