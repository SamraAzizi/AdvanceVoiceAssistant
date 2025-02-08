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

    def get_car_str(self):
        return "\n".join(f"{key.value}: {value}" for key, value in self._car_details.items())

    async def generate_response(self, prompt):
        """Generates a response from Ollama based on the given prompt."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_API_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "temperature": 0.8},
            )
            response_json = response.json()
            return response_json.get("response", "Error generating response.")

    async def lookup_car(self, vin: str):
        """Look up a car by its VIN."""
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
