import os
from app import app

if __name__ == '__main__':
    app.run(debug=app.app.config['DEBUG'], host=os.environ['HTTP_HOST_ADDRESS'])