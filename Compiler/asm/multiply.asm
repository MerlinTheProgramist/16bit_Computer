// RAM[2] = RAM[0] * RAM[1]

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

// RAM[2] = 0
@0
D=A
@2
M=D

// Multiplication loop
(LOOP)
    // add RAM[1] to RAM[2]
    @1
    D=M
    @2
    M=M+D

    // Bump down RAM[0]
    @0
    M=M-1

    D=M
    @LOOP // goto LOOP
    D=D;JNE


@2


