import re

class Tokenizer:
    def __init__(self, jackPath):
        self.jackPath = jackPath

        self.keywords = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
        self.symbols = ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]

        self.tokens = []

        with open(self.jackPath) as fp:
            self.jack = fp.read()
  
        self.parseTokens()

    def getTokens(self):
        return self.tokens

    def parseTokens(self):

        while len(self.jack) > 0:
            found = False

            # whitespace
            while re.search("^\s", self.jack): ## \s matches unicode whitespace including \t\n\r\f\v
                self.jack = self.jack[1:]

            # inline comment
            if re.search("^//.*", self.jack): ## . matches everything except newline
                theMatch = re.match("^//.*", self.jack).group(0)
                self.jack = self.jack[len(theMatch):]
                continue

            # multiline comment
            if re.search("^/\*[\s\S]*?\*/", self.jack): ## \S matches any NON whitespace character (This is the oposite of \s )
                theMatch = re.match("^/\*[\s\S]*?\*/", self.jack).group(0) ## *? is the greedy quantifier -- matching as many characters as possible before reaching */
                self.jack = self.jack[len(theMatch):]
                continue

            # string
            if re.search('^(")([^\n]*)(")', self.jack):
                theMatch = re.match('^(")([^\n]*)(")', self.jack).group(0)
                self.jack = self.jack[len(theMatch):]
                type = "stringConstant"
                value = theMatch.strip('"')
                self.tokens.append({"type":type,"value":value})
                found = True

            # identifiers and keywords 
            if re.search("^([_a-zA-Z]{1})([\w]*)", self.jack): ## \w matches unicode word characters including alpha, numeric and underscore
                theMatch = re.match("^([_a-zA-Z]{1})([\w]*)", self.jack).group(0)
                self.jack = self.jack[len(theMatch):]
                if theMatch in self.keywords:
                    type = "keyword"
                    value = theMatch
                    self.tokens.append({"type":type,"value":value})
                    found = True
                else:
                    type = "identifier"    
                    value = theMatch
                    self.tokens.append({"type":type,"value":value})
                    found = True
                

            # symbols        
            for sym in self.symbols:
                if re.search("^\{}".format(sym), self.jack):
                    self.jack = self.jack[1:]
                    type = "symbol"
                    value = sym
                    self.tokens.append({"type":type,"value":value})
                    found = True

            # integers
            if re.search("^\d+", self.jack): ## \d matches unicode decimal digits
                theMatch = re.match("^\d+", self.jack).group(0)
                self.jack = self.jack[len(theMatch):]
                type = "integerConstant"
                value = theMatch
                if int(value) < 0 or int(value) > 32767:
                    raise OverflowError("Integer out of range: {}".format(value))
                self.tokens.append({"type":type,"value":value})
                found = True

            # error
            if len(self.jack) > 0 and not found:
                theMatch = re.match("^[\S]+", self.jack).group(0)
                raise SyntaxError("Syntax Error: {}".format(theMatch))
                
