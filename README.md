# OS³: Open Source Security Studio

<div align="center">

<!-- Logo placeholder - replace with actual logo when ready -->
<img src="https://jwilliams.science/os3-security-studio/assets/images/os3-logo.png" alt="OS³ Logo" width="200" height="200" />

**Comprehensive Educational Cyber Security Platform**

*Empowering the next generation of cyber security professionals through hands-on, practical education*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Platform](https://img.shields.io/badge/platform-educational-orange.svg)](#)
[![Security](https://img.shields.io/badge/security-learning-red.svg)](#)

[**Quick Start**](#quick-start) • [**Documentation**](./documentation/) • [**Features**](#features) • [**Modules**](#security-modules) • [**Contributing**](#contributing)

---

</div>

## Overview

**OS³ (Open Source Security Studio)** is a comprehensive Flask-based cybersecurity education platform designed for universities, training institutions, and self-directed learners. Built by **James Williams** at **Birmingham Newman University**, OS³ provides hands-on experience with real-world security vulnerabilities in a controlled environment.

### Why OS³?

- **Educational Focus**: Designed specifically for learning with guided tutorials and real-world scenarios
- **Open Source**: Fully open with MIT licence for code and CC BY 4.0 for content - customise, extend, and contribute
- **Modular Design**: Extensible architecture for easy addition of new security modules
- **Interactive Labs**: Hands-on exercises with real-time feedback and step-by-step guidance

---

## Features

<table>
<tr>
<td width="50%">

### **Security Training**
- **13+ Interactive Modules** covering OWASP Top 10
- **Vulnerability Demonstrations** with secure implementations
- **Network Security Labs** including port scanning and traffic analysis
- **Cryptography Workshops** with practical encryption exercises

</td>
<td width="50%">

### **Educational Excellence**
- **Comprehensive Curriculum** with progressive difficulty levels
- **Real-World Scenarios** based on industry best practices
- **Modular Structure** allowing flexible course design

</td>
</tr>
</table>

---

## Security Modules

<div align="center">

| Module | Focus Area | Difficulty | Key Learning Outcomes |
|--------|------------|------------|----------------------|
| **Network Security** | Port scanning, traffic analysis, IDS | Beginner-Advanced | Network reconnaissance, monitoring |
| **Vulnerability Assessment** | SQL injection, XSS, CSRF | Intermediate | Web application security testing |
| **Cryptography** | Encryption, hashing, PKI | Advanced | Cryptographic implementations |
| **Access Control** | Authentication, authorisation | Intermediate | Identity and access management |
| **File Upload Security** | Malicious files, path traversal | Beginner | Secure file handling practices |
| **Security Monitoring** | Logging, SIEM, incident response | Advanced | Security operations and forensics |

</div>

### **Learning Outcomes**
Students will master practical skills in:
- Ethical hacking and penetration testing techniques
- Vulnerability identification and remediation
- Security monitoring and incident response
- Cryptographic implementations and protocols
- Network security analysis and defence
- Secure coding practices and code review

---

## Quick Start

### Prerequisites
- **Python 3.8+** 
- **4GB RAM** minimum
- **2GB Storage** available
- **Modern web browser**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/jwilliamsresearch/os3-security-studio.git
cd os3-security-studio

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the platform
python app.py

# 5. Access the lab
# Open browser to: http://localhost:5000
```

### **Default Credentials**
- **Admin**: `admin` / `admin123`
- **Student**: `testuser` / `password`
- **Demo**: `john` / `weak`

---

---

## Educational Integration

### **For Educators**
- **Flexible Curriculum**: Modular design allows custom course structures
- **Assessment Integration**: Built-in practical testing scenarios
- **Demonstration Tools**: Side-by-side vulnerable vs. secure code
- **Progress Tracking**: Student analytics and performance metrics

### **For Students**
- **Hands-On Learning**: Direct vulnerability exploitation and remediation
- **Progressive Curriculum**: Beginner to advanced skill development
- **Industry Preparation**: Real-world security practices and tools

---

## Getting Involved

### **Contributing**

We welcome contributions from the cybersecurity and education communities!

- **Bug Reports**: [Open an issue](https://github.com/jwilliamsresearch/os3-security-studio/issues/new?template=bug_report.md)
- **Feature Requests**: [Suggest enhancements](https://github.com/jwilliamsresearch/os3-security-studio/issues/new?template=feature_request.md)
- **Documentation**: Help improve learning materials
- **Security Modules**: Contribute new vulnerability demonstrations
- **Translations**: Make OS³ accessible globally

### **Development Guidelines**
1. Follow the established modular architecture
2. Include both vulnerable and secure implementations
3. Provide comprehensive educational documentation
4. Ensure code quality and educational value
5. Add corresponding teaching materials

---

## Important Disclaimers

<div align="center">

### **EDUCATIONAL USE ONLY**

**This platform contains intentional security vulnerabilities for educational purposes.**

</div>

- **Safe for**: Controlled educational environments, security training, academic research
- **Never use in**: Production environments, live networks, or without proper authorisation
- **Always ensure**: Compliance with local laws and institutional policies
- **Remember**: Practice responsible disclosure and ethical security practices

### **Production Deployment Warning**
Never deploy this application in production without:
- Removing all intentional vulnerabilities
- Implementing comprehensive input validation
- Adding proper authentication and authorisation
- Enabling security monitoring and logging
- Following industry security best practices

---

## Licence & Attribution

<div align="center">

**Code & Software**: [MIT License](https://opensource.org/licenses/MIT)  
**Educational Content**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

**Created by [James Williams](https://jwilliams.science)**
*2025*

---

### **Connect & Support**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/jwilliamsresearch/os3-security-studio)
[![Website](https://img.shields.io/badge/Website-OS³_Platform-blue?logo=firefox)](https://jwilliamsresearch.github.io/os3-security-studio/)
[![Discussions](https://img.shields.io/badge/Community-Discussions-purple?logo=github)](https://github.com/jwilliamsresearch/os3-security-studio/discussions)
[![Issues](https://img.shields.io/badge/Support-Issues-red?logo=github)](https://github.com/jwilliamsresearch/os3-security-studio/issues)

**Star this repository if OS³ helps your cyber security journey!**

</div>
