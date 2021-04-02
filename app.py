import json

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from copy_cat.copy_cat import CopyCat
from copy_cat.scripts.reports.parcels import make_report
from copy_cat.services.parcel_service import ParcelService
from copy_cat.services.td_service import TDService

app = Flask(__name__)
CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/up")
def up():
    """
    GET health status of application.
    ---
    responses:
      200:
        description: Returns {'status':'happy'} if application up and running
    """
    return jsonify({"status": "happy"})


@app.route("/validate/org_id/<org_id>/design/<design_name>", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def run(org_id, design_name):
    cc = CopyCat()
    td_service = TDService()
    design = td_service.get_design(org_id, design_name)
    reversed_design = td_service.get_reversed_design(org_id, design_name)
    result = cc.run(json.loads(design), json.loads(reversed_design), request.data)
    if len(cc.validator.errors_container.errors()):
        return jsonify(cc.validator.errors_container.errors())
    return jsonify(result)


@app.route("/parcel_uid/<parcel_uid>", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def get_parcel(parcel_uid):
    ps = ParcelService()
    return ps.get_parcel_data(parcel_uid)


@app.route("/validate/org_id/<org_id>/design/<design_name>/report", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def run_report(org_id, design_name):
    td_service = TDService(environment="prod")
    design = td_service.get_design(org_id, design_name)
    reversed_design = td_service.get_reversed_design(org_id, design_name)
    report = make_report(design, reversed_design, json.loads(request.data))
    return jsonify(report)
