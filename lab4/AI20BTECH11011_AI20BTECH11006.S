.section .data          # (instead of .data in Ripes)
L1: .word 1000000 #delay count to be loaded from memory

# Dishank and Chirag

.section .text
.global main   # (add this to indicate main is a global function, need not be there in Ripes)
main:
la x3, L1          #this will load the ADDRESS of the data section in x3
li x7, 0x10012004
li x18, 5 # num times to glow LED
li x19, 0 # turn-off LED


sw x19, 0(x7)
sw x20, 4(x7)



loop:
    sw x20, 8(x7)
    jal x1, delay
    sw x19, 8(x7)
    jal x1, delay
    beq x0, x0, loop

delay:
    lw x4, 0(x3)
    delay_inner:
        addi x4, x4, -1
        bne x4, x0, delay_inner
    exit:
        jalr x0, x1, 0



#YOUR CODE FOLLOWS HERE. The ADDRESS of the data segment is available in x3

#At the end, have a while(1) loop, as shown below
Lwhile1: j Lwhile1
