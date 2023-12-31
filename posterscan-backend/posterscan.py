from datetime import datetime
# from qrposterscan import PosterQRScanner
from openai import OpenAI

import os
from dotenv import load_dotenv
from pathlib import Path

import json

"""
The main wrapper class of qr-posterscan. PosterScan gets the data from either
PosterQRScanner OR PosterOCRScanner and post processes the text.
"""


class PosterOCRScanner:
    pass


class PosterScan:
    _poster_ocr: PosterOCRScanner
    # _poster_qr: PosterQRScanner
    _api_key: str
    _client: OpenAI

    _max_tokens: int
    _model: str

    def __init__(self) -> None:
        self._poster_ocr = PosterOCRScanner()
        # self._poster_qr = PosterQRScanner()

        if Path(".env.dev"):
            load_dotenv(Path(".env.dev").absolute())
        self._api_key = os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise LookupError("Can not find OPENAI_API_KEY")

        self._client = OpenAI(api_key=self._api_key)
        self._max_tokens = 2048
        self._model = "gpt-3.5-turbo"

    def post_process_poster(self, contents: str) -> dict | None:
        """
        This function post processes the contents into chatGPT and extracts a

        title: str
        contents: str
        date: str (in UTC time)
        """

        messages = [
            {
                "role": "system",
                "content": "You interpret contents from a posters with mispellings and provide the title, contents, and date of it in UTC ISO8601.\nFormat as JSON with keys title, contents, and date.\nNote: We are in Toronto, Canada",
            },
            {
                "role": "user",
                "content": "UW CSA PARTY!! \n New Yers! \n  Jan 1 \n 2O24. 6PM  \nFree food and beverages, make sure to RSVP!",
            },
            {
                "role": "assistant",
                "content": json.dumps({'title': 'UW CSA Party', 'contents': 'Free food and beverages, make sure to RSVP', 'date': '20240101T180000-0500'}),
            },
            {
                "role": "user",
                "content": f"Summarize the contents below to the same format now:\n{contents}",
            },
        ]

        response = self._client.chat.completions.create(
            messages=messages,
            model=self._model,
            max_tokens=self._max_tokens
        )

        ret = json.loads(response.choices[0].message.content)

        return ret


