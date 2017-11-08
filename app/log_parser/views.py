from flask import Blueprint, jsonify, request, render_template

log_parser_blueprint = Blueprint('log_parser', __name__, template_folder='./templates')


@log_parser_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@log_parser_blueprint.route('/activity/<ip_address>/', methods=['GET'])
def get_ip_activity(ip_address):
    return render_template('ip_activity.html', ip_address=ip_address)
