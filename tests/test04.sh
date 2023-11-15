#!/bin/bash

# Copy ASM files
cp ../answers/04/fill/*.asm ../projects/04/fill/
cp ../answers/04/mult/*.asm ../projects/04/mult/


## Assemble
echo "Assemble Fill"
cd ../projects/04/fill
sh ../../../tools/Assembler.sh Fill.asm

echo "Assemble mult"
cd ../mult
sh ../../../tools/Assembler.sh Mult.asm

cd ../../../tests
pwd

## Tests
echo "Fill"
sh ../tools/CPUEmulator.sh ../projects/04/fill/FillAutomatic.tst
echo "Mult"
sh ../tools/CPUEmulator.sh ../projects/04/mult/Mult.tst