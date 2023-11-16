#!/bin/bash

python3 ../answers/10/main.py ../projects/10/ArrayTest/
python3 ../answers/10/main.py ../projects/10/ExpressionLessSquare/
python3 ../answers/10/main.py ../projects/10/Square/

## The answer changed and is incorrect in the new download
echo "diff ArrayTest"
diff -w ../projects/10/ArrayTest/_MainT.xml ../projects/10/ArrayTest/MainT.xml
diff -w ../projects/10/ArrayTest/_Main.xml ../projects/10/ArrayTest/Main.xml

echo "diff ExpressionLessSquare"
diff -w ../projects/10/ExpressionLessSquare/_MainT.xml ../projects/10/ExpressionLessSquare/MainT.xml
diff -w ../projects/10/ExpressionLessSquare/_Main.xml ../projects/10/ExpressionLessSquare/Main.xml
diff -w ../projects/10/ExpressionLessSquare/_SquareT.xml ../projects/10/ExpressionLessSquare/SquareT.xml
diff -w ../projects/10/ExpressionLessSquare/_Square.xml ../projects/10/ExpressionLessSquare/Square.xml
diff -w ../projects/10/ExpressionLessSquare/_SquareGameT.xml ../projects/10/ExpressionLessSquare/SquareGameT.xml
diff -w ../projects/10/ExpressionLessSquare/_SquareGame.xml ../projects/10/ExpressionLessSquare/SquareGame.xml

echo "diff Square"
diff -w ../projects/10/Square/_MainT.xml ../projects/10/Square/MainT.xml
diff -w ../projects/10/Square/_SquareT.xml ../projects/10/Square/SquareT.xml
diff -w ../projects/10/Square/_SquareGameT.xml ../projects/10/Square/SquareGameT.xml
diff -w ../projects/10/Square/_Main.xml ../projects/10/Square/Main.xml
diff -w ../projects/10/Square/_Square.xml ../projects/10/Square/Square.xml
diff -w ../projects/10/Square/_SquareGame.xml ../projects/10/Square/SquareGame.xml
