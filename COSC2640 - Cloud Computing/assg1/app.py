from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import logging
import boto3
from user import *
from music import *
import os
import flask

logging.basicConfig(filename='record.log', level=logging.DEBUG,
					format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb')

s3_bucket_name = 's3939713-artist-image'
s3_expiration = 300

@app.route('/', methods=['GET'])
def index():
	if 'msg' in request.args:
		msg = request.args['msg']
		return render_template('home.html', msg=msg)
	else:
		return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		logging.info(f'email: {email}')
		if login_check(email, password, dynamodb):
			# login success
			session['email'] = email
			return redirect(url_for('main'))
		else:
			# login fail
			return render_template('home.html', msg='email or password is invalid')


@app.route('/register', methods=['GET','POST'])
def register():
	if flask.request.method == 'POST':
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		if register_check(email, dynamodb):
			# can be register
			register_acc(email, username, password, dynamodb)
			return redirect('/')
		else:
			# duplicate email
			return render_template('register.html', msg='The email already exists')
	else:
		return render_template('register.html')


@app.route('/main', methods=['GET','POST'])
def main():
	if 'email' in session:
		email = session['email']
		user_obj = load_user_detail(email, dynamodb)
		if 'form_action' in request.form:
			if request.form['form_action'] == 'query':


				title = request.form['title']
				title = None if not title.strip() else title.strip()

				year = request.form['year']
				year = None if not year.strip() else year.strip()

				artist = request.form['artist']
				artist = None if not artist.strip() else artist.strip()

				email = request.form['email']
				user_obj = load_user_detail(email, dynamodb)

				music_list = music_query(title, year, artist, dynamodb)
				if music_list:
					for music in music_list:
						music['s3_url'] = get_image_from_s3_by_img_url(music['img_url'])

					return render_template('main.html', user=user_obj, query_music_list=music_list)
				else:
					return render_template('main.html', user=user_obj,
										   query_msg='No result is retrieved. Please query again')

			elif request.form['form_action'] == 'subscribe':
				email = request.form['email']
				title = request.form['music_title']

				music_subscribe(title, email, dynamodb)
				user_obj = load_user_detail(email, dynamodb)

				return render_template('main.html', user=user_obj)

			elif request.form['form_action'] == 'remove_sub':
				email = request.form['email']
				title = request.form['music_title']

				music_remove_subscribe(title, email, dynamodb)
				user_obj = load_user_detail(email, dynamodb)
				return render_template('main.html', user=user_obj)

			elif request.form['form_action'] == 'logout':
				session.pop('email')
				return redirect(url_for('index', msg='You have been logout.'))
		else:
			return render_template('main.html', user=user_obj)
	else:
		return redirect(url_for('index', msg='You have been logout.'))


if __name__ == "__main__":
	app.run(host='0.0.0.0')
