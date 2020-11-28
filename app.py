import flask

from flask import request, render_template, redirect
from flask_mysqldb import MySQL
import yaml
from helpers import database

app = flask.Flask(__name__)

db = yaml.load(open('db.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)


class FrontendData:
    def __init__(self):
        self.previous_cleaner = None
        self.current_cleaner = None
        self.next_cleaner = None
        self.cleaning_done = None
        self.user_cleans = None


@app.route('/')
def index():
    cursor = mysql.connection.cursor()

    users_names = database.get_users_names(cursor)
    current_user_id = database.get_current_user_id(cursor)
    cleaning_status = database.get_cleaning_status(cursor)
    cleaning_status_names = database.resolve_cleaning_status_names(cleaning_status,
                                                                   users_names)

    frontend_data = FrontendData()
    frontend_data.previous_cleaner = cleaning_status_names.previous_cleaner
    frontend_data.current_cleaner = cleaning_status_names.current_cleaner
    frontend_data.next_cleaner = cleaning_status_names.next_cleaner
    frontend_data.cleaning_done = cleaning_status.cleaning_done
    frontend_data.user_cleans = current_user_id == cleaning_status.current_cleaner_id

    return render_template('index.html', data=frontend_data)


@app.route('/done', methods=['GET', 'POST'])
def done():
    if request.method == 'POST':
        print("Clicked!")
        return redirect('/')

    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
