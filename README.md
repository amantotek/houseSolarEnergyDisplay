# houseSolarEnergyDisplay
## Overview
An emonPi https://guide.openenergymonitor.org/technical/emonpi/ monitors energy being used and energy from a solar array.

Export or Import from a mains supply (Electricity company) also occurs.

With a minor modification to an emonPi python file this suite of programs allows display of one or more devices (e.g. laptop, PC)
on same LAN as the emonPi

### Modification to emonPi program
Modify a file on SD card of emonPi. Example below uses editor kate
```
$ cd /opt/openenergymonitor/emonpi/lcd
$ cp emonPiLCD.py emonPiLCD.py.v00 (Keep original)
$ kate emonPiLCD.py &
```
Near top of file add...

```
import netcatRxTx
```
#### Slow Refresh
Near bottom of file add three lines between update and time.sleep for 30s updates
```
  updateLCD() 
  sWatts1 = str(r.get("feed1"))
  sWatts2 = str(r.get("feed2"))
  netcatRxTx.trnsmt(sWatts1,sWatts2) #From Solar, to Grid (Watts)
  time.sleep(lcd_update_sec)
```
This relies on lcd_update_sec staying at 30s

#### Fast Refresh
for 5s update (recommended) modification near end becomes...
```
  updateLCD()
  for ix in range(6):
    netcatRxTx.trnsmt(str(r.get("feed1")),str(r.get("feed2"))) #From Solar, to Grid (Watts)
    time.sleep(5) #30/6 s
  #time.sleep(lcd_update_sec)
```
Here lcd_update_sec is not used

## Transmitter
Below just simulates two fixed power levels being sent. Useful for testing

python3 netcatRxTx.py -t

In real use, within another python program, the transmit function is called directly viz...

netcatRxTx.trnsmt(sWatts1,sWatts2) #From Solar, to Grid (Watts)

## Terminal Receiver
python3 netcatRxTx.py -r

## Graphical Receiver
python3 netcatRxPwrGUI.py

Placing this file in the 'cloud' (e.g. Dropbox) allows running it from any graphical device like a PC or laptop on the same LAN (Local Area Network) as the emonPi

![Exporting](20221017_0917pwrExport.png)

Above Solar generation exceeds the household demand so Export to the grid results 

![Importing](20221016wattsSolarDark.png)

Above after dark the solar system no longer generates
