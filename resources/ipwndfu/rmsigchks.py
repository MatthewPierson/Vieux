import dfu2 as dfu
import usbexec2 as usbexec
import sys
import usb.core

HOST2DEVICE = 0x21
DEVICE2HOST = 0xA1

DFU_DNLOAD = 1
DFU_ABORT = 4

class DeviceConfig:
    def __init__(self, version, cpid, patches):
        self.version = version
        self.cpid    = cpid
        self.patches = patches

def all_exploit_configs():
    s5l8965x_patches = {
        0x1000054e4: "\x1f\x20\x03\xd5",
        0x1000054b4: b"".join([
            b"\x21\x00\x80\x52", # mov w1, 1
            b"\xe1\x9f\x02\x39", # strb w1, [sp,#0xA7]
            b"\x1f\x20\x03\xd5", # nop
            b"\xe1\xa7\x02\x39", # strb w1, [sp,#0xA9]
            b"\xe1\xab\x02\x39", # strb w1, [sp,#0xAA]
            b"\x1f\x20\x03\xd5", # nop
            b"\x1f\x20\x03\xd5", # nop
            b"\x1f\x20\x03\xd5", # nop
            b"\x1f\x20\x03\xd5", # nop
        ])
    }
    s5l8960x_patches = {
        0x1000054e4: "\x1f\x20\x03\xd5",
        0x1000054b4: b"".join([
                               b"\x21\x00\x80\x52", # mov w1, 1
                               b"\xe1\x9f\x02\x39", # strb w1, [sp,#0xA7]
                               b"\x1f\x20\x03\xd5", # nop
                               b"\xe1\xa7\x02\x39", # strb w1, [sp,#0xA9]
                               b"\xe1\xab\x02\x39", # strb w1, [sp,#0xAA]
                               b"\x1f\x20\x03\xd5", # nop
                               b"\x1f\x20\x03\xd5", # nop
                               b"\x1f\x20\x03\xd5", # nop
                               b"\x1f\x20\x03\xd5", # nop
                               ])
    }
    t8010_patches = {
        0x100006C80: "\x21\x00\x80\x52\xe1\xe3\x03\x39\xe1\xef\x03\x39\xe1\xf7\x03\x39\xe1\xeb\x03\x39\xe1\xf3\x03\x39\xe1\xfb\x03\x39",
        0x100006ca0: "\x1f\x20\x03\xd5", # nop
        0x100006ca4: "\x1f\x20\x03\xd5", # nop
        0x100006ca8: "\x1f\x20\x03\xd5", # nop
        0x10000f1b0: "\x00\x00\x80\xd2\xc0\x03\x5f\xd6"
    }

    t8011_patches = {
        0x100006df8: "\x21\x00\x80\x52\xe1\xb7\x03\x39\xe1\xb3\x03\x39\xe1\xbb\x03\x39",
        0x100006e0c: "\x1f\x20\x03\xd5", # nop
        0x100006e10: "\x1f\x20\x03\xd5", # nop
        0x100006e14: "\x1f\x20\x03\xd5", # nop
        0x10000f2d0: "\x00\x00\x80\xd2\xc0\x03\x5f\xd6"
    }

    return [
        DeviceConfig("iBoot-1704.10", 0x8960, s5l8965x_patches),
        DeviceConfig("iBoot-1704.10", 0x8960, s5l8960x_patches),
        DeviceConfig("iBoot-2696.0.0.1.33", 0x8010, t8010_patches),
        DeviceConfig("iBoot-3135.0.0.2.3", 0x8011, t8011_patches),
    ]

def exploit_config(serial_number):
    for config in all_exploit_configs():
        if "SRTG:[%s]" % config.version in serial_number:
            return config
    for config in all_exploit_configs():
        if "CPID:%s" % config.cpid in serial_number:
            print "ERROR: CPID is compatible, but serial number string does not match."
            print "Make sure device is in SecureROM DFU Mode and not LLB/iBSS DFU Mode. Exiting."
            sys.exit(1)
    print "ERROR: This is not a compatible device. Exiting."
    print "Right now, only the iPhone 5s is compatible."
    sys.exit(1)

def main():
    print "*** SecureROM Signature check remover by Linus Henze ***"
    device = dfu.acquire_device()
    #print "Found:", device.serial_number
    if not "PWND:[" in device.serial_number:
        print "Please enable pwned DFU Mode first."
        sys.exit(1)
    if not "PWND:[checkm8]" in device.serial_number:
        print "Only devices pwned using checkm8 are supported."
        sys.exit(1)
    config = exploit_config(device.serial_number)
    print "Applying patches..."
    try:
        pdev = usbexec.PwnedUSBDevice()
    except usb.core.USBError:
        print "Patches have already been applied. Exiting."
        sys.exit(0)
    for k in config.patches.keys():
        pdev.write_memory(k, config.patches[k])
    print "Successfully applied patches"
    #print "Resetting device state"
    #print "* This will effectiveley disable pwned DFU Mode"
    #print "* Only the signature patches will remain"
    # Send abort
    device.ctrl_transfer(HOST2DEVICE, DFU_ABORT, 0, 0, 0, 0)
    # Perform USB reset
    dfu.usb_reset(device)
    dfu.release_device(device)
    #print "Device is now ready to accept unsigned images"

if __name__ == "__main__":
	main()
