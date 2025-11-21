from flask import Flask
app = Flask(__name__)

# Accept both /api and /api/
@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
def home():
    return {"message": "Hello from API"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
