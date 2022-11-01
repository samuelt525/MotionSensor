# from crypt import methods
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from io import BytesIO
import os
import pathlib
import time

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
		body = request.json
		d['status'] = 1
		processedVideo = processVideo(body['path'], body['fileName'])
		d['filePath'] = processedVideo
	
	except Exception as e:
		print("Couldn't upload file", e)
		d['status'] = 0
	
	return jsonify(d)


def processVideo(ogPath, fileName):
	# Eventually this should return a string containing the file path to the processed video
	# For now this just returns the path to the uploaded video
	path = str(pathlib.Path(__file__).parent.resolve())
	print(path)
	return path + '\\' + fileName

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
	# app.run(debug=True)
