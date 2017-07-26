from application import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(128), index=True, unique=False)
    host_name = db.Column(db.String(128), index=True, unique=False)
    last_login = db.Column(db.DateTime())
    login_success = db.Column(db.Boolean())

    def __init__(self, app_name, ip_address, host_name, last_login, login_success):
        self.ip_address = ip_address
        self.host_name = host_name
        self.last_login = last_login
        self.login_success = login_success

    def __repr__(self):
        return self.ip_address


class AppData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(128), index=True, unique=False)
    ip_address = db.Column(db.String(128), index=True, unique=False)
    host_name = db.Column(db.String(128), index=True, unique=False)
    permission = db.Column(db.Boolean())
    last_login = db.Column(db.DateTime())

    def __init__(self, app_name, ip_address, host_name, permission, last_login):
        self.app_name = app_name
        self.ip_address = ip_address
        self.host_name = host_name
        self.permission = permission
        self.last_login = last_login
#
#     def __repr__(self):
#         return ','.join([self.app_name, self.ip_address, self.host_name, str(self.permission), str(self.last_login)])