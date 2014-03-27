from datetime import datetime
import os

from flask import Flask, render_template, jsonify

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FOLDER = os.path.join(PROJECT_PATH, 'templates')
STATIC_FOLDER = os.path.join(PROJECT_PATH, 'static')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER)

app.config.from_object('home.dash.config')

from home.ts import SeriesGenerator


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/data/<series>/<start>/<end>/')
def data(series, start, end):

    series_name = series
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    generator = SeriesGenerator(series_name, start_dt, end_dt)

    return jsonify(data=generator.all())
