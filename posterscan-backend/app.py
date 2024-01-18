from flask import Flask, request, make_response, jsonify, Response
from posterscan import PosterScan
from icalendar import Calendar, Event
from flask_cors import CORS
import logging
from datetime import datetime as dt, timedelta
import pytz

app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)


"""
This gets the data for the ical

Output Body:

{
        title: str
        contents: str
        date: ISO 8601 UTC
}

"""
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
        
        return jsonify(ret), 200
    except:
        return 'Internal server error', 500

# def scanposter():
#     app.logger.info("Test")
#     if not request.method == 'POST': return 'Not a POST', 400

#     app.logger.info('Received POST request to /api/scanposter') 
#     req_body: dict = request.json
#     app.logger.info(req_body)

#     try:
#         img: bytes = req_body.get('image')
#         if not img: return 'Can not find image', 400

#         scanner = PosterScan()

#         ret = scanner.get_poster_contents(img=img)
#         print(ret)
#         contents = create_ical(ret['title'], ret['date'])
        
#         # Return Json of filename and contents in base64
#         response = {
#             'filename': ret['title'] + '.ics',
#             'contents': contents.decode('utf-8')
#         }
#         #response.headers.add("Access-Control-Allow-Origin", "*")
#         return jsonify(response), 200
#     except:
#         return 'Internal server error', 500


# with open('test.ics', 'w') as my_file:
#     my_file.writelines(c.serialize_iter())

# with open('test.ics', 'rb') as file:
#     encoded_string = base64.b64encode(file.read())
# return encoded_string

"""
This converts the dictionary into ical
Format:
{
    title: str
    contents: str
    date: ISO 8601 UTC
}

"""
@app.route('/api/getical', methods=['POST'])
def get_ical() -> Response:
    app.logger.info('Convert to ical running')

    try:
        req_body: dict = request.json
        expected_keys = ('title', 'contents', 'date')

        if not set(req_body.keys()).issubset(expected_keys):
            return jsonify({'bad request params'}), 400
        
        title = req_body['title']
        date = dt.strptime(req_body['date'], "%Y%m%dT%H%M%S%z")
        cal = Calendar()

        cal.add('prodid', f'-//{title} Calendar//mxm.dk//')
        cal.add('version', '2.0')

        event = Event()
        event.add('summary', title)
        event.add('dtstart', date.astimezone(tz=pytz.utc))
        event.add('dtend', date.astimezone(tz=pytz.utc) + timedelta(hours=1))
        event.add("dtstamp", dt.utcnow())

        cal.add_component(event)

        res = make_response(cal.to_ical()) 
        res.headers["Content-Disposition"] = "attachment; filename=calendar.ics"

        return res
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/')
def hello():
    app.logger.info("Test")
    return "Hello World"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
