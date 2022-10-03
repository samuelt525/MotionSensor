from flask import Flask

app = Flask(__name__)

@app.route("/test")
def members(): 
	return {"test": ["test1", "test2", "test3"]}

if __name__ == "__main__":
	app.run(debug=True)
