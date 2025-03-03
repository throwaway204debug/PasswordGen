from flask import Flask, render_template, request, jsonify
from password_generator import generate_password, is_valid_password
import os
app = Flask(__name__,
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static'),
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '../template'))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if "length" not in data or not str(data["length"]).isdigit():
        return jsonify({"error": "Please enter a valid password length!"}), 400  # Bad Request

    length = int(data["length"])

    if length < 8 or length > 100:
        return jsonify({"error": "Password length must be between 8 and 100!"}), 400

    password = generate_password(length)
    return jsonify({"password": password})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    password = data.get("password", "")
    is_valid, errors = is_valid_password(password)

    return jsonify({
        "valid": is_valid,
        "errors": errors
    })

if __name__ == '__main__':
    app.run()