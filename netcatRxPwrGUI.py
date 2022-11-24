#!/usr/bin/python
#Created 09Oct2022 by MD
#Version 23 Nov 2022 1719
#Usage: python3 netcatRxPwrGUI.py
#pip3 install --upgrade PySimpleGUI
#python3 -m pip install --upgrade --no-cache-dir PySimpleGUI (update GUI)
#https://www.pysimplegui.org/en/latest/call%20reference/ Call reference
#https://www.pysimplegui.org/en/latest/ Home
#$ scp netcatRxPwrGUI.py fred@192.168.0.52:/home/fred/Downloads (e.g. to kitchen)
#https://www.pysimplegui.org/en/latest/cookbook/  see new Push() justify
#as e.g.           [sg.Push(), sg.Text('23450w'), sg.Push()],
import datetime
import subprocess, time, os, sys

import PySimpleGUI as sg

sg.theme('SystemDefault')	# Add a touch of color was DarkAmber
#Line of stars [sg.Text('*'*50)],
DIREXPORT = '>'*21
DIRIMPORT = '<'*21
SKT = 5005

layout = [
          [sg.Text(' '*36)],
          [sg.Text('SOLAR'), sg.Push()],
          [sg.Text('-w',key='KYSOL'), sg.Push()],
          [sg.Text('V')],
          [sg.Text('V')],
          [sg.Text(DIREXPORT,key='KYDIR'), sg.Text('GRID'), sg.Push()],
          [sg.Text('V'+' '*20), sg.Text('-w',key='KYGRD'), sg.Push()],
          [sg.Text('V')],
          [sg.Text('HOUSE'), sg.Push()],
          [sg.Text('-w',key='KYHSE'), sg.Push()],
          [sg.Text('')],
          [sg.Push(), sg.Text(' '*20,key='KYDATI'), sg.Push()],
         ]

OurFont = ("Courier", 16)
wiindow = sg.Window('Electricity flow', layout, font=OurFont)

sPsolar = "?"
sPgrid = "?"
sPdrain = "?"
sDirflo = DIREXPORT

bRuun = True
while bRuun:
  cmd = "nc -ulk {}".format(SKT)
  p, liine = True, 'start'

  p = subprocess.Popen(cmd,
                    shell=True,
                    bufsize=64,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE)
  for liine in p.stdout:
    eveent, values = wiindow.read(timeout=40, timeout_key='KYSOL')
    if eveent in (sg.WIN_CLOSED, 'Cancel'):
      bRuun = False
      break
    sAll = liine.rstrip().decode() #Convert Bytes to a string
    sImEx = ""
    #print(sAll)
    lAll = sAll.split(',') #Convert comma seperated string to a list
    if len(lAll) == 3:
      sPsolar = lAll[0] #+ve if generating
      sPdrain = lAll[1] #+ve To grid -ve from grid
      sDatTim = lAll[2] #Like 2022Oct16 21:36:14 (18 chars)
      if (sPsolar.replace('-','')).isnumeric() and (sPdrain.replace('-','')).isnumeric():
        iPsolar = int(sPsolar)
        iPdrain = int(sPdrain)
        iPgrid = iPsolar + iPdrain
        sPgrid = str(iPgrid) #For GUI display
        if iPgrid < 0:
          sImEx = "Importing"
          sDirflo = DIRIMPORT
          sDirColor = 'red' #Not good
        else:
          sImEx = "Exporting"
          sDirflo = DIREXPORT
          sDirColor = 'green' #Good
        print("Solar {}w, House {}w, Grid {}w {}, {}".format(iPsolar,sPdrain,iPgrid,sImEx,sDatTim))
        wiindow["KYSOL"].Update(sPsolar+'w')
        wiindow["KYGRD"].Update(sPgrid+'w')
        wiindow["KYHSE"].Update(sPdrain+'w')
        wiindow["KYDIR"].Update(sDirflo,text_color = sDirColor)
        wiindow["KYDATI"].Update(sDatTim)
        wiindow.refresh() #Make updates show up immediately

    if sImEx == "":
      #Calculation wasn't completed
      print("X {} {}".format(sAll,sDatTim))    
      wiindow["KYSOL"].Update('??w')
      wiindow["KYGRD"].Update('??w')
      wiindow["KYHSE"].Update('??w')
    p.stdout.flush()  

wiindow.close()
del wiindow
