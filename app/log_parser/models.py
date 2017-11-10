from app import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(2), unique=False, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)


    def __repr__(self):
        return self.name


class IpAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(32), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)
    country = db.relationship('Country', backref=db.backref('ip_addresses', lazy=True))
    hits = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return self.address


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address_id = db.Column(db.Integer, db.ForeignKey('ip_address.id'), nullable=False)
    ip_address = db.relationship('IpAddress', backref=db.backref('entries', lazy=True))
    raw_log = db.Column(db.Text, nullable=False)
    is_sqli = db.Column(db.Boolean, nullable=False, default=False)
    is_rfi = db.Column(db.Boolean, nullable=False, default=False)
    is_web_shell = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return '<%r Entry>' % self.ip_address
