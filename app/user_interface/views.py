from flask import Blueprint, jsonify, request, render_template

user_interface_blueprint = Blueprint('user_interface', __name__, template_folder='./templates')


@user_interface_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@user_interface_blueprint.route('/activity/<ip_address>/', methods=['GET'])
def get_ip_activity(ip_address):
    return render_template('ip_activity.html', ip_address=ip_address)