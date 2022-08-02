import json

import requests
from flask import Blueprint

bp = Blueprint('external', __name__)


@bp.route("/fetch", methods=['GET', 'POST'])
def fetch():
    microservice_result = None
    try:
        response = requests.get('http://localhost:3000/stats').json()
        stats = response['allCourseStatistics']
        microservice_result = "Getting some where"
    except:
        microservice_result = "Could not access external service."

    return microservice_result
