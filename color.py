colors = {
    'Black'            : '\x1b[1;30m',
    'Blue'             : '\x1b[1;94m',
    'Green'            : '\x1b[1;92m',
    'Cyan'             : '\x1b[0;36m',
    'Red'              : '\x1b[0;31m',
    'Purple'           : '\x1b[0;35m',
    'Brown'            : '\x1b[0;33m',
    'Gray'             : '\x1b[0;37m',
    'Dark Gray'        : '\x1b[1;30m',
    'Light Blue'       : '\x1b[1;34m',
    'Light Cyan'       : '\x1b[1;36m',
    'Light Red'        : '\x1b[1;31m',
    'Light Purple'     : '\x1b[1;35m',
    'Yellow'           : '\x1b[1;33m',
    'White'            : '\x1b[1;37m' 
}
class Col:
    Black    = '\x1b[1;30m'
    Blue     = '\x1b[1;94m'
    Green            = '\x1b[1;92m'
    Cyan             = '\x1b[0;36m'
    Red              = '\x1b[0;31m'
    Purple           = '\x1b[0;35m'
    Brown            = '\x1b[0;33m'
    Gray             = '\x1b[0;37m'
    DarkGray        = '\x1b[1;30m'
    LightBlue       = '\x1b[1;34m'
    LightCyan       = '\x1b[1;36m'
    LightRed        = '\x1b[1;31m'
    LightPurple     = '\x1b[1;35m'
    Yellow           ='\x1b[1;33m'
    White            = '\x1b[1;37m'
#choose color per character
def colorchoice(char):
    if char=="^":
        color="White"
    elif char =="*":
        color="Brown"
    elif char=="-":
        color="Gray"
    elif char=="#":
        color="Green"
    elif char=="|":
        color="Light Red"
    elif char in ["?","P","C","$"]:
        color="Brown"
    elif char=="B":
        color="Yellow"
    elif char in ["@","_"]:
        color="Red"
    elif char=="/":
        color="Cyan"
    elif char=="M":
        color="White"
    elif char==">":
        color="White"
    elif char=="o":
        color="Light Cyan"

    else:
        color="Red"

    return(colors[color]+char+'\x1b[0m')

def choicetwo(char):
    if char=="^":
        color="Blue"
    elif char =="*":
        color="Brown"
    elif char=="-":
        color="Light Blue"
    elif char=="#":
        color="Green"
    elif char=="|":
        color="Light Red"
    elif char in ["?","P","C","$"]:
        color="Brown"
    elif char=="B":
        color="Yellow"
    elif char in ["@","_"]:
        color="White"
    elif char=="/":
        color="Red"
    elif char=="M":
        color="White"
    elif char==">":
        color="White"
    elif char=="o":
        color="Red"

    else:
        color="Red"

    return(colors[color]+char+'\x1b[0m')