import os, sys, shutil
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
            print("Exploit failed =(")
            exit(99)
    elif 'CPID:8965' in serial_number:
        runexploit = checkm8.exploit()
        if runexploit:
            print("Exploit worked!")
            removesig()
        else:
            print("Exploit failed =(")
            exit(99)
    else:
        print('Found:', serial_number)
        print('ERROR: This device is not supported.')
        sys.exit(1)

def restore32(device):
    print("still tired")
    if os.path.exists("restoreFiles/futurerestore"):
        shutil.move("restoreFiles/futurerestore", "futurerestore")
    if os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    if os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print("Entering PWNREC mode...")
    if device == "iPhone5,2":
        cmd = 'irecovery -f iBSS.n42.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.n42.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
    elif device == "iPhone5,1":
        cmd = 'irecovery -f iBSS.n41.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.n41.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
    elif device == "iPhone4,1":
        cmd = 'irecovery -f iBSS.n94.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.n94.RELEASE.dfu'
        so = os.popen(cmd).read()
        print(so)
    else:
        print("Broke")
        exit(5)
    print("Getting SHSH...")

    #cmd = 'tsschecker -d iPhone6,2 -i 10.3.3 -o -m restoreFiles/BuildManifest_iPhone6,2_1033_OTA.plist -e 376AE36B764 --apnonce "nonce" -s --save-path restoreFiles/apnonce.shsh'
    #so = os.popen(cmd).read()
    #print(so)
    print("Restoring...")
    if os.path.exists("restoreFiles/baseband.bbfw"):
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh --latest-baseband custom.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)
    else:
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh --no-baseband custom.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)

def restore64(device):
    if os.path.exists("restoreFiles/futurerestore"):
        shutil.move("restoreFiles/futurerestore", "futurerestore")
    if os.path.exists("restoreFiles/tsschecker"):
        shutil.move("restoreFiles/tsschecker", "tsschecker")
    if os.path.exists("restoreFiles/irecovery"):
        shutil.move("restoreFiles/irecovery", "irecovery")
    print("Entering PWNREC mode...")
    if device == "iPhone6,2" or device == "iPhone6,1":
        cmd = 'irecovery -f iBSS.iphone6.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.iphone6.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
    elif device == "iPad4,1" or device == "iPad4,2" or device == "iPad4,3":
        cmd = 'irecovery -f iBSS.ipad4.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.ipad4.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
    elif device == "iPad4,4" or device == "iPad4,5":
        cmd = 'irecovery -f iBSS.ipad4b.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
        cmd = 'irecovery -f iBEC.ipad4b.RELEASE.im4p'
        so = os.popen(cmd).read()
        print(so)
    else:
        print("Broke")
        exit(5)
    print("Getting SHSH...")
    ecid = localdevice.getecid()
    nonce = localdevice.getapnonce()
    cmd = f'tsschecker -d {device} -i 10.3.3 -o -m restoreFiles/BuildManifest_{device}.plist -e {ecid} --apnonce {nonce} -s'
    so = os.popen(cmd).read()
    print(so)
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".shsh"):
            shutil.move(os.path.join(dir_name, item), "restoreFiles/apnonce.shsh")
    jebait = input("Press enter when you've saved apnonce stuff =)")
    print("Restoring...")
    if os.path.exists("restoreFiles/baseband.bbfw"):
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_iPhone6,2.plist -b restoreFiles/baseband.bbfw -p restoreFiles/BuildManifest_iPhone6,2.plist custom.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)
    else:
        cmd2 = 'futurerestore -t restoreFiles/apnonce.shsh -s restoreFiles/sep.im4p -m restoreFiles/BuildManifest_iPhone6,2.plist --no-baseband custom.ipsw'
        so2 = os.popen(cmd2).read()
        print(so2)