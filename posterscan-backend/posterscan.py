from datetime import datetime
# from qrposterscan import PosterQRScanner
from openai import OpenAI
from easyocr import Reader

import os
from dotenv import load_dotenv
from pathlib import Path

import json
from base64 import b64decode
from PIL import Image
import cv2
import numpy as np
import io

class PosterOCRScanner:
    _scanner: Reader

    def __init__(self) -> None:
        #Disable gpu=False if using GPU
        self._scanner = Reader(lang_list=['en'], gpu=False) 
    
    def preprocess_image_1(self, img: np.ndarray) -> np.ndarray:
        """
        Converts image (base64) to Image applying preprocess techniques.
        1. Binarize
        2. Normalize
        3. Erode Noise
        """
        img = self._binarization(img)
        img = self._normalize(img)
        img = self._erodenoise(img)
        return img

    def preprocess_image_2(self, img: np.ndarray) -> np.ndarray:
        """
        Does not work for easyocr

        Preprocess image
        1. Normalize
        2. Erodenoise
        3. Laplacian
        """
        img = self._normalize(img)
        img = self._erodenoise(img)
        img = self._laplacian(img)
        return img
    
    def scantext(self, img: np.ndarray) -> str:
        text_list = self._scanner.readtext(img, detail=0)
        return " ".join(text_list)
    
    def _binarization(self, img: np.ndarray) -> np.ndarray:
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    def _thinning(self, img: np.ndarray) -> np.ndarray:
        kernel = np.ones((5,5), np.uint8)
        return cv2.erode(img, kernel, iterations = 1)
    
    def _erodenoise(self, img: np.ndarray) -> np.ndarray:
        return cv2.fastNlMeansDenoising(img, None, 20, 7, 21) 
    
    def _normalize(self, img: np.ndarray) -> np.ndarray:
        norm_img = np.zeros((img.shape[0], img.shape[1]))
        return cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    
    def _laplacian(self, img: np.ndarray) -> np.ndarray:
        return cv2.Laplacian(img, cv2.CV_64F)
        
class PosterScan:
    """
    The main wrapper class of qr-posterscan. PosterScan gets the data from either
    PosterQRScanner OR PosterOCRScanner and post processes the text.
    
    _poster_ocr: PosterOCRScanner
    # _poster_qr: PosterQRScanner
    _api_key: str
    _client: OpenAI

    _max_tokens: int
    _model: str
    """

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

    def get_poster_contents(self, img: bytes) -> dict:
        """
        Main wrapper for getting the poster contents. Returns a dictionary.
        {
            title: str
            contents: str
            date: str (in UTC time)
        }
        """

        # Try scanning the poster first for the date
        img_arr = self.convert_base64_to_arr(img)
        text = self._poster_ocr.scantext(img_arr)
        ret = self._post_process_poster(text)
        if (ret['date'] != ''): return ret

        # If no date parameter, then we try scanning the QR

        
    def convert_base64_to_arr(self, img: bytes) -> np.ndarray:
        decoded = b64decode(img)
        with Image.open(io.BytesIO(decoded)) as image:
            #Close image on ret
            return np.array(image)

    def _post_process_poster(self, contents: str) -> dict | None:
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


if __name__ == "__main__":
    scanner = PosterOCRScanner()
    for path in Path('before-image').iterdir():
        new_img = scanner.preprocess_image_1(path)
        new_path = Path('after-image') / Path(path.name)

        cv2.imwrite(str(new_path), new_img)
