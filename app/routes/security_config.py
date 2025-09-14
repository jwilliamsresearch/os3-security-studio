from flask import Blueprint, render_template

security_config_bp = Blueprint('security_config', __name__)

@security_config_bp.route('/')
def index():
    return render_template('security_config/index.html')

@security_config_bp.route('/headers')
def headers():
    # Show current security headers
    return render_template('security_config/headers.html')
