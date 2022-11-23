HEX_INSTRUCTIONS = '''100001b7
10000237
00000137
01020213
0001b503
00100313
02050063
00a13023
00030593
01c000ef
00050313
00013503
fff50513
fe0512e3
00030533
024000ef
000502b3
00000313
00028863
00b30333
fff28293
fe000ae3
00030533
00008067
00a23023'''
HEX_INSTRUCTIONS = HEX_INSTRUCTIONS.split('\n')


BINARY_INSTRUCTIONS = []
for instruction in HEX_INSTRUCTIONS:
    temp = eval('0x'+instruction)
    BINARY_INSTRUCTIONS.append(f'{temp:0>32b}')


def get_rs1(instruction: str) -> str:
    """
    returns the rs1 register from the binary instruction

    Args:
        instruction (str): binary instruction

    Returns:
        str: rs1 register
    """
    temp = int(instruction[12:17], 2)
    return f'x{temp}'


def get_rs2(instruction: str) -> str:
    """
    returns the rs2 register from the binary instruction

    Args:
        instruction (str): binary instruction

    Returns:
        str: rs2 register
    """
    temp = int(instruction[7:12], 2)
    return f'x{temp}'


def get_rd(instruction: str) -> str:
    """
    returns the rd register from the binary instruction

    Args:
        instruction (str): binary instruction

    Returns:
        str: rd register
    """
    temp = int(instruction[20:25], 2)
    return f'x{temp}'


def handle_imm(imm: str, sign: bool) -> int:
    """
    handles the immediate value for sign

    Args:
        imm (str): immediate bit string
        sign (bool): whether to consider sign or not

    Returns:
        int: the value of immediate
    """
    neg = imm[0] == '1'
    if sign and neg:
        imm = imm.replace('1', '2').replace('0', '1').replace('2', '0')
    imm = int(imm, 2)
    if sign & neg:
        imm = -imm
        imm -= 1
    return imm


def parse_R(instruction: str) -> str:
    """
    Handles the R type instructions

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    funct3_1 = {
        0x0: 'add',
        0x4: 'xor',
        0x6: 'or',
        0x7: 'and',
        0x1: 'sll',
        0x5: 'srl',
    }
    funct3_2 = {
        0x0: 'sub',
        0x5: 'sra'
    }

    funct7 = int(instruction[:7], 2)
    funct3 = int(instruction[17:20], 2)
    if funct7 == 0:
        what = funct3_1[funct3]
    else:
        what = funct3_2[funct3]

    rd = get_rd(instruction)
    rs1 = get_rs1(instruction)
    rs2 = get_rs2(instruction)

    return f'{what} {rd}, {rs1}, {rs2}'


def parse_I1(instruction: str) -> str:
    """
    Handles the I type instructions (Category-1)

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    funct3 = {
        0x0: 'addi',
        0x4: 'xori',
        0x6: 'ori',
        0x7: 'andi',
        0x1: 'slli',
        0x2: 'slti'
    }
    __funct3__ = int(instruction[17:20], 2)
    bits_imm = instruction[:12]
    if __funct3__ == 0x5:
        if int(bits_imm[:6], 2):
            operator = 'srai'
        else:
            operator = 'srli'
    else:
        operator = funct3[__funct3__]
    rs = get_rs1(instruction)
    rd = get_rd(instruction)
    if __funct3__ == 0x5 or __funct3__ == 0x1:
        imm = int(bits_imm[-6:], 2)
    else:
        imm = handle_imm(bits_imm, True)
    return f'{operator} {rd}, {rs}, {imm}'


def parse_I2(instruction: str) -> str:
    """
    Handles the I type instructions (Category-2)

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    funct3 = {
        0x0: 'lb',
        0x1: 'lh',
        0x2: 'lw',
        0x3: 'ld',
        0x4: 'lbu',
        0x5: 'lhu',
        0x6: 'lwu'
    }
    __funct3__ = int(instruction[17:20], 2)
    bits_imm = instruction[:12]
    operator = funct3[__funct3__]
    rs = get_rs1(instruction)
    rd = get_rd(instruction)
    imm = handle_imm(bits_imm, True)
    return f'{operator} {rd}, {imm}({rs})'


def parse_I3(instruction: str) -> str:
    """
    Handles the I type instructions (Category-1)

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    rs1 = get_rs1(instruction)
    rd = get_rd(instruction)
    bits_imm = instruction[:12]
    imm = handle_imm(bits_imm, True)
    return f'jalr {rd}, {rs1}, {imm}'


def parse_S(instruction: str) -> str:
    """
    Handles the S type instructions

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    funct3 = {
        0x0: 'sb',
        0x1: 'sh',
        0x2: 'sw',
        0x3: 'sd'
    }
    __funct3__ = int(instruction[17:20], 2)
    bits_imm = instruction[:7]+instruction[20:25]
    operator = funct3[__funct3__]
    rs1 = get_rs1(instruction)
    rs2 = get_rs2(instruction)
    imm = handle_imm(bits_imm, True)
    return f'{operator} {rs2}, {imm}({rs1})'


def parse_U(instruction: str) -> str:
    """
    Handles the U type instructions

    Args:
        instruction (str): binary string (instruction)

    Returns:
        str: the disassembled instruction
    """
    rd = get_rd(instruction)
    bits_imm = instruction[:20]
    imm = handle_imm(bits_imm, True)
    return f'lui {rd}, {imm}'


def parse_B(instruction: str,
            line_num: int,
            labels: dict) -> str:
    """
    parses the B type instruction

    Args:
        instruction (str): binary string
        line_num (int): line number of the instruction
        labels (dict): the dictionary containing all the labels
        and associated line numbers

    Returns:
        str: the disassembled instruction
    """
    funct3 = {
        0x0: 'beq',
        0x1: 'bne',
        0x4: 'blt',
        0x5: 'bge',
        0x6: 'bltu',
        0x7: 'bgeu'
    }
    __funct3__ = int(instruction[17:20], 2)
    operator = funct3[__funct3__]
    rs2 = get_rs2(instruction)
    rs1 = get_rs1(instruction)
    bits_imm = (instruction[0]+instruction[-8] +
                instruction[1:7]+instruction[-12:-8])
    imm = handle_imm(bits_imm[:-1], True)
    if line_num+imm not in labels:
        label_counter = len(labels)+1
        label = f'L{label_counter}'
        labels[line_num+imm] = label
    else:
        label = labels[line_num+imm]
    return f'{operator} {rs1}, {rs2}, {label}'


def parse_J(instruction: str,
            line_num: int,
            labels: dict) -> str:
    """
    parses the J type instruction

    Args:
        instruction (str): binary string
        line_num (int): line number of the instruction
        labels (dict): the dictionary containing all the labels
        and associated line numbers

    Returns:
        str: the disassembled instruction
    """
    rd = get_rd(instruction)
    bits_imm = (instruction[0]+instruction[12:20] +
                instruction[11]+instruction[1:11])
    imm = handle_imm(bits_imm[:-1], True)
    if line_num+imm not in labels:
        label_counter = len(labels)+1
        label = f'L{label_counter}'
        labels[line_num+imm] = label
    else:
        label = labels[line_num+imm]
    return f'jal {rd}, {label}'


def handler(BINARY_INSTRUCTION: list):
    """
    Handler for the instructions, it selects which type
    of instruction is given, then chooses the parse function
    accordingly

    Args:
        BINARY_INSTRUCTION (list): list of instructions
        in binary string format

    Returns:
        list: list of instructions
    """
    OPCODE = {
        '0110011': 'R',
        '0010011': 'I1',
        '0000011': 'I2',
        '0100011': 'S',
        '1100011': 'B',
        '1101111': 'J',
        '1100111': 'I3',
        '0110111': 'U',
    }
    labels = {}
    TEXT_INSTRUCTIONS = []
    for line_num, instruction in enumerate(BINARY_INSTRUCTION):
        opcode = instruction[-7:]
        instruction_type = OPCODE[opcode]
        match instruction_type:
            case 'R':
                output = parse_R(instruction)
            case 'I1':
                output = parse_I1(instruction)
            case 'I2':
                output = parse_I2(instruction)
            case 'I3':
                output = parse_I3(instruction)
            case 'S':
                output = parse_S(instruction)
            case 'U':
                output = parse_U(instruction)
            case 'B':
                output = parse_B(instruction, line_num, labels)
            case 'J':
                output = parse_J(instruction, line_num, labels)
        TEXT_INSTRUCTIONS.append(output)
    for line_num in sorted(labels.keys()):
        TEXT_INSTRUCTIONS[line_num] = (labels[line_num]
                                       + ':\n'
                                       + TEXT_INSTRUCTIONS[line_num])
    return TEXT_INSTRUCTIONS


print('\n'.join(handler(BINARY_INSTRUCTIONS)))
