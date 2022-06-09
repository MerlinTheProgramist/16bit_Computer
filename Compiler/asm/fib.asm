
define N 0
define TEMP 1
define F 2
define S 3

define n 11

// set N to n
@n
D=A
@N
M=D

// set F to 0 and S to 1
@F
M=0
@S
M=1

(LOOP)
    // TEMP=F
    // F=F+S
    // S=TEMP  
    @F
    D=M
    @TEMP
    M=D

    @S
    D=M
    @F
    M=M+D

    @TEMP
    D=M
    @S
    M=D
    
    // decrease N
    @N
    M=M-1

    // if N != 0 then continue loop
    //@N
    D=M
    @LOOP
    D;JNE

@F
quit
    