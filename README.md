# Hacking an rf433 temperature probe

## The temperature and humidity probe Oregon THGR810
![Image](https://github.com/user-attachments/assets/4a85eabd-7aa1-44f7-b024-3813c0648c27)

## Capture signal

Use rtl_433 software to record the signal from THGR810
```
rtl_433 -d driver=hackrf -w capture_thgr810.ook
```
![Image](https://github.com/user-attachments/assets/b5496536-d790-41c0-afed-f0e047c8363c)

## Decode Oregon Protocols V3 and spoof temperature on rf433

Convert signals captured with rtl_433 or rtl-sdr to .sub format.
[https://github.com/evilpete/flipper_toolbox](https://github.com/evilpete/flipper_toolbox)


```
python3 subghz_ook_to_sub.py capture-thgr810.ook
```
