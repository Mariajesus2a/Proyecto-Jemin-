from flask import Flask
import pathlib
UPLOAD_FOLDER = f'{pathlib.Path(__file__).parent.resolve()}/static/uploads'
app = Flask(__name__)
app.secret_key = "shhh"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
