import os
import subprocess
import shutil
import time
from resources.ipwndfu import checkm8, dfu
import device as localdevice

irecovery = "resources/bin/irecovery"
tsschecker = "resources/bin/tsschecker"
igetnonce = "resources/bin/igetnonce"

def removesig():
    cmd = 'python2.7 rmsigchks.py'
    so = os.popen(cmd).read()
    print(so)
    os.chdir("../..")


def pwndfumode():
    os.chdir("resources/ipwndfu")

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

def saveshsh(path, ecid, device, seperate):
    print("Getting SHSH...")\
    #ApNonce Collision list from https://twitter.com/dora2_yururi - https://github.com/dora2-iOS/Nudaoaddu/blob/master/get.sh
    nonceList = [
        '03011429dca6e0e1e71cc99716f27d94131d8128',
        '7d7bdc28e5eca36dc5bc20c791850f110dc28269',
        '1dedf288afea588e803be0737af7ae5ca87d107f',
        '6b83f831a6305ae90d57a78ba8eb9d81e7a9058f',
        'f5cce05e81a9be2ef66ec287f692ffdf20b13860',
        '7ce1657233867e988e1b48988ef98fc28ddf20f5',
        '74f5bbf201cbdcb8a145220fdcc6d82c3ce3a9d8',
        '72d41d45661d4108ab49a743701b4203862e1651',
        'b05a70468054cfe94251b34b58f28450054f1aa9',
        'ee4b7f9b2d7d41bfde4c8390734a83d63c2fe997',
        '47080312e71eda7ccd8eec33af095f41710fe8db',
        '8f760412c8653de657e8ea2352f706de2e9ca85c',
        '778282f0cf6e5234446d88ebc5dcfde81f415b57',
        '319c24a1e5adadb275b9be2fe82460d4ad068f92',
        '0f3b31015974dcc5ceb91c6883d6402621e5f1bb',
        '0a6b1027d0758d9f3699d8e40ce1189848190cc0',
        '93d5c7ba2844327ccb0a2a705fa8bb186021b459',
        '3f808110c6c0e2be97c087be8fa866012f3db5ab',
        'efd3060f847c13dbd79b955cc9761a76bb6b9653',
        '6b81a2c3cdf87404dee28330f7fcb0ee62c425a1',
        'b803b8b5bbb727ebcd70f705f1f03eb45ceeca08',
        '83265a110a03fe0d78649d6eefa5094389dcba65',
        'ec0ee58adb595a213910f3bcc495c2e5f6c7d608',
        '41234383e4311bca58b55807009f68c202d1a4f6',
        '16aeb5f04d3d74485d83a3a24db74c95e07ba2b9',
        'da218206498ff76001c8ae2e224713c293c5056c',
        '2890f2304faeb3ef156006b2ba5225d873ab1e9d',
        'd1c243d4e68964a383fe9804dc63d6a359cca4b6',
        'be6cd33cfe780486f604015abb9c0910c2a5f6c3',
        'ed85a1dfc3119de81f661508c3257705f265ecc2',
        '728a82a4bf7246939ea5db839ca782604cd97511',
        '8e33f9b17ca3ce754f5e7b4674ff796bc481302f',
        '8659875543cddd64b19873fe6e4b1cf811a2d18f',
        'a0d98fd69e122797ad6fb27376e83d982d321eff',
        'caadf840ba58ff6ca21d498e8f8496f7b0a33277',
        '4da8b62e458c5b5d280c238ad152ea232e5386f7',
        '99b5e22d771c0f1c81f70c394e9907993a2db435',
        'e750584ad5e9cefc403a03d9fe5d3b9cc46a3ac4',
        '4e7a5f87f93d32bb40f6c518726088c7e15997f5',
        '2a18e4781eab79bc8f5f5b0a0ab87a0215974ee8',
        '92658e2398b3aa22c7e8299ba6f78fc6fb3f84ed',
        '2570ffcb6fbf841ebebac999a4f3e7c220a71a2a',
        '1323f3979e87f71b8083fb98487fe3e744e1539a',
        'eeb59e528128a79ccb3903799f40d196f51d528d',
        '87d2ee06d87e4b81e415f57d6bbd84167b846352',
        'ccd8b14ceb4e66c7abf7e22625448b00f2e4b754',
        '99cdb2cc94047e80cf0e469aace151d3f819c417',
        '02a2b9a3c27d778d31c87d156060dbdd5d6baca4',
        '89a10fdaa35ef8fcd4f444bcef7e9c1031f489d0',
        '9440dad2b27ac1f7f626a7a11b3df13683721100',
        'ad51655059471fd0647599d091df98f73f59c2a8',
        'dc1879c6b0b065f037943871f27c1ecbc9e48b14',
        'aec09c7811dd02297b80251278608e67d913b74a',
        '6d943452cae56d76aace5e6da62da10f47769aa9',
        'ce610744ad24931c96d46b20f47d096b0b27487b',
        'fcd3d819cb3d2c2d043ccdbaeafe6d8938c3ac1d',
        'c067414bc17bc7d65dd036f56b81b522265ba79f',
        '42b39f38a9951c205df9d16bcece4422764f1cfd',
        '530783a50d36aea82628de2abb90920c3428918d',
        '831513e57eddad8652ae3addae987287a0047367',
        '198365e19ea223bd73ee27faa555ca24ac6ed65d',
        '76b3343a8cd2b25ff65dd493ea2bc18edea77be8',
        '1ff89bb136025233f089fa48708d7d217db70895',
        '0648939eac93a33ae5a9d6c4f5703f0baa2e68f3',
        '8b9244eba18e07f3ad9d5eed4f972aa98f0c495e',
        '63e81aabb8e9e45cc756c347e8cdfd9ae7c796ad',
        'a06f39ac30036a94e5d23954f010dbdeeadb8918',
        '994bf71da4fd4ba758a8ec6c943a5a610be02edb',
        'c1b22dd6b0531773fd8ae01ba2b72fda38b16cda',
        '21e0110ab8a9196aa851072e4aebf41571082612',
        '76e240fd1af3270e25f0b3c800ef1dbaf9d29de6',
        'f72dbc3917fc6d4234915c9f01e882086991ce44',
        'a7c5f8c66e72ed8481d7dc0bfc0363207c800cf9',
        'bc8e18c024cd4d130b4af0031b6fa80ab07bc43c',
        'abd8bfcfc3dcb4e8eabfdb57b30b6978e27bf819',
        '99a7b1ba5977d6c112717cc208a41785aaa7a313',
        '1166fc08241bbd4f26d495a892958c05d660a45f',
        '70bbffa807a66b2a1a3a017d233b0c9f874e6be3',
    ]

    if seperate: #If specified then setup the folder structure and iterate over the ApNonce list, saving SHSH for each ApNonce
        dir_name = os.getcwd()
        test = os.listdir(dir_name)
        if not str(path).endswith("/"):
            path = path + "/"
        if not str(path).endswith("10.3.3 OTA Blobs/"):
            path = path + "10.3.3 OTA Blobs/"
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        subfolder = device + " " + ecid + "/"
        subfolderpath = path + subfolder
        if os.path.exists(subfolderpath):
            print("You have already saved OTA Blobs for this device, you do not need to do this multiple times!\nExiting...")
            exit(222)
        else:
            os.mkdir(subfolderpath)


        for i in nonceList:
            if device != "iPad4,3":
                cmd = f'{tsschecker} -d {device} -i 10.3.3 -o -m resources/manifests/BuildManifest_{device}.plist -e {ecid} --apnonce {i} -s'
            else:
                cmd = f'{tsschecker} -d iPad4,3 --boardconfig j73AP -i 10.3.3 -o -m resources/manifests/BuildManifest_iPad4,3.plist -e {ecid} --apnonce {i} -s'
            so = subprocess.run(cmd, shell=True, stdout=open('errorlogshsh.txt', 'w'))
            returncode = so.returncode
            output = 'errorlogshsh.txt'

            if returncode != 0:
                with open(output, 'r') as fin:
                    print(fin.read())

                print("ERROR..\nReturn code:", returncode)
                print("SHSH Saving Failed.\nPlease try again and report the error/full logs and the 'errorlogshsh.txt' file if it persists.\nExiting...")
                exit(938862428)

            else:
                if os.path.exists('errorlogshsh.txt'):
                    os.remove('errorlogshsh.txt')
            dir_name = os.getcwd()
            test = os.listdir(dir_name)
            dest_name = subfolderpath + ecid + "." + device + '.10.3.3.' + i + ".shsh"
            for item in test:
                if item.endswith(".shsh"):
                    if os.path.exists(dest_name):
                        os.remove(dest_name)
                    shutil.move(os.path.join(dir_name, item), dest_name)
        return path
    else:
        nonce = localdevice.getapnonce()
        if device != "iPad4,3":
            cmd = f'{tsschecker} -d {device} -i 10.3.3 -o -m resources/manifests/BuildManifest_{device}.plist -e {ecid} --apnonce {nonce} -s'
        else:
            cmd = f'{tsschecker} -d iPad4,3 --boardconfig j73AP -i 10.3.3 -o -m resources/manifests/BuildManifest_iPad4,3.plist -e {ecid} --apnonce {nonce} -s'

        so = subprocess.run(cmd, shell=True, stdout=open('errorlogshsh.txt', 'w'))
        returncode = so.returncode
        output = 'errorlogshsh.txt'

        if returncode != 0:
            with open(output, 'r') as fin:
                print(fin.read())

            print("ERROR..\nReturn code:", returncode)
            print("SHSH Saving Failed.\nPlease try again and report the error/full logs and the 'errorlogshsh.txt' file if it persists.\nExiting...")
            exit(938862428)

        else:
            if os.path.exists('errorlogshsh.txt'):
                os.remove('errorlogshsh.txt')

        dir_name = os.getcwd()
        test = os.listdir(dir_name)
        if not str(path).endswith("/"):
            path = path + "/"
        dest_name = path + "apnonce.shsh"

        for item in test:
            if item.endswith(".shsh"):
                if os.path.exists(dest_name):
                    os.remove(dest_name)
                shutil.move(os.path.join(dir_name, item), dest_name)
        return dest_name

def restore32(device, iosversion):

    print("Getting SHSH...")
    ecid = localdevice.getecid()
    device32 = str(localdevice.getmodel())
    if iosversion == "6.1.3":
        cmd = f'{tsschecker} -d {device32} -i {iosversion} -o -m resources/manifests/BuildManifest613_{device32}.plist -e {ecid} -s'
    else:
        cmd = f'{tsschecker} -d {device32} -i {iosversion} -o -m resources/manifests/BuildManifest_{device32}.plist -e {ecid} -s'

    so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    returncode = so.returncode

    if returncode != 0:
        print(
            "Saving SHSH failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
        exit(938862428)

    dir_name = os.getcwd()
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".shsh2"):
            shutil.move(os.path.join(dir_name, item), "resources/other/apnonce.shsh")

    print("Restoring...")
    print('\033[91m' + "Note that errors about 'BbSkeyId', 'FDR Client', 'BasebandFirmware Node' and 'ERROR: zip_name_locate: Firmware/all_flash/manifest' are not important.\nJust ignore them and only report errors that actually stop the restore." + '\033[0m')
    futurerestore  = "resources/bin/futurerestore"
    if device32 == "iPad2,1" or device32 == "iPad2,4" or device32 == "iPad2,5" or device32 == "iPad3,1" or device32 == "iPad3,4" or device32 == "iPod5,1":
        cmd2 = f'{futurerestore} -t resources/other/apnonce.shsh --no-baseband --use-pwndfu custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=open('errorlogrestore.txt', 'w'))
        returncode = so2.returncode
        output = 'errorlogrestore.txt'

        if returncode != 0:
            with open(output, 'r') as fin:
                print(fin.read())
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error/send me the full logs and the 'errorlogrestore.txt' file if it persists\nExiting...")
            exit(938862428)

        else:
            if os.path.exists('errorlogrestore.txt'):
                os.remove('errorlogrestore.txt')

    else:
        cmd2 = f'{futurerestore} -t resources/other/apnonce.shsh --use-pwndfu --latest-baseband custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=open('errorlogrestore.txt', 'w'))
        returncode = so2.returncode
        output = 'errorlogrestore.txt'

        if returncode != 0:
            with open(output, 'r') as fin:
                print(fin.read())
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error/send me the full logs and the 'errorlogrestore.txt' file if it persists\nExiting...")
            exit(938862428)

        else:
            if os.path.exists('errorlogrestore.txt'):
                os.remove('errorlogrestore.txt')


def restore64(device):

    print("Entering PWNREC mode...")
    ecid = localdevice.getecid()
    os.chdir("IPSW/Firmware/dfu")
    irecerr = "Sending iBSS/iBEC Failed.\nPlease reboot device, start the tool again and report the error + full logs if it persists.\nExiting..."
    #irecovery needs to have the image thats being sent in the current work directory, irecovery binary can be anywhere
    if device == "iPhone6,2" or device == "iPhone6,1":
        cmd = '../../../resources/bin/irecovery -f iBSS.iphone6.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)
        time.sleep(5)
        cmd = '../../../resources/bin/irecovery -f iBEC.iphone6.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)

    elif device == "iPad4,1" or device == "iPad4,2" or device == "iPad4,3":
        cmd = '../../../resources/bin/irecovery -f iBSS.ipad4.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)

        cmd = '../../../resources/bin/irecovery -f iBEC.ipad4.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)

    elif device == "iPad4,4" or device == "iPad4,5":
        cmd = '../../../resources/bin/irecovery -f iBSS.ipad4b.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)

        cmd = '../../../resources/bin/irecovery -f iBEC.ipad4b.RELEASE.im4p'
        so = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        returncode = so.returncode

        if returncode != 0:
            print("ERROR..\nReturn code:", returncode)
            print(irecerr)
            exit(938862428)

    else:
        print('\033[91m' + "Somehow you made it here with an invalid device, nice work! Please tell me how @mosk_i" + '\033[0m')
        exit(5)

    os.chdir("../../..")
    time.sleep(5)
    seperate = False
    saveshsh("resources/other", ecid, device, seperate)
    time.sleep(3)
    print("Restoring...")
    print('\033[91m' + "Note that errors about 'BbSkeyId', 'FDR Client', 'BasebandFirmware Node' and 'ERROR: zip_name_locate: Firmware/all_flash/manifest' are not important.\nJust ignore them and only report errors that actually stop the restore." + '\033[0m')
    futurerestore  = "resources/bin/futurerestore"
    if device == "iPad4,1" or device == "iPad4,4":
        
        print(f"Restoring without a baseband as your {device} doesn't have cellular capabilities...")
        cmd2 = f'{futurerestore} -t resources/other/apnonce.shsh -s resources/other/sep.im4p -m resources/manifests/BuildManifest_{device}.plist --no-baseband custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=open('errorlogrestore.txt', 'w'))
        returncode = so2.returncode
        output = 'errorlogrestore.txt'

        if returncode != 0:
            with open(output, 'r') as fin:
                print(fin.read())
                
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error + full logs if it persists.\nExiting...")
            exit(938862428)

    else:

        cmd2 = f'{futurerestore} -t resources/other/apnonce.shsh -s resources/other/sep.im4p -m resources/manifests/BuildManifest_{device}.plist -b resources/other/baseband.bbfw -p resources/manifests/BuildManifest_{device}.plist custom.ipsw'
        so2 = subprocess.run(cmd2, shell=True, stdout=open('errorlogrestore.txt', 'w'))
        returncode = so2.returncode
        output = 'errorlogrestore.txt'

        if returncode != 0:
            with open(output, 'r') as fin:
                print(fin.read())
            print("ERROR..\nReturn code:", returncode)
            print("Restore Failed.\nPlease try again and report the error/send me the full logs and the 'errorlogrestore.txt' file if it persists\nExiting...")
            exit(938862428)

        else:
            if os.path.exists('errorlogrestore.txt'):
                os.remove('errorlogrestore.txt')