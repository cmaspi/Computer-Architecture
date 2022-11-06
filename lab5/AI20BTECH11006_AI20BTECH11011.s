.data          # (instead of .data in Ripes)
L1: .word 0 
.word 2 2
.word 1 2 3 4
.word 2 3
.word 1 2 3 4 5 6

# Dishank and Chirag

.text
.global main   # (add this to indicate main is a global function, need not be there in Ripes)
main:
li sp 0
la gp, L1          # loading the address in global pointer
lw a0, 4(x3)       # loading the first dimension of the matrix-1
lw a1, 8(x3)       # loading the second dimension of the matrix-1
mul t0 a0 a1       # calculating number of elements in matrix-1
li t1 4
mul t0 t0 t1       # converting to bytes 
addi gp gp 12
add a4 gp x0       # Matrix-1 pointer
add gp gp t0       # moving to the next dimension inputs


lw a2, 0(gp)
lw a3, 4(gp)
bne a1 a2 ERROR
mul t0 a2 a3
mul t0 t0 t1
addi gp gp 8
add a5 gp x0       # Matrix-2 pointer
add gp gp t0


sw a0 0(gp)        # saving the dimensions of the output matrix
sw a3 4(gp)
addi gp gp 8       # output matrix entries

li t0 0
li t6 4

LOOP1:
    li t1 0
    blt t0 a0 LOOP2
    jal x0 BYE
    LOOP2:
        li t2 0
        li t3 0   # temporary variable to store matrix-3 elements 
        blt t1 a3 LOOP3
        addi t0 t0 1
        jal x0 LOOP1
        LOOP3:
            mul t4 t0 a1
            add t4 t4 t2
            mul t4 t4 t6
            
            mul t5 t2 a3
            add t5 t5 t1
            mul t5 t5 t6
            
            add s0 a4 t4
            add s1 a5 t5
            
            lw s2 0(s0)
            lw s3 0(s1)
            mul s4 s2 s3
            add t3 t3 s4
            
            addi t2 t2 1
            blt t2 a2 LOOP3
            sw t3 0(gp)
            addi gp gp 4
            addi t1 t1 1
            jal x0 LOOP2
            
        
    








#MULTIPLY:
#    li t0 0
#    li t1 -1
#    bge a0, x0, MULTIPLY_INNER
#    li t1 1
#    MULTIPLY_INNER:
#        beq a0 x0 EXIT
#        add t0 t0 a1
#        add a0 a0 t1
#        beq x0 x0 MULTIPLY_INNER
#    EXIT:
#        li t2 -1
#        beq t1 t2 POS
#        sub t0 x0 t0
#        POS:
#            add a0 t0 x0
#            jalr x0 x1 0


ERROR:
    la gp L1
    li t0 1
    sw t0 0(gp)

BYE:
    add x0 x0 x0
    jal x0 BYE