import string

ALPHABET = string.ascii_letters + string.digits


class CodeGenerator:
    """Base62 code generator and decoder.

    Attributes:
        length (int): Default length of generated codes.
    """

    def __init__(self, length: int = 6) -> None:
        self.length = length

    @staticmethod
    def decode(code: str) -> int:
        """Decode a Base62 string back to integer."""
        base = len(ALPHABET)
        num = 0
        for char in code:
            num = num * base + ALPHABET.index(char)
        return num