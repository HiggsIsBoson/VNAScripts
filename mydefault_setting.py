#!/usr/bin/env python

from vna_solib import vna
from sys import argv

mode = 'normal'
if len(argv) >= 2:
    ## force reset (output 0dBm tempolarly)
    if argv[1] == '-r': mode = 'reset'

    ## fast scan mode
    if argv[1] == '-f': mode = 'fast'
    pass


v = vna()
if mode == 'reset': v.reset()

v.set_S21()

v.set_freq_center(6.015e9)
v.set_freq_span(200.e6)

v.set_power(-10)
v.output_on()

v.set_bandwidth(2.e3)
v.set_sweep_points(5001)

v.trigger_single()
v.autoscale()

if mode != 'fast':
    v.set_bandwidth(1.e3)
    v.set_sweep_points(100001)
    pass

v.trigger_cont()
