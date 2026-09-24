from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome to DevOps Week 02</h1>
    <p>Feature 1: Application setup completed</p>
    <p>Feature 2: New application changes</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
