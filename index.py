from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

if __name__ == '__main__':
    app.run()