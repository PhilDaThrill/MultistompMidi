MultistompMidi
by Philip Hugo
 
This was my first real project in Python, so go easy on me. Hey, as long as it works!
Check it out in action here:
https://www.youtube.com/watch?v=W0LHTxjAvKs
 
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CONTENTS / CODE MODULES~~~~~~~~~~~~~~~~~~~~~
msmidi_fx_edit.py:
This module contains the following functions you can call from the outside:
edit_parameter(fx_nbr, param_nbr, value) - only works on effect 0-2. 
switch_fx(switch_step) - hand over 1 or -1 to switch left and right. Other values work as well. Returns 0 if you cannot switch any further.
get_tap_tempo()
set_tap_tempo(tap_tempo) -  unfortunately means that tails are cut off.
All other functions are mostly there for utility. 
 
"switch_fx" and set_tap_tempo" work by copying the patch data, changing the bits that determine the current effect focus / tap tempo and then sending it back. Since the whole patch is re-written, this unfortunately means that tails are cut off.
 
ms_utils:
Strictly utility functions used by msmidi_fx_edit.py
 
The folder "exp_stuff" contains the modules needed to control the Multistomp with an expression pedal if you really have to. They can serve as a basis at most, since I originally wrote it for the HX stomp and did the bare minimum changes for it to work on the Multistomp. The effect and parameter is currently hardcoded.
 
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~HOW TO GET IT TO WORK~~~~~~~~~~~~~~~~~~~~~~~
The code at hand was written for the MS 70 CDR. It will most likely also work on the MS 50G, although you will have to adapt the code as described in Midi Spec #1 (find it below) by replacing the "0x61" with "0x58" in the code. This could be automated using the identity request SysEx message. Most messages will not work for the MS60-B.
 
Hardwarewise you need a Raspberry Pi and a USB cable to connect to the Multistomp. I used the RPi 4 and Zero models, but it will likely work on older models as well.
 
You'll also need to set up Mido. I used the following guide.
https://ixdlab.itu.dk/wp-content/uploads/sites/17/2017/10/Setting-Up-Raspberry-Pi-for-MIDI.pdf
Make sure that
- you use "pip3" (not "pip"!) to install the packages for the python version 3. Otherwise you will get the ModuleNotFound error because it only installs the module for python2.
- you see 'ZOOM MS Series MIDI 1' listed when you type 'amidi -l' into the terminal while the Multistomp is connected. Then you should be fine.
 
Lastly, you'll of course need to call the functions in msmidi_fx_edit.py with your own code.
 
If you really need to use and expression pedal with the Multistomp, you will need to read the values from an expression pedal first. They mostly contain 10K pots that you connect to with a TRS cable. On the Raspberry Pi, you will need to read analog inputs. I recommend the following guide from which I pretty much bluntly copied the code from: 
https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi?view=all
 
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MISCELLANEOUS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These are the two resources that deserve all the glory. I can highly recommend them:
Multistomp Midi Spec #1
https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md
 
Multistomp Midi Spec #2
https://www.dropbox.com/s/z05pzz5wnebcc2y/Zoom%20MS70-CDR%20MIDI%20specification.rtf?dl=0
 
If you want to dive deeper into what these guides provide, I might add that you need to go into editor mode to get things like patch requests to work. Don't worry, the code in this repo does that for you. I'm only mentioning this because I would have liked to known it at the time.
 
