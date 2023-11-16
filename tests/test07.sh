#!/bin/bash

## Test Translator
echo "Translator"
python3 ../answers/08/main.py ../projects/07/MemoryAccess/BasicTest/BasicTest.vm
python3 ../answers/08/main.py ../projects/07/MemoryAccess/PointerTest/PointerTest.vm
python3 ../answers/08/main.py ../projects/07/MemoryAccess/StaticTest/StaticTest.vm

python3 ../answers/08/main.py ../projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm
python3 ../answers/08/main.py ../projects/07/StackArithmetic/StackTest/StackTest.vm

echo "testing"
sh ../tools/CPUEmulator.sh ../projects/07/MemoryAccess/BasicTest/BasicTest.tst
sh ../tools/CPUEmulator.sh ../projects/07/MemoryAccess/PointerTest/PointerTest.tst
sh ../tools/CPUEmulator.sh ../projects/07/MemoryAccess/StaticTest/StaticTest.tst

sh ../tools/CPUEmulator.sh ../projects/07/StackArithmetic/SimpleAdd/SimpleAdd.tst
sh ../tools/CPUEmulator.sh ../projects/07/StackArithmetic/StackTest/StackTest.tst
