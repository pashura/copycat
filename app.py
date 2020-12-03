from flask import Flask, jsonify, request

from copy_cat.copy_cat import main_run
from copy_cat.services.identity_service import IdentityService
from copy_cat.validators.validator import Validator

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
    is_ = IdentityService()
    token = is_.get_identity_token()

    validator = Validator()
    validator.errors.clear()  # TODO: remove

    main_run(validator, token['access_token'], org_id, design_name, request.data)
    return jsonify(validator.errors)
