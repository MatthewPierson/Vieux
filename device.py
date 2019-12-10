from ipwndfu import dfu
import re
import os
import main
import time
import paramiko
import socket
import getpass
from scp import SCPClient


def getecid():
    device = dfu.acquire_device()
    serial = device.serial_number
    with main.silence_stdout():
        print(serial)

    try:
        found = re.search('ECID:(.+?) IBFL', serial).group(1)
        print("Your ECID is :", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't find ECID in serial" + '\033[0m')


def getapnonce():
    print("Getting current ApNonce from device...")
    cmd = './igetnonce'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)
    try:

        found = re.search('ApNonce=(.+?)\nSep', so).group(1)
        print("Your current ApNonce is :", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't get ApNonce from device" + '\033[0m')

def getmodel():
    print("Getting device model...")
    cmd = './igetnonce'
    so = os.popen(cmd).read()
    with main.silence_stdout():
        print(so)
    try:
        found = re.search(', (.+?) in DFU mode', so).group(1)
        print("Your device is an ", found)
        return found
    except AttributeError:
        print('\033[91m' + "ERROR: Couldn't get device model information" + '\033[0m')



def enterkdfumode(kloader, kloader10, ibss):
    print("Connecting to device via SSH...")
    ip = input("Please enter your devices IP address (Find it in WiFi settings):\n")

    try:
        socket.inet_aton(ip)
    except:
        print("ERROR: Invalid IP address...")
        a = ip
        while not a.startswith("b'"):
            ip = input("Please enter a valid IP Address...")
            try:
                socket.inet_aton(ip)
            except:
                print("")
        else:
            print("")
    if ip.count(".") != 3:
        print("ERROR: Invalid IP address...")
        b = ip.count(".")
        while b != 3:
            ip = input("Please enter a valid IP Address...")
            b = ip.count(".")
            print(b)
        else:
            print("")

    devicepassword = getpass.getpass("Please enter the root password to your device (Default is 'alpine'):\n")

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        client.connect(hostname=ip, password=devicepassword, username="root")
        command = "uname -r"
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read(),
        scp = SCPClient(client.get_transport())
        finalresult = str(result)
        with main.silence_stdout():
            print(finalresult)
        scp.put(ibss, '/')
        if finalresult.startswith("(b'16"):
            print("Device is running iOS 10.x, using HGSP4 kloader...")
            scp.put(kloader10, '/')
            command2 = "/kloader10 /ibss > /dev/null 2>&1 &"
        else:
            print('Device is not running iOS 10.x, using normal TFP0 kloader...')
            scp.put(kloader, '/')
            command2 = "/kloader /ibss > /dev/null 2>&1 &"
        stdin, stdout, stderr = client.exec_command(command2)
        result2 = stdout.read(),
        with main.silence_stdout():
            print(result2)
        scp.close()
        client.close()
        print("Please press the home button on your device or unplug and replug it back in.\nWaiting 10 seconds for you to do this.")
        time.sleep(10)
    except:
        print("broke")
