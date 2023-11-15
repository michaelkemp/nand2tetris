#!/bin/bash

# Copy HDL files
cp ../answers/01/*.hdl ../projects/01/

## Tests
echo "Not"
sh ../tools/HardwareSimulator.sh ../projects/01/Not.tst
echo "And"
sh ../tools/HardwareSimulator.sh ../projects/01/And.tst
echo "Or"
sh ../tools/HardwareSimulator.sh ../projects/01/Or.tst
echo "Xor"
sh ../tools/HardwareSimulator.sh ../projects/01/Xor.tst
echo "Mux"
sh ../tools/HardwareSimulator.sh ../projects/01/Mux.tst
echo "DMux"
sh ../tools/HardwareSimulator.sh ../projects/01/DMux.tst

echo "Not16"
sh ../tools/HardwareSimulator.sh ../projects/01/Not16.tst
echo "And16"
sh ../tools/HardwareSimulator.sh ../projects/01/And16.tst
echo "Or16"
sh ../tools/HardwareSimulator.sh ../projects/01/Or16.tst
echo "Mux16"
sh ../tools/HardwareSimulator.sh ../projects/01/Mux16.tst

echo "Or8Way"
sh ../tools/HardwareSimulator.sh ../projects/01/Or8Way.tst
echo "Mux4Way16"
sh ../tools/HardwareSimulator.sh ../projects/01/Mux4Way16.tst
echo "Mux8Way16"
sh ../tools/HardwareSimulator.sh ../projects/01/Mux8Way16.tst
echo "DMux4Way"
sh ../tools/HardwareSimulator.sh ../projects/01/DMux4Way.tst
echo "DMux8Way"
sh ../tools/HardwareSimulator.sh ../projects/01/DMux8Way.tst