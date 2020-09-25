from flask import Flask
from config import Config
from flask import render_template

app = Flask(__name__)
app.config.from_object(Config)

from app import routes