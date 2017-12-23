from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth


### settings ###
SECRET_KEY = 'very secret key' # required for sessions @see http://flask.pocoo.org/docs/0.10/quickstart/#sessions
DEBUG = True # to detect code changes and reload automatically
FACEBOOK_APP_ID = '543697795982907' # comes from our registered facebook application
FACEBOOK_APP_SECRET = 'f6fe211788af944510fcfb1a104ea0e4'
HOST = 'localhost'
PORT = 5000

### creating flask object ###
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

facebook = OAuth().remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'user_posts'}
)

@app.route('/')
def home():
    """ first function that is called after accessing url """
    return render_template('welcome.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return (facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None, _external=True)))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return ("token : " + get_facebook_oauth_token()[0] +'<br>' + "id : " + me.data['id'] + '<br>' 
           + "name : " + me.data['name'] )

@facebook.tokengetter
def get_facebook_oauth_token(token = None):
    """ this function is mandatory """
    return session.get('facebook_token')



if __name__ == '__main__':
    app.run(host = HOST, port = PORT)
