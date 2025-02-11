import httpx
import enum
import logging
import os
from db_driver import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

# Ollama API Configuration
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")  # Use any other Ollama model if needed

class CarDetails(enum.Enum):
    VIN = "vin"
    Make = "make"
    Model = "model"
    Year = "year"
    
class AssistantFnc:
    def __init__(self):
        self._car_details = {
            CarDetails.VIN: "",
            CarDetails.Make: "",
            CarDetails.Model: "",
            CarDetails.Year: ""
        }

 

        return f"The car details are:\n{self.get_car_str()}"

    async def get_car_details(self):
        """Get the details of the current car."""
        logger.info("get car details")
        return f"The car details are:\n{self.get_car_str()}"

    async def create_car(self, vin: str, make: str, model: str, year: int):
        """Create a new car."""
        logger.info("create car - vin : %s, make: %s, model: %s, year: %s", vin, make, model, year)

        result = DB.create_car(vin, make, model, year)
        if result is None:
            return "Failed to create car"

        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.Make: result.make,
            CarDetails.Model: result.model,
            CarDetails.Year: result.year
        }

        return "Car created!"

    def has_car(self):
        """Check if the car details exist."""
        return bool(self._car_details[CarDetails.VIN])
