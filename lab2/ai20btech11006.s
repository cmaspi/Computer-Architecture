.data

.dword 6

.text
    # x1 has the value n
    lui x1, 0x10000
    ld x1, 0(x1)
    lui x4, 0x10000
    addi x4, x4, 256
    lui x5, 0x10000
    addi x5, x5, 16 # address for sum
    addi x6, x0, 0 # sum

    # x2 will be the iterator
    # 0 to n-1
    addi x2, x0, 0
    # x3 will contain the square number
    # at current iteration
    addi x3, x0, 0
    # while x2 <= x1(n)
        # x2 += 1 [addi x2, x2, 1]
        # x3 += x3 + 2*x2-1
        # add x3, x3, x3
        # add x3, x3, x2
        # add x3, x3, x2
        # addi x3, x3, -1
        
    LOOP:
        bge x2, x1, EXIT
        addi x2, x2, 1
        add x3, x3, x2
        add x3, x3, x2
        addi x3, x3, -1
        sd x3, 0(x4)
        add x6, x6, x3
        sd x6, 0(x5)
        addi x4, x4, 8
        beq x0, x0, LOOP # true condition

   EXIT:
        addi x0, x0, 1 # junk statement
        

        