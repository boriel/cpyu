import sys
from typing import List


class CPU:
    SP: int = None  # Stack pointer
    PC: int = None  # Program Counter
    BP: int = None  # Base Pointer
    memory: List[int] = None

    def __init__(self, word_size=16, mem_size=1024 * 1024):
        self.PC = 0
        self.BP = 0
        self.memory = [0] * mem_size
        self.word_size: int = word_size
        self.mask: int = (1 << word_size) - 1  # Mask
        self.SP = len(self.memory)  # Stack Ptr initialized to top of memory
        self.nibbles: int = word_size // 4  # number of nibbles per word

    @staticmethod
    def log(msg: str):
        sys.stdout.write('{}\n'.format(msg))

    def panic(self, msg: str):
        """ Execution exception ("kernel panic", "guru meditation")
        """
        self.log('Execution fault:')
        self.log(msg)
        self.log(('PC = 0x%%0%iX | %%i' % self.nibbles) % (self.PC, self.PC))
        self.log(('SP = 0x%%0%iX | %%i' % self.nibbles) % (self.SP, self.SP))
        self.log('Execution halted')
        sys.exit(1)

    def to_word(self, value: int) -> int:
        """ Applies bit-mask to the given value
        """
        return value & self.mask

    def push(self, value: int):
        """ Pushes a value in the stack
        """
        self.SP -= 1
        if self.SP < 0:
            self.panic("Stack overflow")

        self.memory[self.SP] = self.to_word(value)

    def pop(self) -> int:
        if self.SP >= len(self.memory):
            self.panic("Stack underflow")

        result = self.memory[self.SP]
        self.SP += 1
        return result

    # Base pointer (BP) instructions
    def ld_bp_sp(self):
        """ Performs BP <- SP
        """
        self.BP = self.SP

    def ld_sp_bp(self):
        """ Performs SP <- BP
        """
        self.SP = self.SP

    def push_bp(self):
        self.push(self.BP)

    def pop_bp(self):
        self.BP = self.pop()

    # Arithmetic integer 2-ary operations
    def add(self):
        self.push(self.pop() + self.pop())

    def sub(self):
        b = self.pop()
        a = self.pop()
        self.push(a - b)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        b = self.pop()
        a = self.pop()
        self.push(a // b)

    def mod(self):
        b = self.pop()
        a = self.pop()
        self.push(a % b)

    # bitwise integer 2-ary operations
    def and_(self):
        self.push(self.pop() & self.pop())

    def or_(self):
        self.push(self.pop() | self.pop())

    def xor(self):
        self.push(self.pop() ^ self.pop())

    # Arithmetic and bitwise unary operations
    def neg(self):
        """ Negates the top of the stack
        """
        self.push(-self.pop())

    def cpl(self):
        """ Complements bits top of the stack
        """
        self.push(self.pop() ^ self.mask)


