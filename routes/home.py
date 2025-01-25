from quart import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
async def index():
    return await render_template('index.html')