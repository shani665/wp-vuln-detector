# Brout Force Attack and User Enumeration
WordPress Chained Attack Detection – Astra Security Assignment

This project detects chained vulnerabilities on a WordPress site:
- **User Enumeration**
- **Login Brute-force Attack**

## 📌 Target
- Tested on a local WordPress instance at: `http://localhost/wordpress/wp-login.php`
- Compatible with other WordPress sites.

---

## 🔧 Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/wp-vuln-detector.git
cd wp-vuln-detector
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Create Input Files

Create user.txt:
```
admin
test
guest
password
```
Create pass.txt:
```
admin
123456
root
password
```
4. Run the Detector
```
pip install import
python3your_script.py

