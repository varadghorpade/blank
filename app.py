from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

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
            
            # Combine into CIDR notation (e.g., 192.168.1.5/24)
            network_str = f"{ip_input}/{cidr_input}"
            
            # Calculate Subnet Details
            network = ipaddress.ip_network(network_str, strict=False)
            
            result = {
                "ip": ip_input,
                "cidr": cidr_input,
                "network_address": str(network.network_address),
                "broadcast_address": str(network.broadcast_address),
                "netmask": str(network.netmask),
                "num_hosts": network.num_addresses - 2 if network.num_addresses > 2 else 0, # Subtract Net & Broadcast
                "range": f"{network.network_address + 1} - {network.broadcast_address - 1}"
            }
        except ValueError:
            error = "Invalid IP Address or CIDR. Please check your input."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', authors=AUTHORS, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
