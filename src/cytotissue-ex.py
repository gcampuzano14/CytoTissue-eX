import sys
import time
import json
import os
import re
import socket
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, app
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import _compat
from application import db
from application.models import Data, AppData
import forms as fs
from werkzeug import secure_filename
from PyQt4 import QtCore, QtGui, QtWebKit
import config
import tempfile
import parsetxt
import gevent.wsgi
import gevent.pywsgi
import gevent.core
from gevent import *

import appmodules.dbx_call as dbx

import sys


def __dependencies_for_freezing():
    from gevent import core, resolver_thread, resolver_ares, socket,\
        threadpool, thread, threading, select, subprocess
    import sip
    import pymysql
    import dropbox
    from flask import ext
    import flask_sqlalchemy._compat as _
    import flask_sqlalchemy
    from jinja2 import ext
    from PyQt4.QtNetwork import *
    import pprint, traceback, signal


class WebView(QtWebKit.QWebView):
    def __init__(self):
        QtWebKit.QWebView.__init__(self)

        self.load(QtCore.QUrl("http://localhost:666/"))
        self.connect(self , QtCore.SIGNAL("clicked()"), self.closeEvent)

    def closeEvent(self, event):
        self.deleteLater()
        app.quit()
        print "closing gui"
        g.kill(gevent.GreenletExit, block=False)
        f.kill(gevent.GreenletExit, block=False)


class PyQtGreenlet(gevent.Greenlet):
    def __init__(self, app):
        gevent.Greenlet.__init__(self)
        self.app = app

    def _run(self):
        while True:
            self.app.processEvents()
            while self.app.hasPendingEvents():
                self.app.processEvents()
                gevent.sleep(0.01)
        gevent.sleep(0.1)


def get_user_data():
    print 'Logging into CytoTissue-eX'
    app_name = 'cyto_tissue_comp'
    os.environ['COMPUTERNAME']
    socket.gethostbyname(socket.gethostname())
    host_name = str(socket.gethostname())
    ip_address = socket.gethostbyname(socket.gethostname())
    last_login = datetime.now()
    entries_a_month = db.session.query(AppData).filter((AppData.host_name == host_name) &
                                        (AppData.ip_address == ip_address)).all()
    if len(entries_a_month) == 0:
        permission = True
        permit = True
        login_success = True
        data_entered = AppData(app_name, ip_address, host_name, permission, last_login)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
    else:
        permit = entries_a_month[0].permission
        if permit is False:
            login_success = False
        else:
            login_success = True
    data_entered = Data(app_name, ip_address, host_name, last_login, login_success)
    try:
        db.session.add(data_entered)
        db.session.commit()
        db.session.close()
    except:
        db.session.rollback()
    return permit


if __name__ == "__main__":

    ALLOWED_EXTENSIONS = set(['txt'])
    fapp = Flask(__name__)
    fapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # fapp.config['SESSION_TYPE'] = 'filesystem'

    fapp.debug=True
    # db = SQLAlchemy(fapp)
#     def allowed_file(filename):
#         return '.' in filename and \
#                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @fapp.route('/index',  methods=['GET', 'POST'])
    @fapp.route('/',  methods=['GET', 'POST'])
    def index():
        global first_pass
        first_pass = 0
        form = fs.InputForm(request.form, csrf_enabled=False)
        form_file = fs.FileInputForm()

        for f in os.listdir(os.path.join(os.getcwd(), 'temp', 'lock')):
            os.remove(os.path.join(os.getcwd(), 'temp', 'lock',f))

        if request.method == 'GET':
            if first_pass == 0:
#               user authentication
                permit = get_user_data()
                if permit is False:
                    print 'Access to this app has been terminated. Please contact development team.\n\n\n\n\n'
                    msg = 'Access to this app has been terminated. Please contact development team if new access required.\n\n\n\n\n'
                    return render_template('access_denied.html', msg=msg)
#             form.process()
            return render_template('index.html', form=form, form_file=form_file)

        if request.method == 'POST':
            print request.files
            first_pass = 1

            form_file.validate_on_submit()
            if (form.validate_on_submit() is False) or (form_file.validate_on_submit() is False):
                flash('Input is incomplete!')
                return render_template('index.html', form=form, form_file=form_file)

            if (form.validate_on_submit() is True) and (form_file.validate_on_submit() is True):
                print 'file in'
#                 file = request.files['file']
                print 'file'

                filename = secure_filename(form_file.openfile.data.filename)
                print filename
                print os.path.join(os.getcwd(), 'temp', filename)
                form_file.openfile.data.save(os.path.join(os.getcwd(), 'temp', filename))
                print request.form
                params = dict(request.form)
                print params
                params.pop('csrf_token')
                print params['out_dir']
                out_dir = re.sub('[^\w]', '_', params['out_dir'][0], re.S)
                params['out_dir'] = os.path.join(os.getcwd(), 'job_output', out_dir)
                params['openfile'] = os.path.join(os.getcwd(), 'temp', filename)
                params['choice_site'] = params['choice_site'][0]
                print params
                session['params'] = params

                return redirect(url_for('wait'))

    @fapp.route('/wait',  methods=['GET', 'POST'])
    def wait():
        print request.method
        if request.method == 'POST':
            while len(os.listdir(os.path.join(os.getcwd(), 'temp', 'lock'))) > 0:
                pass
            return redirect(url_for('index'))
        if request.method == 'GET':
            #os.makedirs(session['params']['out_dir'])
            with tempfile.NamedTemporaryFile('w+b', dir=os.path.join(os.getcwd(), 'temp', 'lock'), delete=False) as tf:
                temp_str = 'parsing copath NLS job'
                tf.write(temp_str)
                tempname = tf.name
#             if params['choice_site'] == 'meditech':
#                 case_counts, parsed_cases_counts, excel_truncation = meditech_nls_hack.file_fuck(session['params'])
#             else:
            parsetxt.cyto_tissue_extract(session['params'])
            os.remove(tempname)
            os.remove(os.path.join(os.getcwd(), 'temp', session['params']['openfile']))

            return render_template('wait.html')


    http_server = gevent.wsgi.WSGIServer(('', 666), fapp)
    f = gevent.spawn(http_server.serve_forever)
    app = QtGui.QApplication(sys.argv)
    window = WebView()
    window.setWindowTitle('CoPath CytoTissue-eX')
    window.resize(450, 605)
    window.setFixedSize(450, 605)
    window.show()
    g = PyQtGreenlet.spawn(app)
    gevent.joinall([f, g])
