
from route import app
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

port = getenv("PORT")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=port)