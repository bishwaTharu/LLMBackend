from flask import Flask, request
from model import LLM
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def generate_response():
    if request.method == "POST":
        input_text = request.json["input_text"]
    elif request.method == "GET":
        input_text = request.args.get("input_text")

    llm = LLM.load_model()
    response = llm.generate_response(input_text)
    return {"response": response}

if __name__ == "__main__":
    app.run(debug=True)
