import json
import os
import pygeoip
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .models import IpAddress, Entry, Country
from app import db

log_parser_blueprint = Blueprint('log_parser', __name__, template_folder='./templates')


@log_parser_blueprint.route('/', methods=['GET'])
def index():
    # menu
    return render_template('index.html')


@log_parser_blueprint.route('/entry/', methods=['GET'])
def get_entry():
    entries = Entry.query.all()

    return render_template('entry.html', entries=entries)


@log_parser_blueprint.route('/ip_address/', methods=['GET'])
def get_ip_address():
    ips = IpAddress.query.all()

    return render_template('ip_address.html', ips=ips)


@log_parser_blueprint.route('/ip_address_ajax/', methods=['GET'])
def get_ip_address_ajax():
    q = request.args.get('term', '-')
    ips = IpAddress.query.filter(IpAddress.address.startswith(q)).all()
    result = []
    for ip in ips:
        result.append(ip.address)

    return json.dumps(result)


@log_parser_blueprint.route('/entry/<ip_address>/', methods=['GET'])
def get_ip_entry(ip_address):
    ip_address = IpAddress.query.filter_by(address=ip_address).first_or_404()

    return render_template('ip_entry.html', ip_address=ip_address)


@log_parser_blueprint.route('/upload-log-file/', methods=['GET', 'POST'])
def upload_log_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join('/tmp', filename)
            file.save(filename)

            flash('Upload Success')
            entries = 0
            with open(filename, 'r') as uploaded_file:
                gi = pygeoip.GeoIP('GeoIP.dat')
                for entry in uploaded_file:
                    entries += 1
                    # extract ip from a log entry, eg result: ['172.17.100.8', '198.72.2.70']
                    ip_addresses = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', entry)

                    client_ip = ip_addresses[-1]
                    ip_address = IpAddress.query.filter_by(address=client_ip).first()

                    # check if ip_address already on db
                    if ip_address:
                        ip_address.hits = ip_address.hits + 1
                        db.session.commit()
                    else:
                        country_code = gi.country_code_by_addr(client_ip)
                        country = Country.query.filter_by(code=country_code).first()
                        db.session.add(IpAddress(address=client_ip, country=country))
                        ip_address = IpAddress.query.filter_by(address=client_ip).first()
                        db.session.commit()

                    split_entry = entry.split(' ')
                    url_query = split_entry[5]

                    is_sqli = check_attack('sqli', url_query)
                    is_rfi = check_attack('rfi', url_query)
                    is_web_shell = check_attack('web_shell', url_query)

                    db.session.add(
                        Entry(
                            ip_address=ip_address,
                            raw_log=entry,
                            is_rfi=is_rfi,
                            is_sqli=is_sqli,
                            is_web_shell=is_web_shell
                        )
                    )
                    db.session.commit()

            return redirect(url_for('log_parser.upload_log_file'))

    return render_template('upload_file.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['log']


def check_attack(attack_type, url_query):
    if url_query == '-':
        return False
    else:
        attack_dict = {
            'sqli': ['union', 'system\(', 'eval(', 'group_concat',
                     'column_name', 'order by', 'insert into', 'select', 'load_file', 'concat',
                     '@@version'],
            'rfi': ['file='],
            'web_shell': ['cmd=']
        }
        result = False
        for keyword in attack_dict[attack_type]:
            if keyword.upper() in url_query.upper():
                result = True
        return result
