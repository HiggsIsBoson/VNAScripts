#!/usr/bin/env python

import socket
from time import sleep
from numpy import array

class vna(object):
    def __init__(self,
                 #host = '192.168.10.17',
                 host = '192.168.215.115',
                 port = 5025):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((host, port))
        # socket setting
        self.soc.settimeout(1)
        sleep(1)
        self.buffsize = 4096
        pass


    ## socket tools (Users do not use them.)
    def _send(self, cmd):
        return self.soc.send((cmd + '\r\n').encode())
    def _recv(self, cmd = None):
        if cmd: self._send(cmd)
        ret = ''
        while True:
            try:
                ret_tmp = self.soc.recv(self.buffsize)
            except socket.timeout:
                return 'vna_solib: timeout!'
            ret += ret_tmp.decode()
            if len(ret) > 0 and ret[-1] == '\n': break
            pass
        ret = ret.strip()
        if ret[ 0] == '"': ret = ret[1:]
        if ret[-1] == '"': ret = ret[:-1]
        return ret.strip()
        

    ## reset
    def reset(self):
        self._send('*rst')
        self.output_off()


    ## S-parameter
    def set_S11(self): self._set_Spara('S11')
    def set_S21(self): self._set_Spara('S21')
    def _set_Spara(self, spara = 'S11'):
        self._trace_set()
        self._send('calc:parameter:modify %s' % spara)
        return
    def _trace_set(self):
        if self._recv('calc:parameter:select?'): return
        cat = self._recv('calc:parameter:catalog?').split(',')[0]
        self._send('calc:parameter:select %s' % cat)
        return


    ## source power
    def output_off(self): return self._send('output OFF')
    def output_on(self):  return self._send('output ON')
    def set_power(self, power_dBm):
        return self._send('source:power %f' % float(power_dBm))
    def get_power(self):
        return float(self._recv('source:power?'))


    ## frequency
    def set_freq_start(self, freq_Hz):
        return self._send('sense:freq:start %f'  % float(freq_Hz))
    def set_freq_stop(self, freq_Hz):
        return self._send('sense:freq:stop %f'   % float(freq_Hz))
    def set_freq_center(self, freq_Hz):
        return self._send('sense:freq:center %f' % float(freq_Hz))
    def set_freq_span(self, freq_Hz):
        return self._send('sense:freq:span %f'   % float(freq_Hz))
    def get_freq_start(self):
        return float(self._recv('sense:freq:start?'))
    def get_freq_stop(self):
        return float(self._recv('sense:freq:stop?'))
    def get_freq_center(self):
        return float(self._recv('sense:freq:center?'))
    def get_freq_span(self):
        return float(self._recv('sense:freq:span?'))


    ## sweep points
    def set_sweep_points(self, num):
        return self._send('sense:sweep:points %d' % int(num))
    def get_sweep_points(self):
        return int(self._recv('sense:sweep:points?'))


    ## IF band width
    def set_bandwidth(self, freq_Hz):
        return self._send('sense:bandwidth %f' % float(freq_Hz))
    def get_bandwidth(self):
        return float(self._recv('sense:bandwidth?'))

    ## Number of average
    def set_average_mode(self, mode):
        return self._send('sense:average:mode %f' % int(mode))
    def get_average_mode(self):
        return int(self._recv('sense:average:mode?'))
    def set_average_count(self, nave):
        return self._send('sense:average:count %f' % int(nave))
    def get_average_count(self):
        return int(self._recv('sense:average:count?'))

    ## scale
    def autoscale(self):
        return self._send('display:window:y:auto')


    ## trigger
    def trigger_single(self):
        self._send('sense:sweep:mode SINGLE')
        while self._recv('sense:sweep:mode?') != 'GRO': sleep(1)
        return
    def trigger_cont(self):
        self._send('sense:sweep:mode CONTINUOUS')
        return


    ## get data
    def get_data(self):
        freq = array(self._recv('calc:x?').split(',')).astype(float)
        data = array(self._recv('calc:data? sdata').split(',')).astype(float)
        data = data[0::2] + data[1::2] * 1j
        return freq, data


    ## tool bar - keys, entry
    def tool_keys(self, enable = True):
        val = 'ON' if enable else 'OFF'
        return self._send('display:tool:keys %s' % val)
    def get_tool_keys(self):
        return self._recv('display:tool:keys?') == '1'
    def tool_entry(self, enable = True):
        val = 'ON' if enable else 'OFF'
        return self._send('display:tool:entry %s' % val)
    def get_tool_entry(self):
        return self._recv('display:tool:entry?') == '1'

    pass

'''
    ## set parameter
    def set_param(self, f_c=6.e9, f_s = 1000.e6, power = -20, points = 100001, IFband = 10.e3):
        self.reset()
        self.set_S21()
        self.set_freq_center(f_c)
        print('freq_center', self.get_freq_center()/1e9, 'GHz')
        self.set_freq_span(f_s)
        print('freq_span  ', self.get_freq_span()/1e6,   'MHz')
        self.set_power(power)
        print('power', self.get_power(), 'dBm')
        self.set_sweep_points(points)
        print('sweep point', self.get_sweep_points())
        self.set_bandwidth(IFband)
        print('IF bandwidth', self.get_bandwidth()/1e3, 'kHz')
        self.output_off()
'''

def test1():
    v = vna()

    print('set S11')
    v.set_S11()
    sleep(10)

    print('set S21')
    v.set_S21()
    print('output off')
    v.output_off()
    sleep(10)

    print('output power:', v.get_power())

    print('output on')
    v.output_on()
    print('set output power -20')
    v.set_power(-20)
    sleep(10)

    print('set output power -10')
    v.set_power(-10)
    pass

def test2():
    v = vna()

    print('center: 6GHz,  span: 4GHz')
    v.set_freq_center(6.e9)
    v.set_freq_span(4.e9)
    sleep(15)

    print('center: 6.015GHz,  span: 200MHz')
    v.set_freq_center(6.015e9)
    v.set_freq_span(200.e6)
    pass

def test3():
    v = vna()
    v.trigger_single()
    f, d = v.get_data()
    from matplotlib.pyplot import plot, show
    plot(f, abs(d))
    show()
    # print len(v._recv('calc:data? sdata').split(','))
    # print len(v._recv('calc:x?').split(','))
    
    # print v._recv('calc:x?').split(',')[0:10]
    # print v._recv('calc:data? fdata').split(',')[0:10]
    # print v._recv('calc:data? sdata').split(',')[0:10]
    # print v._recv('calc:data? rdata').split(',')[0:10]
    pass

def test4():
    v = vna()
    v.reset()
    print(v._recv('sense:sweep:mode?'))
    v.set_S21()
    v.set_freq_center(5.5e9)
    print('freq_center', v.get_freq_center()/1e9, 'GHz')
    v.set_freq_span(1500.e6)
    print('freq_span  ', v.get_freq_span()/1e6,   'MHz')
    v.set_power(-10)
    print('power', v.get_power(), 'dBm')
    v.output_on()
    v.set_sweep_points(100001)
    print('sweep point', v.get_sweep_points())
    v.set_bandwidth(1.e3)
    print('IF bandwidth', v.get_bandwidth()/1e3, 'kHz')
    v.output_off()
    print('output off', v.get_power(), 'dBm')
    print(array(v._recv('calc:x?').split(',')).astype(float))
    v._send('sense:sweep:mode SINGLE')
    print(v._recv('sense:sweep:mode?'))

def test5():
    v = vna()
    v.set_param()

if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    #test4()
    test5()
    pass


