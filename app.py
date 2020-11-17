from flask import Flask, request, jsonify

from copy_cat.copy_cat import main_run
from copy_cat.parsers.parser import Parser

app = Flask(__name__)


@app.route('/up')
def up():
    return 'Hello, World!'


@app.route('/validate/org_id/<org_id>/design/<design_name>', methods=['POST'])
def run(org_id, design_name):
    token = request.headers.get("Authorization").removeprefix('Bearer ')
    body = request.data
    ps = Parser()
    ps.errors.clear()

    main_run(ps, token, org_id, design_name, body)
    return jsonify(ps.errors)
