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
