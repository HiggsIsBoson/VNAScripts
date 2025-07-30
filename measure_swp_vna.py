#!/usr/bin/env python

import datetime
from vna_solib import vna
from time import strftime, sleep
from numpy import log10, angle, pi
import sys
import os

from argparse import ArgumentParser

print(datetime.datetime.now())
v = vna()

freq, data = v.get_data()
sleep(1)
v.trigger_cont()
v.output_off()

## make save  directory
'''
print("Please enter the path where you want to save data.  /data/he3/VNA_log/??? ex:20200211")
date = input()
dir_path = '/data/he3/VNA_log/{}'.format(date)
os.makedirs(dir_path,exist_ok=True)
'''


fname = strftime('%Y-%m%d-%H%M%S.dat')
#ofs = open('{}/{}'.format(dir_path,fname), 'w')
ofs = open(fname, 'w')
print('## frequency[GHz]  I  Q  LogM[dB] Phase[deg]', file=ofs)

for f, d in zip(freq, data):
    print(f, d.real, d.imag, log10(abs(d))*20, angle(d)/pi*180, file=ofs)
    pass

ofs.close()
