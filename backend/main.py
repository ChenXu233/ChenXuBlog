from uvicorn import run

from backend import app as APP

if __name__ == "__main__":
    run(APP, host="127.0.0.1", port=8080)
