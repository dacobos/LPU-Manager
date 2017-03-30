import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lpu.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices', methods=['GET'])
def devices():
    db = get_db()
    cur = db.execute('select * from devices')
    entries = cur.fetchall()
    return render_template('devices.html', entries = entries)

@app.route('/createDevice', methods=['POST'])
def createDevice ():
    db = get_db()
    db.execute('insert into devices (device, ipAddress) values (?,?)',[request.form['device'],request.form['ipAddress']])
    db.commit()
    flash('Device successfully created')
    return redirect(url_for('devices'))

@app.route('/updateDevice', methods=['POST'])
def updateDevice():
    db = get_db()
    db.execute('update devices set device = (?), ipAddress = (?) where device = (?)',[request.form['newdevice'],request.form['newipAddress'],request.form['oldDevice']])
    db.commit()
    flash('Device successfully updated')
    return redirect(url_for('devices'))

@app.route('/deleteDevice', methods=['POST'])
def deleteDevice():
    db = get_db()
    db.execute('delete from devices where device = (?)',[request.form['deleteDevice']])
    db.commit()
    flash('Device successfully deleted')
    return redirect(url_for('devices'))


@app.route('/category', methods=['GET'])
def category():
    db = get_db()
    cur = db.execute('select * from category')
    entries = cur.fetchall()
    return render_template('category.html', entries = entries)

@app.route('/createCategory', methods=['POST'])
def createCategory ():
    db = get_db()
    db.execute('insert into category (category, capexCat) values (?,?)',[request.form['category'],request.form['capexCat']])
    db.commit()
    flash('Category successfully created')
    return redirect(url_for('category'))

@app.route('/updateCategory', methods=['POST'])
def updateCategory():
    db = get_db()
    db.execute('update category set category = (?), capexCat = (?) where category = (?)',[request.form['newCategory'],request.form['newcapexCat'],request.form['oldCategory']])
    db.commit()
    flash('Category successfully updated')
    return redirect(url_for('category'))

@app.route('/deleteCategory', methods=['POST'])
def deleteCategory():
    db = get_db()
    db.execute('delete from category where category = (?)',[request.form['deleteCategory']],)
    db.commit()
    flash('Category successfully deleted')
    return redirect(url_for('category'))


@app.route('/interfaces', methods=['GET'])
def interfaces():
    db = get_db()
    devs = db.execute('select * from devices').fetchall()
    entries = db.execute('select * from interfaces').fetchall()
    return render_template('interfaces.html', entries = entries, devs=devs)

@app.route('/addDevice', methods=['POST'])
def addDevice ():
    db = get_db()
    ipAdd = db.execute('select ipAddress from devices where device = (?)',[request.form['device']]).fetchall()[0][0]
    # val = collect_from_devices(ipAdd)
    # val = [('1 GE TR', 4),('10 GE TR', 4),('1 GE SE',2),('10 GE SE',8)]
    # db.execute('insert into interfaces (device, category, foc, current, lpu, capexLPU) values (?,?,?,?,?,?)',[request.form['device'],request.form['capexCat']])
    # db.commit()
    # flash('Category successfully created')
    return redirect(url_for('interfaces'))
