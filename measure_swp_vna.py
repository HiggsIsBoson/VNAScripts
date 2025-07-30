#!/usr/bin/env python                                                                             
import datetime
from vna_solib import vna
from time import sleep
from numpy import array
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('-s','--S_param',
                    type=float,
                    default=21,
                    help='S_param of measurement. default=21(S21)')

parser.add_argument('-f_c','--f_center',
                    type=float,
                    default=6.e9,
                    help='sweep center frequency. default=6.e9')

parser.add_argument('-f_s','--f_span',
                    type=float,
                    default=1000.e6,
                    help='sweep span. f_c +- f_s/2. default=1000.e6(1GHz)')

parser.add_argument('-p', '--power',
                    type=float,
                    default=-20,
                    help='supply power(dBm). defalt = -20(dBm)')

parser.add_argument('-IF', '--IFband',
                    type=float,
                    default=10.e3,
                    help='IF bandwidth(Hz). defalt=10.e3')

parser.add_argument('-ch',
                    type=float,
                    default=100001,
                    help='the number of freqency channles. defalut=100001')

parser.add_argument('-ave',
                    type=int,
                    default=1,
                    help='Number of average. defalut=1')

parser.add_argument('-outfile',
                    type=str,
                    default="None",
                    help='Output file name')

args = parser.parse_args()

Sparam = args.S_param
f_center = args.f_center
f_span = args.f_span
power = args.power
IFband = args.IFband
ch = args.ch
nave = args.ave
fname = args.outfile

print(datetime.datetime.now())

v = vna()

v.reset()
if Sparam == 21:
    v.set_S21()
elif Sparam == 12:
    v.set_S11()
elif Sparam == 11:
    v.set_S11()
else:
    print('Sparam error: Spara, does not match 21(S21) or 12(S12) or 11(S11)')
v.set_freq_center(f_center)
print('freq_center', v.get_freq_center()/1e9, 'GHz')
v.set_freq_span(f_span)
print('freq_span  ', v.get_freq_span()/1e6,   'MHz')
v.set_power(power)
print('power', v.get_power(), 'dBm')
v.set_sweep_points(ch)
print('sweep point', v.get_sweep_points())
v.set_bandwidth(IFband)
print('IF bandwidth', v.get_bandwidth()/1e3, 'kHz')

if nave > 1 :
    v.set_average_mode(1)
    v.set_average_count(nave)
    print('Number of average', v.get_average_count())

# Start data taking
exp_DAQ_time = nave * ch / (IFband+0.) # in second
print("Expected DAQ time [sec]", exp_DAQ_time)

v.output_on()
v.trigger_single()
sleep(exp_DAQ_time+2.)

# Fetch the outcome
freq, data = v.get_data()

# Shut down
sleep(1)
v.trigger_cont()
v.output_off()

# Write 
if fname is "None" :
    fname = strftime('%Y-%m%d-%H%M%S.dat') 

ofs = open(fname, 'w')
print('## frequency[GHz]  I  Q  LogM[dB] Phase[deg]', file=ofs)

for f, d in zip(freq, data):
    print(f, d.real, d.imag, log10(abs(d))*20, angle(d)/pi*180, file=ofs)
    pass

ofs.close()
