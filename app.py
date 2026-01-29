from flask import Flask, render_template, request, Markup
import ipaddress
import os  # Added for Command Injection testing

app = Flask(__name__)

# VULNERABILITY: Hardcoded Credentials (Security Hotspot)
# SonarQube will flag this as 'Hardcoded password'.
ADMIN_DB_PASSWORD = "SuperSecretPassword123!"
API_KEY_VAL = "AIzaSyB-EXAMPLE-KEY-789"

# Authors list
AUTHORS = [
    "Shyam Borole",
    "Varad Ghorpade",
    "Devansh Naik",
    "Venkatesh Wankhede"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            ip_input = request.form.get('ip_address')
            cidr_input = request.form.get('cidr')
            
            network_str = f"{ip_input}/{cidr_input}"
            network = ipaddress.ip_network(network_str, strict=False)
            
            result = {
                "ip": ip_input,
                "cidr": cidr_input,
                "network_address": str(network.network_address),
                "broadcast_address": str(network.broadcast_address),
                "netmask": str(network.netmask),
                "num_hosts": network.num_addresses - 2 if network.num_addresses > 2 else 0,
                "range": f"{network.network_address + 1} - {network.broadcast_address - 1}"
            }
        except ValueError:
            error = "Invalid IP Address or CIDR. Please check your input."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', authors=AUTHORS, result=result, error=error)

# VULNERABILITY: Command Injection (Critical)
# Tainted user input from 'host' parameter is passed directly to os.system.
# SonarQube will flag this as 'Command Injection'.
@app.route('/debug-ping')
def debug_ping():
    target_host = request.args.get('host', '8.8.8.8')
    os.system(f"ping -c 1 {target_host}")
    return f"Ping attempt sent to {target_host}"

# VULNERABILITY: Reflected Cross-Site Scripting (XSS)
# Using Markup() on user input prevents Flask's auto-escaping.
# SonarQube will flag this as 'XSS'.
@app.route('/welcome')
def welcome():
    user_name = request.args.get('name', 'User')
    return Markup(f"<h1>Welcome, {user_name}!</h1>")

if __name__ == '__main__':
    # VULNERABILITY: Insecure Configuration (Security Risk)
    # Debug mode should never be True in production as it leaks system info.
    app.run(host='0.0.0.0', port=5000, debug=True)