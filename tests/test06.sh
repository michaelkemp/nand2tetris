#!/bin/bash

## Assemble
echo "Assemble"
cd ../projects/06/add
sh ../../../tools/Assembler.sh Add.asm
cd ../max
sh ../../../tools/Assembler.sh Max.asm
sh ../../../tools/Assembler.sh MaxL.asm
cd ../pong
sh ../../../tools/Assembler.sh Pong.asm
sh ../../../tools/Assembler.sh PongL.asm
cd ../rect
sh ../../../tools/Assembler.sh Rect.asm
sh ../../../tools/Assembler.sh RectL.asm

cd ../../../tests
pwd

## Test Assembler
echo "Assembler"
python3 ../answers/06/main.py ../projects/06/add/Add.asm
python3 ../answers/06/main.py ../projects/06/max/Max.asm
python3 ../answers/06/main.py ../projects/06/pong/Pong.asm
python3 ../answers/06/main.py ../projects/06/rect/Rect.asm
python3 ../answers/06/main.py ../projects/06/max/MaxL.asm
python3 ../answers/06/main.py ../projects/06/pong/PongL.asm
python3 ../answers/06/main.py ../projects/06/rect/RectL.asm

## Compare
echo "Compare"
diff -w ../projects/06/add/Add.hack ../projects/06/add/_Add.hack
diff -w ../projects/06/max/Max.hack ../projects/06/max/_Max.hack
diff -w ../projects/06/pong/Pong.hack ../projects/06/pong/_Pong.hack
diff -w ../projects/06/rect/Rect.hack ../projects/06/rect/_Rect.hack
diff -w ../projects/06/max/MaxL.hack ../projects/06/max/_MaxL.hack
diff -w ../projects/06/pong/PongL.hack ../projects/06/pong/_PongL.hack
diff -w ../projects/06/rect/RectL.hack ../projects/06/rect/_RectL.hack
