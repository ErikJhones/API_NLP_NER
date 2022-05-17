import uvicorn
import unittest
import prospector.run as prosp
from dotenv import load_dotenv

load_dotenv()


def run_development_server():
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, workers=2)


def run_tests():
    unittest.main(module='tests', verbosity=3)


def run_static_analysis():
    prosp.main()
