from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_driver import DatabaseDriver


logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class CarDetails(enum.Enum):
    VIN = "vin"
    Make = "make"
    Model = "model"
    Year = "year"
    
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
        
        self._car_details = {
            CarDetails.VIN: "",
            CarDetails.Make: "",
            CarDetails.Model: "",
            CarDetails.Year: ""
        }

    def get_car_str(self):
        car_str =""
        for key, value in self._car_details.items():
            car_str += f"{key}: {value}\n"

        return car_str
    

        

    @llm.ai_callable(description="lookup a car by its vin")
    def lookup_car(self, vin: Annotated[str, llm.TypeInfo(description="the vin of the car to lookup")]):
        logger.info("lookup car - vin: %s", vin)

        result = DB.get_car_by_vin(vin)
        if result is None:
            return "Car not found"
        
        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.Make: result.make,
            CarDetails.Model: result.model,
            CarDetails.Year: result.year

        }

        car_str =""
        for key, value in self._car_details.items():
            car_str += f"{key}: {value}\n"

        return f"The car details are: {self.get_car_str()}"
    

    @llm.ai_callable(description="lookup a car by its vin")
    def lookup_car(self, vin: Annotated[str, llm.TypeInfo(description="the vin of the car to lookup")]):




