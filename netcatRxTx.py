#!/usr/bin/python
#Created 09Oct2022 MD
#Version 16Oct2022 1532
#Usage: python3 netcatRxTx.py -t (transmit) or python3 netcatRxTx.py -r (receive)
#Transmits power data from emonPi or receives data for terminal display on devices (eg laptops) on same LAN as emonPi
# https://guide.openenergymonitor.org/technical/emonpi/ emonPi website
# nc = netcat
# sudo apt install socat

import datetime
import subprocess, time, os, sys

sProgName = "netcatRxTx.py"
SKT = 5005

def heelp():
  print("Use for TX like: python3 {} -t".format(sProgName))
  print(" or for RX like: python3 {} -r".format(sProgName))
  sys.exit()

def trnsmt(sWats1,sWats2):
  xdt = datetime.datetime.now()
  #xdt = datetime.datetime.now().astimezone()
  sDatTim = xdt.strftime("%Y%b%d %H:%M:%S")
  #sDf = "echo '{},{},{}' | nc -N 192.168.0.52 {}".format(sWats1,sWats2,sDatTim,SKT)
  sDf = "echo '{},{},{}' | socat - UDP-DATAGRAM:255.255.255.255:{},broadcast".format(sWats1,sWats2,sDatTim,SKT)
  try:
    os.system(sDf)
    print("TXing "+sDf)
  except:
    print("Failed to send, is RX setup?")
  
#-----------------------------------
# Defining main function
def main():
  #Decide on user input mode
  sProgName = sys.argv[0]
  #print ('Number of arguments:', len(sys.argv), 'arguments.')
  iNumArgs = len(sys.argv)
  if iNumArgs != 2:
    heelp()
  #print ('Argument List:', str(sys.argv))
  sArg = sys.argv[1]
  #print(sArg)
  if sArg != "-t" and sArg != "-r":
    heelp()

  if sArg == "-r":
    #Receive
    #Put below on RX device terminal
    # $ nc -l -k -u 5005 (-k keep running u=UDP)
    #cmd = "nc -l -k {}".format(SKT)
    cmd = "nc -ulk {}".format(SKT)
    p, line = True, 'start'

    p = subprocess.Popen(cmd,
                      shell=True,
                      bufsize=64,
                      stdin=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      stdout=subprocess.PIPE)
    for line in p.stdout:
      #print(">>> " + str(line.rstrip()))
      sAll = line.rstrip().decode() #Convert Bytes to a string
      sImEx = ""
      #print(sAll)
      lAll = sAll.split(',') #Convert comma seperated string to a list
      if len(lAll) == 3:
        sPsolar = lAll[0] #+ve if generating
        sPdrain = lAll[1] #+ve To grid -ve from grid
        sDatTim = lAll[2]
        if (sPsolar.replace('-','')).isnumeric() and (sPdrain.replace('-','')).isnumeric():
          iPsolar = int(sPsolar)
          iPdrain = int(sPdrain)
          iPgrid = iPsolar + iPdrain
          if iPgrid < 0:
            sImEx = "Importing"
          else:
            sImEx = "Exporting"
          print("Solar {}w, Drain {}w, Grid {}w {}, {}".format(iPsolar,sPdrain,iPgrid,sImEx,sDatTim))
      if sImEx == "":
        #Calculation wasn't completed
        print("X {} {}".format(sAll,sDatTim))    
      p.stdout.flush()  
    
  if sArg == "-t":
    #Transmit
    #Client needs to know of the existence of and the address of the server (as here)
    #, but the server does not need to know the address of (or even the existence of)
    # the client prior to the connection being established 
    #Below uses IP and channel of RX device
    while (1):
      trnsmt("56789","1234") #From Solar, to Grid (Watts)
      time.sleep(4) 
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()    
