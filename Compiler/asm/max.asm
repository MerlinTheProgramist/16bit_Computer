define first 33
define second 45

@first
D=A
@0
M=D

@second
D=A
@1
M=D

@0
D=D-M
@OUTPUT_SEC
D;JGT // if second>first output second
// else output first
@0
D=M
@2
M=D

@END
0;JMP

(OUTPUT_SEC)
@1
D=M
@2
M=D

(END)
@2