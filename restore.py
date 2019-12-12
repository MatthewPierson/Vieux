import os
import subprocess
import shutil
import time
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
        print('\033[91m' + "You need to have your 32 Bit device in normal mode, not DFU. Restart it and try again" + '\033[0m')
        exit(2)

    else:
        print('Found:', serial_number)
        print('\033[91m' + 'ERROR: This device is not supported.' + '\033[0m')
        exit(1)

def restore32(device, iosversion):
    if os.path.exists("restoreFiles/futurerestore"):
        shutil.move("restoreFiles/futurerestore", "futurerestore")
    elif os.path.exists("restoreFiles/igetnonce"):
        shutil.move("restoreFiles/igetnonce", "igetnonce")
    elif os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    elif os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print("Getting SHSH...")
    ecid = localdevice.getecid()
    device32 = str(localdevice.getmodel())
    cmd = f'./tsschecker -d {device32} -i {iosversion} -o -m restoreFiles/BuildManifest_{device32}.plist -e {ecid} -s'
    so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    returncode = so.returncode
    if returncode != 0:
        print(
            "Resoting Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
        exit(938862428)
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".shsh2"):
            shutil.move(os.path.join(dir_name, item), "restoreFiles/apnonce.shsh")
    print("Restoring...")
    print('\033[91m' + "Note that errors about 'BbSkeyId', 'FDR Client' and 'BasebandFirmware Node' are not important, just ignore them and only report errors that actually stop the restore." + '\033[0m')
    if device32 != "iPad2,1" or "iPad2,4" or "iPad2,5" or "iPad3,1" or "iPad3,4" or "iPod5,1":
        cmd2 = './futurerestore -t restoreFiles/apnonce.shsh --use-pwndfu --latest-baseband custom.ipsw'
        so = subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("Resoting Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
            exit(938862428)
    else:
        cmd2 = './futurerestore -t restoreFiles/apnonce.shsh --no-baseband --use-pwndfu custom.ipsw'
        so = subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        print(returncode)
        if returncode != 0:
            print("Resoting Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
            exit(938862428)

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
    irecerr = "Sending iBSS/iBEC Failed.\nPlease try again and report the error + full logs if it persists.\nExiting..."
    if device == "iPhone6,2" or device == "iPhone6,1":
        cmd = '../../irecovery -f iBSS.iphone6.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
        time.sleep(5)
        cmd = '../../irecovery -f iBEC.iphone6.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
    elif device == "iPad4,1" or device == "iPad4,2" or device == "iPad4,3":
        cmd = '../../irecovery -f iBSS.ipad4.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
        cmd = '../../irecovery -f iBEC.ipad4.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
    elif device == "iPad4,4" or device == "iPad4,5":
        cmd = '../../irecovery -f iBSS.ipad4b.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
        cmd = '../../irecovery -f iBEC.ipad4b.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
    else:
        print('\033[91m' + "Broke" + '\033[0m')
        exit(5)
    os.chdir("../..")
    time.sleep(5)
    print("Getting SHSH...")
    nonce = localdevice.getapnonce()
    if device != "iPad4,3":
        cmd = f'./tsschecker -d {device} -i 10.3.3 -o -m restoreFiles/BuildManifest_{device}.plist -e {ecid} --apnonce {nonce} -s'
    else:
        cmd = f'./tsschecker -d iPad4,3 --boardconfig j73AP -i 10.3.3 -o -m restoreFiles/BuildManifest_iPad4,3.plist -e {ecid} --apnonce {nonce} -s'
    so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    returncode = so.returncode
    if returncode != 0:
        print("ERROR..\nReturn code:", returncode)
        print("SHSH Saving Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
        exit(938862428)
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".shsh"):
            shutil.move(os.path.join(dir_name, item), "restoreFiles/apnonce.shsh")
    time.sleep(3)
    print("Restoring...")
    print('\033[91m' + "Note that errors about 'BbSkeyId', 'FDR Client' and 'BasebandFirmware Node' are not important, just ignore them and only report errors that actually stop the restore." + '\033[0m')
    if device != "iPad4,1" or "iPad4,4":
        cmd2 = f'./futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_{device}.plist -b restoreFiles/baseband.bbfw -p restoreFiles/BuildManifest_{device}.plist custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL)
        returncode = so2.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
            exit(938862428)
    else:
        cmd2 = f'./futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_{device}.plist --no-baseband custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL)
        returncode = so2.returncode
        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
            exit(938862428)