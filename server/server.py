from crypt import methods
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
import os

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})

UPLOAD_FOLDER= os.path.expanduser("~/Desktop/MotionSensor")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/test")
def members(): 
	return {"test": ["test1", "test2", "test3"]}

@app.route("/backend", methods=['POST'])
def testingFile():
	d = {}
	try:
		file = request.files['file']
		filename = file.filename
		print(f"Uploading file {filename}")
		print(file)
		file_bytes = file.read()
		file_content = BytesIO(file_bytes).readlines()
		d['status'] = 1
	
	except Exception as e:
		print("Couldn't upload file", e)
		d['status'] = 0
	return jsonify(d)


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	# app.run(debug=True)
