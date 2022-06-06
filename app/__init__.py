from flask import Flask
UPLOAD_FOLDER = '/Users/mariajesusarancibia/Documents/codindojo/work/proyecto_pp/app_jemin/app/static/uploads'
app = Flask(__name__)
app.secret_key = "shhh"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
