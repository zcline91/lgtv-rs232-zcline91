# LGTV RS232

This is a simple example package to allow control of the LG 47LW6500 TV through its serial port. It may be compatible with other LG TVs and support for more TVs may be added in the future. Right now, this is just for functionality with the TV model that I own.

Example usage:
```python
from lgtv_rs232 import LgTV
tv = LgTV('/dev/ttyUSB0') # Set the argument to the location of your serial device
tv.request('power', 'on')
```

Apologies for the sparse documentation, both here and in the docstrings. I only used this briefly myself.
