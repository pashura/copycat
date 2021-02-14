from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from copy_cat.copy_cat import CopyCat
from copy_cat.services.td_service import TDService

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/up')
def up():
    """
    GET health status of application.
    ---
    responses:
      200:
        description: Returns {'status':'happy'} if application up and running
    """
    return jsonify({'status': 'happy'})


@app.route('/validate/org_id/<org_id>/design/<design_name>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def run(org_id, design_name):
    cc = CopyCat()

    td_service = TDService()
    design = td_service.get_design(org_id, design_name)
    reversed_design = td_service.get_reversed_design(org_id, design_name)
    cc.run(design, reversed_design, request.data)
    if len(cc.validator.errors_container.errors()):
        return jsonify(cc.validator.errors_container.errors())
    return cc.transformer.result
