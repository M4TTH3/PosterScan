# Routes

## Base URL: tbd  /api

### 1. POST **/scanposter** 
Returns the contents after scanning the image/QR and getting info about the event

POST Body (JSON):
    - image (base64)

RETURN Body (JSON):
    {
        title: str
        contents: str
        date: ISO 8601 UTC
    }