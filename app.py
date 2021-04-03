import json

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from copy_cat.copy_cat import CopyCat
from copy_cat.scripts.reports.parcels import make_report
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
    """
    Run validation and transformation
    ---
    produces:
      application/json
    parameters:
    - name: org_id
      in: query
      description: Organization ID
      required: true
      schema:
       type: string
    - name: design_name
      in: query
      description: Design Name
      required: true
      schema:
       type: string
    - name: body
      in: body
    responses:
     200:
       description: returns list with either validation errors or transformation result
    """

    cc = CopyCat()
    td_service = TDService()
    design = td_service.get_design(org_id, design_name)
    reversed_design = td_service.get_reversed_design(org_id, design_name)
    result = cc.run(json.loads(design), json.loads(reversed_design), request.data)
    if len(cc.validator.errors_container.errors()):
        return jsonify(cc.validator.errors_container.errors())
    return jsonify(result)


@app.route("/validate/org_id/<org_id>/design/<design_name>/report", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def run_report(org_id, design_name):
    """
    Run report
    ---
    produces:
      application/json
    parameters:
    - name: org_id
      in: query
      description: Organization ID
      required: true
      schema:
       type: string
    - name: design_name
      in: query
      description: Design Name
      required: true
      schema:
       type: string
    - name: body
      in: body
    responses:
     200:
       description: returns list of object for each row of report table
    """
    td_service = TDService(environment="prod")
    design = td_service.get_design(org_id, design_name)
    reversed_design = td_service.get_reversed_design(org_id, design_name)
    report = make_report(design, reversed_design, json.loads(request.data))
    return jsonify(report)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
