#!/bin/bash

PATH=../pyston_env/bin:../pypy-c-jit-85210-d8cafae12463-linux64/bin/:$PATH

RESULT_DIR='timings'
TIME_OUT='baccarat_time.csv'
TIMEDIFF_OUT='baccarat_timediff.csv'
THREADS_OUT='baccarat_threads.csv'
PROCS_OUT='baccarat_procs.csv'

#for i in 10 100 1000 10000 100000 1000000
#do
#    /usr/bin/time -f "O,%D,%E,%F,%I,%K,%M,%O,%P,%R,%S,%U,%W,%X,%Z,%c,%e,%k,%p,%r,%s,%t,%w" python baccarat/game.py time $i 2>&1 | paste -sd "," - >> $TIME_OUT
#done

. ../bin/activate

rm -v $RESULT_DIR/cpython27
rm -v $RESULT_DIR/pypy
rm -v $RESULT_DIR/pyston
rm -v $RESULT_DIR/cython

echo '[+] Copying pyx files'
for i in `seq 3`
do
    cp -v baccarat/baccarat$i.py baccarat/baccarat_ext$i.pyx
    cp -v baccarat/baccarat$i.py baccarat/baccarat_ext$i.pyx
    cp -v baccarat/baccarat$i.py baccarat/baccarat_ext$i.pyx
done

echo '[+] Compiling Cython .so files'
python setup.py build_ext --inplace

echo '[+] Running Timings'
for i in 10 100 1000 10000 100000 1000000
do
    python baccarat/baccarat1.py timediff $i >> $RESULT_DIR/cpython27
    python baccarat/baccarat2.py timediff $i >> $RESULT_DIR/cpython27
    python baccarat/baccarat3.py timediff $i >> $RESULT_DIR/cpython27
    python baccarat/baccarat1_c.py timediff $i >> $RESULT_DIR/cython
    python baccarat/baccarat2_c.py timediff $i >> $RESULT_DIR/cython
    python baccarat/baccarat3_c.py timediff $i >> $RESULT_DIR/cython
    pypy baccarat/baccarat1.py timediff $i >> $RESULT_DIR/pypy
    pypy baccarat/baccarat2.py timediff $i >> $RESULT_DIR/pypy
    pypy baccarat/baccarat3.py timediff $i >> $RESULT_DIR/pypy
    pyston baccarat/baccarat1.py timediff $i >> $RESULT_DIR/pyston
    pyston baccarat/baccarat2.py timediff $i >> $RESULT_DIR/pyston
    pyston baccarat/baccarat3.py timediff $i >> $RESULT_DIR/pyston
done
