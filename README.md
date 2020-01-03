# Vieux - A tool for 32/64 Bit iOS downgrades using OTA Blobs

## By - Matty ([Twitter - @mosk_i](https://twitter.com/mosk_i))
#### With help from - Merc ([Twitter - @Vyce_Merculous](https://twitter.com/Vyce_Merculous))

-----------------
# Requirements 
A MacOS machine (Hackintosh or legit Mac) running 10.14.x or higher

Compatible iOS device - If your device is 32 Bit it needs to be jailbroken with OpenSSH installed (Some devices need a reboot and rejailbreak after installing OpenSSH)

The ability to read this README

-----------------
# Device support

## iOS 10.3.3
iPhone 5s, iPad Air, iPad Mini 2 (Not iPad4,6)

## iOS 8.4.1
iPhone 5, iPhone 4s, iPad 2, iPad 3, iPad 4, iPad Mini 1, iPod 5 

## iOS 6.1.3
iPhone 4s, iPad 2 (Not iPad2,4)

-----------------

# Usage
```
Usage: viuex [OPTIONS] [IPSW PATH (If required)]

Options:

  -i, --ipsw PATH		Path to IPSW file
  -c, --clean			Clean up any leftover files
  -k, --kdfu PATH		"Path/To/patchiBSS" Enter KDFU mode (32 Bit Only, device must be jailbroken)
  -l, --list			List what devices can be restored to what iOS versions
  -p, --pwn		        Enter PWNDFU mode, which will also apply sig patches (64 Bit Only)
  -r, --restore		        "Path/To/.ipsw" Just restore to a custom ipsw
  -s, --shsh PATH	        "Path/To/Save/Location/" Save OTA blobs to a given path for future use (64 Bit Only)
  -v, --version			List the version of the tool
  -y, --credits			List credits and Big Yoshi

```



-----------------
# Installing dependencies

Needs Python3 (At least 3.5)

Also needs Python2 but that comes default with macOS

Run 'pip3 install -r requirements.txt' to install all dependencies

-----------------
# Instructions

1. 'pip3 install -r requirements.txt' to install all dependencies
2. 'cd' into the 'Vieux' folder that you either git cloned or downloaded
3. run './vieux -i "PATH/TO/.ipsw"' or, if the that command doesn't work, 'python3 vieux -i "PATH/TO/.ipsw"'
4. Follow what the tool tells you to do
5. Profit?
-----------------
# F.A.Q
### How do I use this tool?
If you have a 64 Bit device (iPhone 5s, iPad Mini 2, iPad Air) then just connect your device in DFU mode and run the tool, if you have a 32 Bit device then just connect the device in Normal mode, NOT DFU MODE, and run the tool!

### What devices does this support/when will it support my iPad XX or iPhone XX?
See [above](#current-device-support), all compatible devices are already supported. No other devices will ever be supported for the 10.3.3 downgrade. Ever.

### Why does the tool not run?
Make sure you have ran "pip3 install -r requirements.txt" before attempting to use this tool. If that doesn't fix the issue, take a screen shot of the error and create an issue on the Github page.

### When will other OS's be supported? E.G Linux, Windows, etc...
There will most likely never be Windows support as Windows is an awful OS for any iOS related stuff. Linux support is possible and will most likely come at a later date. macOS only for now, Mojave is best but Catalina works. Lower then Mojave is untested and officially unsupported but feel free to try, just don't expect any help from me if it doesn't work.

### Why should I use this over other older methods?
This is by far the fastest tool for OTA downgrades on the market, plus no other tool can do both 32 and 64 Bit downgrades. Also this tool "Just Works (TM)" so there is no reason not to try it!

### How can I get help with an error/issue that I can't figure out?
If you have tried everything mentioned in this readme, you can either open an issue on the Github page, tweet @ me (@mosk_i) or send me a DM on twitter (@mosk_i). 

Please include as much detail as you can, including but not limited to - Full log from the tool, macOS version, device model/iOS version you are trying to downgrade to and what you have already tried.

### How do you pronounce "Vieux"?
"vyuh" apparently, I've had 5 different pronunciations given to me, it's French for "old" which fits well with the old iOS versions this tool downgrades devices to! Not that iOS 6/8/10 are bad at all, even given their age.

-----------------
# Credits

[@axi0mX](https://twitter.com/axi0mX) - Checkm8/ipwndfu

[@tihmstar](https://twitter.com/tihmstar) - Futurerestore/tsschecker

[@linushenze](https://twitter.com/LinusHenze) - SecureROM Signature Check Remover

[@geohotz](https://twitter.com/realGeorgeHotz) - Fork of ipwndfu ported to Python3

[@Vyce_Merculous](https://twitter.com/Vyce_Merculous) - General help/Cleaning up my messy code

[@xerusdesign](https://twitter.com/xerusdesign) - Testing

[Schnob](https://github.com/Schnob) - Testing/Fixing non-cellular iPad support 

-----------------
