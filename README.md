# PythonOTADowngrader

## By - Matty (Twitter - @mosk_i)
## With help from - Merc (Twitter - @Vyce_Merculous)

# Current device support

## 10.3.3
### iPhone 5s, iPad Air, iPad Mini (Not iPad4,6)

## 8.4.1
### iPhone 5, More 32 bit device support is coming

# Installing dependencies

Needs python3 (I used 3.8 but any 3.x should be fine) and python2 installed. Am working on removing the python2 dependency, should have it gone by the full release :)

All other dependecies are in requirements.txt

pip install -r requirements.txt


# Instructions

1. 'cd' into the 'PythonOTADowngrader' folder
2. run './main.py' or, if the first command doesn't work, 'python3 main.py'
3. Follow what the tool tells you to do
4. Profit?

# Known Issues

Sometimes the program will crash and complain about "USB permissions" if it is run multiple times back to back in quick succession. No clue why it does this, but just waiting 5 seconds or so will fix this issue

No output in terminal when the device is restoring. This isn't really an issue, more of a choice I made. I am working on adding a "verbose" option which will show the output of everything that I've hidden for those that want it.

It only works on MacOS machines (hackintosh or legit). This is something that *can* be fixed at least Linux support could be added, just would need someone to compile the edited futurerestore for OTA downgrades on Linux so I can create a patchfile for the currently released Linux binary. Everything else this tool does *should* work fine on Linux already. Windows sucks.


# Other Things

This tool is my first venture into Python, so there are probably a plethora of things that I could have done better. If you find something then just open a pull request and explain why the changes you have made are better :) I'm quite fine with admitting that I am not an expert in Python and I would love some help/critisism on this tool. Also this tool will never support any devices other then A5, A6 and A7 ones (unless later on other checkm8 vulnerable devices end up with a permenatly signed OTA version) so don't even ask.
