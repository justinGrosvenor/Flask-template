from sn_app import app

@app.route('/')
def index():
	return 'test text'