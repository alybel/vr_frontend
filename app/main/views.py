from flask import render_template
from flask import send_from_directory
import os
from . import main

@main.route('/')
def index():
    return render_template('index.html')

