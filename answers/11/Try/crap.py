import jackExpressions

exp = jackExpressions.Expressions()

exp.addTerm("a","variable")
exp.addTerm("+","symbol")
exp.addTerm("3","number")
exp.addTerm("*","symbol")
tmp1 = jackExpressions.Expressions()
exp.addTerm("wed","funcCall", [tmp1])
exp.addTerm("+","symbol")
exp.addTerm("3","number")

tmp1.addTerm("a","variable")
tmp1.addTerm("+","symbol")
tmp1.addTerm("3","number")
tmp1.addTerm("*","symbol")
tmp2 = jackExpressions.Expressions()
tmp1.addTerm("thur","funcCall", [tmp2])

tmp2.addTerm("a","variable")
tmp2.addTerm("+","symbol")
tmp2.addTerm("3","number")

exp.getOutput()

