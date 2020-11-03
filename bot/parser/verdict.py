from enum import Enum
from typing import Optional


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


def parse_verdict(verdict: str) -> Optional[Verdict]:
    if verdict.startswith('Runtime error'):
        return Verdict('Runtime error')
    try:
        return Verdict(verdict)
    except ValueError:
        return None
