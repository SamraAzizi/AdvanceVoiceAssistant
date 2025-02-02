from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_driver import DatabaseDriver


logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class CarDetail(enum.Enum):
    VIN = "vin"
    Make = "make"
    Model = "model"
    Year = "year"
    
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()