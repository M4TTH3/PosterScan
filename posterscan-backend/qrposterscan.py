from qreader import QReader
from requests import request
from bs4 import BeautifulSoup

class PosterQRScanner:

    cur_link: str
    _reader: QReader

    def __init__(self) -> None:
        self.cur_link = ""
        self._reader = QReader()

    def readQR(self, img) -> bool:
        """
        Scan the QR
        Returns whether the image produced a link
        """
        link: str = self._reader.detect_and_decode(image=img)
        if "http" in link:
            self.cur_link = link
            return True
        
        return False
    
    def scrapeLink(self) -> bool:
        """
        Scrapes the websites and determines if there is a date within the website
        """
        data = request('GET', self.cur_link)
        
