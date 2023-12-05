#!/bin/bash

python3 main.py Try/Terms.jack > Try/_Terms.vm
../../tools/JackCompiler.sh Try/Terms.jack

python3 main.py Try/Function.jack > Try/_Function.vm
../../tools/JackCompiler.sh Try/Function.jack

python3 main.py Try/Array.jack > Try/_Array.vm
../../tools/JackCompiler.sh Try/Array.jack

diff -w Try/Terms.vm Try/_Terms.vm
diff -w Try/Function.vm Try/_Function.vm
##diff -w Try/Array.vm Try/_Array.vm
