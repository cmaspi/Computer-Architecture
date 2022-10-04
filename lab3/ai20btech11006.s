.data

.dword 6

.text
    # x1 has the value n
    lui x3, 0x10000
    lui x4, 0x10000
    lui x2, 0x0
    addi x4 x4 16 #return address
    ld a0 0(x3)
    
    factorial:
        li t1 1
        inner_fac:
            beq a0 x0 exit_fac
            sd a0 0(x2)
            addi a1 t1 0
            jal x1 multiply
            addi t1 a0 0
            ld a0 0(x2)
            addi a0 a0 -1
            bne a0 x0 inner_fac
        exit_fac:
            add a0 t1 x0
            jal EXIT
            
     
    
    multiply:
        add t0 a0 x0 # temp = a0
        li t1 0 # temp2 = 0
        inner_mul:
            beq t0 x0 exit_mul
            add t1 t1 a1
            addi t0 t0 -1
            beq x0 x0 inner_mul

        exit_mul:
            add a0 t1 x0
        jalr x0 x1 0
    
    EXIT:
        sd a0 0(x4)
        
            
        
        
    
     

        