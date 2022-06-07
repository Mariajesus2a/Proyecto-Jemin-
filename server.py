from app import app
from app.controllers import routes

if __name__ == '__main__':
    app.run(debug=True, host="192.168.100.3")
