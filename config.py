from dotenv import load_dotenv
import os

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")