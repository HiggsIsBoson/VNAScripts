#!/usr/bin/bash

declare -i index
declare -i max
index=0
max=60
#read -p "何回繰り返しますか？:" max
while [ "$index" -lt "$max" ]
do

attn1=$index
#attn2=`expr 30 - $index`
#change variable attn
#/data/sueno/script/controls/LDAControl/atten_manager 26039 $attn1
/data/sueno/script/controls/LDAControl/atten_manager 22267 $attn1
#/data/sueno/script/controls/LDAControl/atten_manager 24830 $attn2
sleep 1

echo "$index"番目>> log_20220215_attn.dat
# S21
cd /data/sueno/others/20220215
/home/he3/program/vna_solib/set_param.py -s 21 -p 10 -f_c 6.e9 -f_s 8.e9 -IF 1.e3 -ch 10001 >> log_20220215_attn.dat
sleep 8
/home/he3/program/vna_solib/measure_swp_vna.py
"""
# S12
cd /data/takeichi/cryoloop/20220210/S11
/home/he3/program/vna_solib/set_param.py -s 11 -p -30 -f_c 6e9 -f_s 8.e9 -IF 1.e3 -ch 10001 >> log_2\
0220210.dat
sleep 8
/home/he3/program/vna_solib/measure_swp_vna.py
"""

let index++
done
