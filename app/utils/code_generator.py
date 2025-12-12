import string
from typing import List

ALPHABET = string.ascii_letters + string.digits


class CodeGenerator:
    """Random Base62 code generator."""

    def __init__(self, length: int = 6) -> None:
        """Initialize CodeGenerator.

        Args:
            length (int): Default length of generated codes.

        Returns:
            None

        Raises:
            None
        """
        self.length = length

    @staticmethod
    def generate(num: int) -> str:
        """Generate a base62 string from integer.

        Args:
            num (int): Integer to encode.

        Returns:
            str: Base62 encoded string.

        Raises:
            None
        """
        if num == 0:
            return ALPHABET[0]
        arr: List[str] = []
        base = len(ALPHABET)
        while num:
            num, rem = divmod(num, base)
            arr.append(ALPHABET[rem])
        arr.reverse()
        return "".join(arr)

    @staticmethod
    def decode(code: str) -> int:
        """Decode a Base62 string back to integer.

        Args:
            code (str): Code to decode.

        Returns:
            int: Decoded integer.

        Raises:
            ValueError: If character not in alphabet.
        """
        base = len(ALPHABET)
        num = 0
        for char in code:
            num = num * base + ALPHABET.index(char)
        return num
