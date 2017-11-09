from app import db


class IpAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(32), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return self.ip


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address_id = db.Column(db.Integer, db.ForeignKey('ip_address.id'), nullable=False)
    ip_address = db.relationship('IpAddress', backref=db.backref('entries', lazy=True))
    raw_log = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return '<%r Entry>' % self.ip_address