#!/usr/bin/env python3
"""
OS³: Open Source Security Studio - Main Application Entry Point

Developed by James Williams (https://jwilliams.science)

A comprehensive Flask-based cybersecurity education platform
"""

from app import create_app
import os

def main():
    """Main application entry point"""
    # Ensure upload directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Create Flask app using factory pattern
    app = create_app()
    
    # Run the application
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
