import _sqlite3
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Car:
    vin: str
    make: str
    model: str
    year: int