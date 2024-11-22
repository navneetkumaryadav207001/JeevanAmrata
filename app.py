import sqlite3,os,dotenv
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_session import Session
from flask_bcrypt import Bcrypt


dotenv.load_dotenv()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'  # Directory to store session files
app.config['SESSION_PERMANENT'] = False
Session(app)
bcrypt = Bcrypt(app)
oauth = OAuth(app)

import google.generativeai as genai

app.config['SECRET_KEY'] = os.getenv('secret_key')  # Important for session management
app.config['GOOGLE_CLIENT_ID'] =  os.getenv('google_client_id')  # Replace with your Client ID
app.config['GOOGLE_CLIENT_SECRET'] =  os.getenv('google_client_secret')  # Replace with your Client Secret

gem_api = os.getenv('gem_api')
genai.configure(api_key=gem_api)



google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    redirect_uri='http://localhost:5000/login/callback',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT
            )
        ''')
        conn.commit()

init_db()


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="you are an chatbot helper for an organic farming website if relevant question is asked reply accordingly else ask to ask a relevent questions reply in hindi",
)

@app.route('/')
def index():
    return render_template('sinup_login.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/detail')
def detail():
    return render_template('detail.html')
@app.route('/feature')
def feature():
    return render_template('feature.html')
@app.route('/product')
def product():
    return render_template('product.html')
@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/team')
def team():
    return render_template('team.html')
@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')
@app.route('/blog')
def blog():
    return render_template('testinomial.html')


@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login_post', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[0], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))
@app.route('/register_post', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        return redirect(url_for('index'))

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/callback')
def google_authorized():
    token = google.authorize_access_token()
    user_info = token['userinfo']
    email = user_info['email']

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ?', (email,))
        user = cursor.fetchone()

        if user:
            session['username'] = email
            return redirect(url_for('dashboard'))

        # Register new user
        cursor.execute('INSERT INTO users (username) VALUES (?)', (email,))
        conn.commit()
        session['username'] = email
        return redirect(url_for('dashboard'))

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = model.generate_content(user_message)
    response = str(response.candidates[0].content.parts[0].text)
    print(response)
    return jsonify({'message': response})



app.run()
