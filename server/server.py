from flask import Flask
import os

app = Flask(__name__)

@app.route("/test")
def members(): 
	return {"test": ["test1", "test2", "test3"]}

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	# app.run(debug=True)
