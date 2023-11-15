import re

class Assembler:
    def __init__(self, asmPath):
        self.asmPath = asmPath

        self.DESTINATION = {
            'null': '000', 
            'M'   : '001',  
            'D'   : '010',  
            'MD'  : '011',  
            'DM'  : '011',  
            'A'   : '100',  
            'AM'  : '101',  
            'MA'  : '101',  
            'AD'  : '110',  
            'DA'  : '110',  
            'AMD' : '111',   
            'ADM' : '111',   
            'MDA' : '111',   
            'MAD' : '111',   
            'DMA' : '111',   
            'MAD' : '111',   
        }

        self.COMPUTATION = {
            '0'   : '101010',
            '1'   : '111111',
            '-1'  : '111010',
            'D'   : '001100',
            'A'   : '110000',
            'M'   : '110000',
            '!D'  : '001101',
            '!A'  : '110001',
            '!M'  : '110001',
            '-D'  : '001111',
            '-A'  : '110011',
            '-M'  : '110011',
            'D+1' : '011111',
            'A+1' : '110111',
            'M+1' : '110111',
            'D-1' : '001110',
            'A-1' : '110010',
            'M-1' : '110010',
            'D+A' : '000010',
            'D+M' : '000010',
            'A+D' : '000010',
            'M+D' : '000010',
            'D-A' : '010011',
            'D-M' : '010011',
            'A-D' : '000111',
            'M-D' : '000111',
            'D&A' : '000000',
            'D&M' : '000000',
            'A&D' : '000000',
            'M&D' : '000000',
            'D|A' : '010101',
            'D|M' : '010101',
            'A|D' : '010101',
            'M|D' : '010101',
        }

        self.JUMP = {
            'null' : '000',
            'JGT'  : '001',
            'JEQ'  : '010',
            'JGE'  : '011',
            'JLT'  : '100',
            'JNE'  : '101',
            'JLE'  : '110',
            'JMP'  : '111',
        }

        self.VARIABLES = {   
            'R0'    : 0,
            'R1'    : 1,
            'R2'    : 2,
            'R3'    : 3,
            'R4'    : 4,
            'R5'    : 5,
            'R6'    : 6,
            'R7'    : 7,
            'R8'    : 8,
            'R9'    : 9,
            'R10'   : 10,
            'R11'   : 11,
            'R12'   : 12,
            'R13'   : 13,
            'R14'   : 14,
            'R15'   : 15,
            'SCREEN': 16384,
            'KBD'   : 24576,
            'SP'    : 0,
            'LCL'   : 1,
            'ARG'   : 2,
            'THIS'  : 3,
            'THAT'  : 4,
        }

        self.VARREGISTER = 16

        self.asm = []

        with open(asmPath) as fp:
            prog = fp.readlines()
            for line in prog:
                ## Strip leading and trailing spaces
                line = line.strip()
                ## Skip blank lines
                if line == "":
                    continue
                ## Skip comment lines -- lines that begin with //
                if re.match("^//", line) is not None:
                    continue
                ## Remove inline comments
                line = line.split("//", 1)[0].strip()

                # Add label
                if line.startswith("("):
                    self.addLabel(line[1:-1], len(self.asm))
                    continue
                
                self.asm.append(line)
        
  


    def addLabel(self, label, lineNumber):
        self.VARIABLES[label] = lineNumber

    def hack(self):
        hack = []
        for command in self.asm:
            if command.startswith("@"):
                hack.append(self.acom(command))
            else:
                hack.append(self.ccom(command))
        return hack

    def acom(self, command):
        ## Strip @ from start of command
        cmd = command[1:]

        try:
            val = int(cmd)
            if (val < 32768):
                address = '{0:016b}'.format(val)
                return address
            else:
                raise SyntaxError("Addressing value exceeds range: {}".format(command))
        except ValueError:
            if cmd in self.VARIABLES:
                address = '{0:016b}'.format(int(self.VARIABLES[cmd]))
            else: ## ADD NEW VARIABLE
                if self.VARREGISTER < self.VARIABLES['SCREEN']:
                    self.VARIABLES[cmd] = self.VARREGISTER
                    address = '{0:016b}'.format(self.VARREGISTER)
                    self.VARREGISTER += 1
                else:
                    raise SyntaxError("Addressing value exceeds range: {}".format(command))
        return address    


    def ccom(self, command):
        # All C Command Addresses begin with 111
        address = "111"

        # Command of the type 0;JMP -- add NULL destination
        if "=" not in command:
            command = "null=" + command
        
        # Command of the type D=D+1 -- add NULL jump
        if ";" not in command:
            command = command + ";null"

        # Command should now be of the type dest=comp;jump
        dest,comp,jump = re.split('=|;',command)

        if "M" not in comp:
            address += "0"
        else:
            address += "1"

        if comp in self.COMPUTATION:
            address += self.COMPUTATION[comp]
        else:
            raise SyntaxError("Unrecognized Computation: {}".format(command))
            
        if dest in self.DESTINATION:
            address += self.DESTINATION[dest]
        else:
            raise SyntaxError("Unrecognized Destination: {}".format(command))

        if jump in self.JUMP:
            address += self.JUMP[jump]
        else:
            raise SyntaxError("Unrecognized Jump: {}".format(command))
            
        return address
