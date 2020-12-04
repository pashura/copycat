from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from copy_cat.copy_cat import CopyCat
from copy_cat.services.identity_service import IdentityService
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


@app.route('/check/design/<design_name>', methods=['GET'])
@cross_origin()
def check_design(design_name):
    # TODO: Move logic to get design to copycat app? ??
    identity_service = IdentityService()
    token = identity_service.get_identity_token()['access_token']
    td_service = TDService('test', token)
    design = td_service.search_design(design_name)

    return jsonify({"designsInfo": design})


@app.route('/validate/org_id/<org_id>/design/<design_name>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def run(org_id, design_name):
    cc = CopyCat()

    # TODO: Move logic to get design to copycat app? ??
    identity_service = IdentityService()
    token = identity_service.get_identity_token()['access_token']
    td_service = TDService('test', token)
    design = td_service.get_reversed_design(org_id, design_name)
    cc.run(design, request.data)
    return jsonify(cc.validator.errors_container.errors())
