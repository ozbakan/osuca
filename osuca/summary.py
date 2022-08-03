from re import M
from webbrowser import get
import requests
from flask import Blueprint, render_template, request, flash

from osuca.db import get_db

bp = Blueprint('summary', __name__)


@bp.route("/fetch", methods=['GET', 'POST'])
def fetch():

    db = get_db()
    microservice_result = None
    try:
        response = requests.get('http://localhost:3000/stats').json()
        microservice_result = prepare(
            response['allCourseStatistics'], db.course())
    except:
        flash("Could not access summary service.")

    selection_label = "All Courses"
    if request.method == 'POST' and request.form['course'] != "All Courses":
        selection_label = request.form['course']
        selection = db.course(selection_label)
        microservice_result = db.course_combination_aggregate(selection)

    return render_template("summary.html",
                           selection_label=selection_label,
                           course=sorted(db.course()),
                           microservice_result=microservice_result)


def prepare(response, course):
    result = {}
    for r in response:
        for c in course:
            if r['course'] == c.id:
                stats = r['statistics'][0]
                ad = stats['averageDifficulty']
                ld = stats['lowestDifficulty']
                hd = stats['highestDifficulty']
                result[c.subject + ' ' + c.id + ' - ' + c.name] = (ad, ld, hd)

    result = sorted(result.items(), key=lambda item: item[1][0], reverse=True)
    return result 
