import re

DESTINATION = {
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

COMPUTATION = {
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

JUMP = {
    'null' : '000',
    'JGT'  : '001',
    'JEQ'  : '010',
    'JGE'  : '011',
    'JLT'  : '100',
    'JNE'  : '101',
    'JLE'  : '110',
    'JMP'  : '111',
}

def hack(asm):
    hack = []
    for command in asm:
        if command.startswith("@"):
            hack.append(acom(command))
        else:
            hack.append(ccom(command))
    return hack

def acom(command):
    ## Strip @ from start of command
    cmd = command[1:]

    ## Get Integer Value of Command
    val = int(cmd)
    if (val < 32768):
        address = '{0:016b}'.format(val)
        return address
    
    raise SyntaxError("Addressing value exceeds range: {}".format(command))

def ccom(command):
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

    if comp in COMPUTATION:
        address += COMPUTATION[comp]
    else:
        raise SyntaxError("Unrecognized Computation: {}".format(command))
        
    if dest in DESTINATION:
        address += DESTINATION[dest]
    else:
        raise SyntaxError("Unrecognized Destination: {}".format(command))

    if jump in JUMP:
        address += JUMP[jump]
    else:
        raise SyntaxError("Unrecognized Jump: {}".format(command))
        
    return address
