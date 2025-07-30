#!/usr/bin/bash

declare -i index
declare -i max
index=0
max=4000

outdir=/data/muto/cryoloop/20230728/
#outdir=/data/chen/
#outdir=/data/sueno/KUKID/20230308/


# 10sec * 2000 = 20000sec = 5.56hour
#read -p "何回繰り返しますか？:" max
while [ "$index" -lt "$max" ]
do
    echo "$index"番目>> log_20230728.dat
    
    outfile=${outdir}/S21_${index}.dat
    /home/he3/program/vna_solib/measure_swp_vna.py -s 21 -p -10 -f_c 5.e9 -f_s 4.e9 -IF 1.e4 -ch 10001 -ave 2 -outfile ${outfile}  >> log_20230728.dat
    let index++
    
done
