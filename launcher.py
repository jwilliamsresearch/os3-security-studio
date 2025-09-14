#!/usr/bin/env python3
"""
OS³: Open Source Security Studio Launcher

Developed by James Williams (https://jwilliams.science)

Educational tool for demonstrating web application vulnerabilities
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import werkzeug
        import bleach
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def main():
    print("=" * 60)
    print("      OS³: Open Source Security Studio")
    print("=" * 60)
    print()
    print("Educational Web Application Security Demonstrator")
    print("Developed by James Williams")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("✗ app.py not found. Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("Would you like to install missing dependencies? (y/n): ", end="")
        if input().lower().startswith('y'):
            if not install_dependencies():
                return
        else:
            print("Cannot start without required dependencies.")
            return
    
    print()
    print("🎯 Learning Objectives:")
    print("  • SQL Injection vulnerabilities and prevention")
    print("  • Cross-Site Scripting (XSS) attacks and mitigation")
    print("  • Cross-Site Request Forgery (CSRF) protection")
    print("  • Authentication security best practices")
    print("  • File upload vulnerabilities")
    print("  • Access control implementation")
    print("  • Sensitive data exposure prevention")
    print("  • Security configuration hardening")
    print()
    
    print("👥 Test Accounts:")
    print("  • Admin:    admin / admin123")
    print("  • Test User: testuser / password")
    print()
    
    print("🌐 Starting application...")
    print("   URL: http://localhost:5000")
    print()
    print("⚠️  WARNING: This application contains intentional vulnerabilities")
    print("   Use only for educational purposes in controlled environments")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Start the Flask application
    try:
        from app import app, init_db
        init_db()  # Initialize database
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nShutting down OS³: Open Source Security Studio...")
        print("Thank you for using our educational security platform!")
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")

if __name__ == "__main__":
    main()
