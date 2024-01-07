from flask import Flask, request, Response, jsonify
from posterscan import PosterScan

app = Flask(__name__)

@app.route('/api/scanposter', methods=['POST'])
def scanposter():
    if not request.method == 'POST': return 'Not a POST', 400

    app.logger.info('Received POST request to /api/scanposter') #
    req_body: dict = request.json
    
    try:
        img: bytes = req_body.get('image')
        if not img: return 'Can not find image', 400

        scanner = PosterScan()

        ret = scanner.get_poster_contents(img=img)
        if not (ret.get('title') or ret.get('contents') or ret.get('date')): 
            return 'Unable to retrieve any data', 400
        
        return jsonify(ret), 200
    except:
        return 'Internal server error', 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)