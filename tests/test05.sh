#!/bin/bash

# Copy HDL files
cp ../answers/05/*.hdl ../projects/05/

## Tests
echo "CPU"
sh ../tools/HardwareSimulator.sh ../projects/05/CPU.tst
sh ../tools/HardwareSimulator.sh ../projects/05/CPU-external.tst
echo "Memory -- needs to be run interactively"
#sh ../tools/HardwareSimulator.sh ../projects/05/Memory.tst
echo "Computer"
sh ../tools/HardwareSimulator.sh ../projects/05/ComputerAdd.tst
sh ../tools/HardwareSimulator.sh ../projects/05/ComputerMax.tst
sh ../tools/HardwareSimulator.sh ../projects/05/ComputerRect.tst
