#!/bin/bash

## Test Translator
echo "Translator"
python3 ../answers/08/main.py ../projects/08/FunctionCalls/FibonacciElement/
python3 ../answers/08/main.py ../projects/08/FunctionCalls/NestedCall/
python3 ../answers/08/main.py ../projects/08/FunctionCalls/SimpleFunction/
python3 ../answers/08/main.py ../projects/08/FunctionCalls/StaticsTest/

python3 ../answers/08/main.py ../projects/08/ProgramFlow/BasicLoop/
python3 ../answers/08/main.py ../projects/08/ProgramFlow/FibonacciSeries/


echo "testing"
sh ../tools/CPUEmulator.sh ../projects/08/FunctionCalls/FibonacciElement/FibonacciElement.tst
sh ../tools/CPUEmulator.sh ../projects/08/FunctionCalls/NestedCall/NestedCall.tst
sh ../tools/CPUEmulator.sh ../projects/08/FunctionCalls/SimpleFunction/SimpleFunction.tst
sh ../tools/CPUEmulator.sh ../projects/08/FunctionCalls/StaticsTest/StaticsTest.tst

sh ../tools/CPUEmulator.sh ../projects/08/ProgramFlow/BasicLoop/BasicLoop.tst
sh ../tools/CPUEmulator.sh ../projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.tst
   