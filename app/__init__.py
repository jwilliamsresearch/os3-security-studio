from flask import Flask
from .models.database import init_db

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'os3-open-source-security-studio-2025'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from .routes.main import main_bp
    from .routes.sql_injection import sql_injection_bp
    from .routes.xss import xss_bp
    from .routes.csrf import csrf_bp
    from .routes.auth import auth_bp
    from .routes.file_upload import file_upload_bp
    from .routes.access_control import access_control_bp
    from .routes.data_exposure import data_exposure_bp
    from .routes.security_config import security_config_bp
    from .routes.ssrf import ssrf_bp
    from .routes.crypto import crypto_bp
    from .routes.vulnerable_components import vulnerable_components_bp
    from .routes.logging_monitoring import logging_monitoring_bp
    # Network Security Modules
    from .routes.network_protocols import network_protocols_bp
    from .routes.port_scanner import port_scanner_bp
    from .routes.dns_security import dns_security_bp
    from .routes.traffic_analysis import traffic_analysis_bp
    from .routes.firewall_sim import firewall_sim_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(sql_injection_bp, url_prefix='/sql-injection')
    app.register_blueprint(xss_bp, url_prefix='/xss')
    app.register_blueprint(csrf_bp, url_prefix='/csrf')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(file_upload_bp, url_prefix='/file-upload')
    app.register_blueprint(access_control_bp, url_prefix='/access-control')
    app.register_blueprint(data_exposure_bp, url_prefix='/data-exposure')
    app.register_blueprint(security_config_bp, url_prefix='/security-config')
    app.register_blueprint(ssrf_bp, url_prefix='/ssrf')
    app.register_blueprint(crypto_bp, url_prefix='/crypto')
    app.register_blueprint(vulnerable_components_bp, url_prefix='/vulnerable_components')
    app.register_blueprint(logging_monitoring_bp, url_prefix='/logging_monitoring')
    # Network Security Modules
    app.register_blueprint(network_protocols_bp, url_prefix='/protocol-security')
    app.register_blueprint(port_scanner_bp, url_prefix='/port-scanning')
    app.register_blueprint(dns_security_bp, url_prefix='/dns-security')
    app.register_blueprint(traffic_analysis_bp, url_prefix='/traffic-analysis')
    app.register_blueprint(firewall_sim_bp, url_prefix='/firewall')
    
    # Add security headers middleware
    from .utils.security_headers import add_security_headers
    app.after_request(add_security_headers)
    
    return app
