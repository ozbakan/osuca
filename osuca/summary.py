from webbrowser import get
import requests
from flask import Blueprint, render_template

from osuca.db import get_db

bp = Blueprint('summary', __name__)


@bp.route("/fetch", methods=['GET', 'POST'])
def fetch():
    db = get_db()

    microservice_result = None
    try:
        response = requests.get('http://localhost:3000/stats').json()
        stats = response['allCourseStatistics']
        microservice_result = "Getting some where..."
    except:
        microservice_result = "Could not access summary service."

    return render_template("summary.html",
                           course=sorted(db.course()),
                           microservice_result=microservice_result)
