import os
from dotenv import load_dotenv
from quart import Quart
from routes.home import home_bp
from routes.track import track_bp
from routes.api import api_bp

load_dotenv()

app = Quart(__name__, template_folder='templates')

app.register_blueprint(home_bp)
app.register_blueprint(track_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)