from flask import Flask, jsonify, request

from copy_cat.copy_cat import main_run
from copy_cat.parsers.parser import Parser
from copy_cat.services.identity_service import IdentityService

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
    is_.get_identity_token()

    token = request.headers.get("Authorization").removeprefix('Bearer ')
    body = request.data
    ps = Parser()
    ps.errors.clear()  # TODO: remove

    main_run(ps, token, org_id, design_name, body)
    return jsonify(ps.errors)
