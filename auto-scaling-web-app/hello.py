from flask import Flask

app = Flask(__name__)

# Updated route for the root URL
@app.route('/')
def root():
    return 'Hello, World! This is my Flask web application.'

# Updated route for the '/app' URL
@app.route('/app')
def hello_world():
    return 'Hello, World! This is my /app route.'

# Run the application if this script is executed
if __name__ == '__main__':
    # Run the app on 0.0.0.0 (all available network interfaces) and port 2000
    app.run(host='0.0.0.0', port=2000)
