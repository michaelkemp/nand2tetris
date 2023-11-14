#!/bin/bash

python3 main.py ../../10/ArrayTest/
python3 main.py ../../10/ExpressionLessSquare/
python3 main.py ../../10/Square/

echo "diff ArrayTest"
diff -w ../../10/ArrayTest/_MainT.xml ../../10/ArrayTest/MainT.xml
diff -w ../../10/ArrayTest/_Main.xml ../../10/ArrayTest/Main.xml

echo "diff ExpressionLessSquare"
diff -w ../../10/ExpressionLessSquare/_MainT.xml ../../10/ExpressionLessSquare/MainT.xml
diff -w ../../10/ExpressionLessSquare/_Main.xml ../../10/ExpressionLessSquare/Main.xml
diff -w ../../10/ExpressionLessSquare/_SquareT.xml ../../10/ExpressionLessSquare/SquareT.xml
diff -w ../../10/ExpressionLessSquare/_Square.xml ../../10/ExpressionLessSquare/Square.xml
diff -w ../../10/ExpressionLessSquare/_SquareGameT.xml ../../10/ExpressionLessSquare/SquareGameT.xml
diff -w ../../10/ExpressionLessSquare/_SquareGame.xml ../../10/ExpressionLessSquare/SquareGame.xml

echo "diff Square"
diff -w ../../10/Square/_MainT.xml ../../10/Square/MainT.xml
diff -w ../../10/Square/_SquareT.xml ../../10/Square/SquareT.xml
diff -w ../../10/Square/_SquareGameT.xml ../../10/Square/SquareGameT.xml
diff -w ../../10/Square/_Main.xml ../../10/Square/Main.xml
diff -w ../../10/Square/_Square.xml ../../10/Square/Square.xml
diff -w ../../10/Square/_SquareGame.xml ../../10/Square/SquareGame.xml
