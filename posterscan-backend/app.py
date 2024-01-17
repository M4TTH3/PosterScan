from flask import Flask, request, Response, jsonify
from posterscan import PosterScan
from icalendar import create_ical
from flask_cors import CORS
import logging

app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

@app.route('/api/scanposter', methods=['POST'])
def scanposter():
    app.logger.info("Test")
    if not request.method == 'POST': return 'Not a POST', 400

    app.logger.info('Received POST request to /api/scanposter') 
    req_body: dict = request.json
    app.logger.info(req_body)

    try:
        img: bytes = req_body.get('image')
        if not img: return 'Can not find image', 400

        scanner = PosterScan()

        ret = scanner.get_poster_contents(img=img)
        print(ret)
        contents = create_ical(ret['title'], ret['date'])
        
        # Return Json of filename and contents in base64
        response = {
            'filename': ret['title'] + '.ics',
            'contents': contents.decode('utf-8')
        }
        #response.headers.add("Access-Control-Allow-Origin", "*")
        return jsonify(response), 200
    except:
        return 'Internal server error', 500

@app.route('/')
def hello():
    app.logger.info("Test")
    return "Hello World"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
