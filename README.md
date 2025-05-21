# Hacking an rf433 temperature probe

## The temperature and humidity probe Oregon THGR810
![Image](https://github.com/user-attachments/assets/4a85eabd-7aa1-44f7-b024-3813c0648c27)

## Capture signal with a HackRF One
![Image](https://github.com/user-attachments/assets/2f7489a0-a559-48f0-a4dd-85895ca61207)

Use rtl_433 software to record the signal from THGR810
```
rtl_433 -d driver=hackrf -w capture_thgr810.ook
```
![Image](https://github.com/user-attachments/assets/b5496536-d790-41c0-afed-f0e047c8363c)

## Decode Oregon Protocols V3 and spoof temperature on rf433

Convert signals captured with rtl_433 or rtl-sdr to .sub format:

[https://github.com/evilpete/flipper_toolbox](https://github.com/evilpete/flipper_toolbox)


```
python3 subghz_ook_to_sub.py capture-thgr810.ook
```

Binary visualization with URH:

![Image](https://github.com/user-attachments/assets/25edabd0-f072-40cc-98d2-2a13712cf16f)

This is the logic:

* if state change > long pulse
* if state no change > short pulse

For each change, we take the previous state and reverse it.

Using the spoofing_oregon.py script.
This script will regenerate a frame in Oregon THGR810 format.

The output format is a sub.
Possibility to replay this frame with a flipper zero.

