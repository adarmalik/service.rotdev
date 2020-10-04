Rotary Encoder Support
----------------------

This add-on lets you regulate the volume with a KY040 rotary encoder connected to an RPi.

Enable evdev support for KY040 by adding the following lines to config.txt
```
# enable rotary encoder 
dtoverlay=rotary-encoder,pin_a=23,pin_b=24,relative_axis=1
```

Settings change requires deactivate/activate to take effect.

Based on information found here:

https://blog.ploetzli.ch/2018/ky-040-rotary-encoder-linux-raspberry-pi/

https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/

