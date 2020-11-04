from enum import Enum
from typing import Optional


class Verdict(Enum):
    wrong_answer = 'Wrong answer'
    compilation_error = 'Compilation error'
    accepted = 'Accepted'
    time_limit = 'Time limit exceeded'
    memory_limit = 'Memory limit exceeded'
    output_limit = 'Output limit exceeded'
    idleness_limit = 'Idleness limit exceeded'
    runtime_error = 'Runtime error'
    restricted_function = 'Restricted function'
    compiling = 'Compiling'


def parse_verdict(verdict: str) -> Optional[Verdict]:
    if verdict.startswith('Runtime error'):
        return Verdict('Runtime error')
    try:
        return Verdict(verdict)
    except ValueError:
        return None
