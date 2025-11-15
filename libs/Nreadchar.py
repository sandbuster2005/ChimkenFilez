import termios
import sys
from copy import copy
from select import select
from io import StringIO


class ReadChar:
    """
    A ContextManager allowing for keypress collection without requiring the user to
    confirm presses with ENTER. Can be used non-blocking while inside the context.
    """

    def __init__(self) -> None:
        self.interrupt_key = ["\x03"]  #ctrl C
        self._buffer = StringIO()

    def __enter__(self) -> "ReadChar":
        self.fd = sys.stdin.fileno()
        term = termios.tcgetattr(self.fd)
        self.old_settings = copy(term)

        term[3] &= ~(
                termios.ICANON  # don't require ENTER
                | termios.ECHO  # don't echo
                | termios.IGNBRK
                | termios.BRKINT
        )
        term[6][termios.VMIN] = 0  # immediately process every input
        term[6][termios.VTIME] = 0
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, term)
        return self

    def __exit__(self, type, value, traceback) -> None:
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_settings)

    def __update(self) -> None:
        """
        check stdin and update the internal buffer if it holds data
        """
        if sys.stdin in select([sys.stdin], [], [], 0)[0]:
            pos = self._buffer.tell()
            data = sys.stdin.read()
            self._buffer.write(data)
            self._buffer.seek(pos)

    @property
    def key_waiting(self) -> bool:
        """
        True if a key has been pressed and is waiting to be read. False if not.
        """
        self.__update()
        pos = self._buffer.tell()
        next_byte = self._buffer.read(1)
        self._buffer.seek(pos)
        return bool(next_byte)

    def char(self) -> str:
        """
        Reads a single char from the input stream and returns it as a string of
        length one. Does not require the user to press ENTER.
        """
        self.__update()
        return self._buffer.read(1)

    def key(self) -> str:
        """
        Reads a keypress from the input stream and returns it as a string. Key-pressed
        consisting of multiple characters will be read completely and be returned as a
        string matching the definitions in `key.py`.
        Does not require the user to press ENTER.
        """
        self.__update()

        c1 = self.char()

        if c1 in self.interrupt_key:
            raise KeyboardInterrupt

        if c1 != "\x1B":
            return c1

        c2 = self.char()
        if c2 not in "\x4F\x5B":
            return c1 + c2

        c3 = self.char()
        if c3 not in "\x31\x32\x33\x35\x36":
            return c1 + c2 + c3

        c4 = self.char()
        if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
            return c1 + c2 + c3 + c4

        c5 = self.char()
        return c1 + c2 + c3 + c4 + c5
