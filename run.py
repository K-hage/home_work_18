from app.config import Config
from utils import create_app

if __name__ == '__main__':
    app = create_app(Config())
    app.run(host="localhost", port=8000)
