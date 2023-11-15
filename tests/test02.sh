#!/bin/bash

# Copy HDL files
cp ../answers/02/*.hdl ../projects/02/

## Tests
echo "HalfAdder"
sh ../tools/HardwareSimulator.sh ../projects/02/HalfAdder.tst
echo "FullAdder"
sh ../tools/HardwareSimulator.sh ../projects/02/FullAdder.tst
echo "Add16"
sh ../tools/HardwareSimulator.sh ../projects/02/Add16.tst
echo "Inc16"
sh ../tools/HardwareSimulator.sh ../projects/02/Inc16.tst
echo "ALU"
sh ../tools/HardwareSimulator.sh ../projects/02/ALU.tst
