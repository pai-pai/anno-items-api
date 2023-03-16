import os

from app import create_app


app = create_app(os.environ.get("MONGO_URI"))

if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
