from dotenv import load_dotenv
import motor.motor_asyncio

from decouple import config

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"))
conn = client.calculos_trabajador