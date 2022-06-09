// RAM[2] = RAM[0] + RAM[1]
@21
D=A
@0
M=D

@43
D=A
@1
M=D


@0
D=M

@1
A=M
D=D+A

@2
M=D
