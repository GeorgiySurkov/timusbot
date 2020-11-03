from enum import Enum


class Verdict(Enum):
    WA = 'Wrong answer'
    CE = 'Compilation error'
    AC = 'Accepted'
    TL = 'Time limit exceeded'
    ML = 'Memory limit exceeded'
    OL = 'Output limit exceeded'
    IL = 'Idleness limit exceeded'
    RE = 'Runtime error'
    RF = 'Restricted function'
    C = 'Compiling'
