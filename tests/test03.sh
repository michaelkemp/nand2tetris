#!/bin/bash

# Copy HDL files
cp ../answers/03/a/*.hdl ../projects/03/a/
cp ../answers/03/b/*.hdl ../projects/03/b/

## Tests
echo "Bit"
sh ../tools/HardwareSimulator.sh ../projects/03/a/Bit.tst
echo "Register"
sh ../tools/HardwareSimulator.sh ../projects/03/a/Register.tst
echo "PC"
sh ../tools/HardwareSimulator.sh ../projects/03/a/PC.tst
echo "RAM8"
sh ../tools/HardwareSimulator.sh ../projects/03/a/RAM8.tst
echo "RAM64"
sh ../tools/HardwareSimulator.sh ../projects/03/a/RAM64.tst

echo "RAM512"
sh ../tools/HardwareSimulator.sh ../projects/03/b/RAM512.tst
echo "RAM4K"
sh ../tools/HardwareSimulator.sh ../projects/03/b/RAM4K.tst
echo "RAM16K"
sh ../tools/HardwareSimulator.sh ../projects/03/b/RAM16K.tst

