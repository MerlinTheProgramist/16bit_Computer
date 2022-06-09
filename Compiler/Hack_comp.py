import argparse
from typing import List
import re

"""
A = address/data register (can be set to static number)
    @10 //set register A to 10
    D = A //set register D to content of A, so D = 10
    D = M //set register D to RAM register with id 10
D = data register (can NOT be set to static number)
M = currently selected memory register
    @17
    D = M //like D = RAM[17]


// RAM[17] = 10
@10
D=A
@17
M=D

// RAM[5] = RAM[3]
@3
D=M
@5
M=D

Compiling:
    3 bits 1

    a bit:
        0 = A
        1 = M

    6 comp bits with D and {A,B}[a]

    dest:
        null = 0 0 0
        M    = 0 0 1
        D    = 0 1 0
        MD   = 0 1 1
        A    = 1 0 0
        AD   = 1 1 0
        AMD  = 1 1 1



"""

COMPS={
"0":  "101010",
"1":  "111111",
"-1": "111010",
"D":  "001100",
"A":  "110000",#"M":"110000",
"!D": "001101",
"!A": "110001",
"-D": "001111",
"-A": "110011",#"-M":"110011",
"D+1":"011111",
"A+1":"110111",#"M+1":"110111",
"D-1":"001110",
"A-1":"110010",#"M-1":"110010",
"D+A":"000010",#"D+M":"110111",
"D-A":"010011",#"D-M":"010011",
"A-D":"000111",#"M-D":"",
"D&A":"000000",#"D&M":"000000",
"D|A":"010101"#"D|M":"010101"
}

DESTS={
"M":"001",
"D":"010",
"MD":"011",
"A":"100",
"AM":"110",
"AD":"101",
"AMD":"111"
}

JMPS={
"JGT":"001",
"JEQ":"010",
"JGE":"011",
"JLT":"100",
"JNE":"101",
"JLE":"110",
"JMP":"111"
}

branches={}
consts={}

exit_code="1"+"0"*15

MAX_VAL = 2**15-1

def compile(text:str)->List[str]:
    out_bin:List[str]=list()

    for i,line in enumerate(find_labels(text.split('\n'))):
        line=line.strip().replace(" ","")

        if line[:2]=="//" or not line: continue

        if re.search(r"//.*",line):
            line = line[:re.search(r"//.*",line).span()[0]]

        out_bin.append(operation(line,i))

    out_bin.append(exit_code)

    return out_bin

def find_labels(lines:List[str])->str:
    simplified_out=[]
    i = 0
    for line in lines:
        line=line.strip()#.replace(" ","")
        if not line or line[:2]=="//": continue

        if re.search(r"\(.*\)",line):
            branches[re.search(r"\(.*\)",line).group()[1:-1]] = i
        
        elif "define" in line:
            const_name, const = line.replace("define","").strip().split(" ")
            branches[const_name] = int(const)        
        else:
            simplified_out.append(line)
            i+=1

    return simplified_out

def operation(line:str,line_num)->str:
    print(f"{line_num}. {line}")

    dest=line[0]


    if line[0]=="@": # set register A(address) to val
        bin_num = ""
        if not line[1:].isnumeric():
            if not line[1:] in branches: return
            bin_num = bin(branches[line[1:]])[2:]
        else:
            num:int = int(re.search(r'[\d]+',line).group())
            assert -MAX_VAL<num<MAX_VAL, f"too high value at line {line_num}"

            bin_num = bin(num)[2:]
        return "0" + "0"*(15-len(bin_num)) + bin_num
    
    elif line=="quit":
        out=exit_code
    else:
        out="111"
        if "M" in line:
            out+="1"
        else:
            out+="0"

        expr = line.split(";")[0]

        #comp
        comp = re.search(r"(([\d+,\w][\+,\-][\d+,\w])|\d+|\w)$",expr).group().replace("M","A")
        print(comp)

        if comp in COMPS:
            out+= COMPS[comp]
        elif comp[::-1] in COMPS and "+" in comp:
            out+= COMPS[comp[::-1]]
        else:
            print(comp)
            print(f"No operation like: {comp}")
            quit()

        # dest
        dest = re.search(r'.=',expr) #get everything before = character
        if dest:
            out+=DESTS[dest.group()[:-1].strip()]
        else:
            out+="000"

        # jmp
        if ";" in line:
            out+=JMPS[ re.search(r';.*',line).group()[1:].strip() ]
        else:
            out+="000"

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Compile Hack code to binary")
    parser.add_argument("path",default=None)
    parser.add_argument("out_path",)
    args = parser.parse_args()

    if args.path:
        with open(args.path) as file:
            instructions:List[str] = compile(file.read())

            with open("./builds/"+args.path.replace("asm","hex"), "w") as out:
                out.write("v2.0 raw\n")
                for ins in instructions:
                    print(ins)
                    out.write(hex(int(ins,2))[2:].upper() + "\n")

    else:
        while(True):
            print(compile(input())[0])

