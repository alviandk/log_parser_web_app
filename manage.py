import json
import unittest

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.log_parser.models import IpAddress, Entry, Country

app = create_app()
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    
    db.session.commit()


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def init_db():
    """Initialize data if db is empty"""

    if not Country.query.first():
        print('Populating Countries Data')
        with open('countries.json') as countries_json:
            data = json.load(countries_json)
            for entry in data:
                db.session.add(Country(name=entry['name'], code=entry['code']))
                db.session.commit()

    if not IpAddress.query.first():
        print('Populating IP Address Data')
        # example data for development only
        country = Country.query.filter_by(code='US').first()
        ip_address = IpAddress(address='64.233.161.99')
        country.ip_addresses.append(ip_address)
        db.session.add(country)
        db.session.commit()


if __name__ == '__main__':
    manager.run()
