# File to start application
from applicationfiles import app
from dotenv import load_dotenv
import os

try:
    load_dotenv()
except Exception as error:
    # Need to add error.htm handle this part
    print(f"Error loading .env file: {error}")

if __name__ == "__main__":
    app.run(debug=False)