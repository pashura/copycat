from flask import Flask, jsonify, request

from copy_cat.copy_cat import CopyCat
from copy_cat.services.identity_service import IdentityService
from copy_cat.services.td_service import TDService

app = Flask(__name__)


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
def check_design(design_name):
    return jsonify({"design_name": design_name})


@app.route('/validate/org_id/<org_id>/design/<design_name>', methods=['POST'])
def run(org_id, design_name):
    cc = CopyCat()

    # TODO: Move logic to get design to copycat app? ??
    identity_service = IdentityService()
    token = identity_service.get_identity_token()['access_token']
    td_service = TDService('test', token)
    design = td_service.get_reversed_design(org_id, design_name)
    cc.run(design, request.data)
    return jsonify(cc.errors)
