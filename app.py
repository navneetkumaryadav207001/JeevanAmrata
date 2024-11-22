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

import google.generativeai as genai

app.config['SECRET_KEY'] = os.getenv('secret_key')  # Important for session management
app.config['GOOGLE_CLIENT_ID'] =  os.getenv('google_client_id')  # Replace with your Client ID
app.config['GOOGLE_CLIENT_SECRET'] =  os.getenv('google_client_secret')  # Replace with your Client Secret

gem_api = os.getenv('gem_api')
genai.configure(api_key=gem_api)




def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="""you are an chatbot helper for an organic
    farming website we connect organic farmer to the buyers and we
      also promote farm tourism in india if relevant question
      is asked reply accordingly else ask to ask a relevent questions reply in hindi""",
)

@app.route('/')
def index():
    return render_template('sinup_login.html')
@app.route('/home')
def home():
    model.system_instruction=""" your name is dall-e tell them if they ask for it if a question is asked regarding a website assume its our website 
    you are an chatbot helper for an organic farming website we connect 
    organic farmer to the buyers and we also promote farm tourism in india 
    if relevant question is asked reply accordingly else ask to ask a relevent
      questions reply in hindi user is on the homepage of the website it contains 
    this is the content of the page guide the user with the help of this
    
    website contains 6 links in the header 
    Home for the home
About for the about section of the website
Service for searching for the service we are providing
Product for searching for the organic products
Blogs for blogs uploaded by tourists
Tour for searching or creating the tour
Contact for contacting the site owner

    """
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/tour')
def tour():
    return render_template('tour.html')
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




@app.route('/login_post', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[0], password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route('/register_post', methods=['POST'])
def register_post():
    username = request.form.get('username-2')
    password = request.form.get('password-2')
    name = request.form.get('name')
    type = request.form.get('type')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    

    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, name , type) VALUES (?, ?,?,?)', (username, hashed_password,name ,type))
            conn.commit()
            print("yes")
            return redirect(url_for('home'))
        
    except sqlite3.IntegrityError:
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
