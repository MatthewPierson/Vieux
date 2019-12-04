import os
import shutil
import time
import main
from ipwndfu import dfu, checkm8
import device as localdevice

def removesig():
    os.chdir("../removesig")

    cmd = 'python rmsigchks.py'
    so = os.popen(cmd).read()
    print(so)
    
    os.chdir("..")

def pwndfumode():
    os.chdir("ipwndfu")
    
    device = dfu.acquire_device()
    serial_number = device.serial_number
    dfu.release_device(device)

    if 'CPID:8960' in serial_number:
        runexploit = checkm8.exploit()
        if runexploit:
            print("Exploit worked!")
            removesig()
        else:
            print('\033[91m' + "Exploit failed =(" + '\033[0m')
            exit(99)
    elif 'CPID:8965' in serial_number:
        runexploit = checkm8.exploit()
        if runexploit:
            print("Exploit worked!")
            removesig()
        else:
            print('\033[91m' + "Exploit failed =(" + '\033[0m')
            exit(99)
    elif 'CPID:8950' in serial_number:
        print("iPhone 5 found!")
        os.chdir("..")
        print('\033[91m' + "32 Bit support is still WIP, shouldn't be hard to get it working :)" + '\033[0m')
        exit(69)
    else:
        print('Found:', serial_number)
        print('\033[91m' + 'ERROR: This device is not supported.' + '\033[0m')
        exit(1)

def restore32(device):
    print("still tired")
    if os.path.exists("restoreFiles/futurerestore"):
        shutil.move("restoreFiles/futurerestore", "futurerestore")
    elif os.path.exists("restoreFiles/igetnonce"):
        shutil.move("restoreFiles/igetnonce", "igetnonce")
    elif os.path.exists("restoreFiles/idevicerestore"):
        shutil.move("restoreFiles/idevicerestore", "idevicerestore")
    elif os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    elif os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print("Entering PWNREC mode...")
    os.chdir("Firmware/dfu")
    if device == "iPhone5,2":
        print("iPhonr 5 =)")
        cmd = '../../irecovery -f iBSS.n42.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        cmd = '../../irecovery -f iBEC.n42.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    elif device == "iPhone5,1":
        cmd = '../../irecovery -f iBSS.n41.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        cmd = '../../irecovery -f iBEC.n41.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    elif device == "iPhone4,1":
        cmd = '../../irecovery -f iBSS.n94.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        cmd = '../../irecovery -f iBEC.n94.RELEASE.dfu'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    else:
        print('\033[91m' + "Broke" + '\033[0m')
        exit(5)
    os.chdir("../..")
    print("Getting SHSH...")

    cmd = 'tsschecker -d iPhone6,2 -i 10.3.3 -o -m restoreFiles/BuildManifest_iPhone6,2_1033_OTA.plist -e 376AE36B764 --apnonce "nonce" -s --save-path restoreFiles/apnonce.shsh'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)
    print("Restoring...")
    if os.path.exists("restoreFiles/baseband.bbfw"):
        cmd2 = './idevicerestore -e -c custom2.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)
    else:
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh --no-baseband custom.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)

def restore64(device):
    if os.path.exists("restoreFiles/futurerestore"):
        shutil.move("restoreFiles/futurerestore", "futurerestore")
    if os.path.exists("restoreFiles/igetnonce"):
        shutil.move("restoreFiles/igetnonce", "igetnonce")
    if os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    if os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print("Entering PWNREC mode...")
    ecid = localdevice.getecid()
    os.chdir("Firmware/dfu")
    if device == "iPhone6,2" or device == "iPhone6,1":
        cmd = '../../irecovery -f iBSS.iphone6.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        time.sleep(5)
        cmd = '../../irecovery -f iBEC.iphone6.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    elif device == "iPad4,1" or device == "iPad4,2" or device == "iPad4,3":
        cmd = '../../irecovery -f iBSS.ipad4.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        cmd = '../../irecovery -f iBEC.ipad4.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    elif device == "iPad4,4" or device == "iPad4,5":
        cmd = '../../irecovery -f iBSS.ipad4b.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
        cmd = '../../irecovery -f iBEC.ipad4b.RELEASE.im4p'
        so = os.popen(cmd).read()
        with main.silence_stdout():
            print(so)
    else:
        print('\033[91m' + "Broke" + '\033[0m')
        exit(5)
    os.chdir("../..")
    time.sleep(5)
    print("Getting SHSH...")
    nonce = localdevice.getapnonce()
    cmd = f'tsschecker -d {device} -i 10.3.3 -o -m restoreFiles/BuildManifest_{device}.plist -e {ecid} --apnonce {nonce} -s'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".shsh"):
            shutil.move(os.path.join(dir_name, item), "restoreFiles/apnonce.shsh")
    time.sleep(3)
    print("Restoring...")
    if os.path.exists("restoreFiles/baseband.bbfw"):
        cmd2 = f'futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_{device}.plist -b restoreFiles/baseband.bbfw -p restoreFiles/BuildManifest_{device}.plist custom.ipsw'
        so2 = os.popen(cmd2).read()
        with main.silence_stdout():
            print(so2)
    else:
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_iPhone6,2.plist --no-baseband custom.ipsw'
        so2 = os.popen(cmd2).read()
        with main.silence_stdout():
            print(so2)
