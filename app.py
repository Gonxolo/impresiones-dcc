from flask import Flask, render_template, request
import paramiko
from config import Config

app = Flask("impresiones-dcc")
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh', methods=['POST'])
def ssh_connection():
    if request.method == 'POST':
        host = request.form['host']
        username = request.form['username']
        password = request.form['password']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(host, username=username, password=password)
            # Perform SSH operations here
            stdin, stdout, stderr = ssh.exec_command('ls -l')
            output = stdout.read().decode('utf-8')
            ssh.close()
            return output
        except paramiko.AuthenticationException:
            return "Authentication failed."
        except paramiko.SSHException as e:
            return f"SSH connection failed: {str(e)}"
    
    return "Invalid request"

if __name__ == '__main__':
    app.run(debug=False)