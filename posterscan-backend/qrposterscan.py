from qreader import QReader
import requests as req
from bs4 import BeautifulSoup as Soup
from numpy import ndarray


class PosterQRScanner:
    cur_link: str
    _reader: QReader

    def __init__(self) -> None:
        self.cur_link = ""
        self._reader = QReader()

    def scan_qr(self, img: "ndarray") -> str:
        """
        Scans the QR and returns the text from the website.
        If no QR or no Text, then it returns ""
        """
        if self.read_qr(img):
            return self.web_info(self.cur_link)

        return ""

    def read_qr(self, img) -> bool:
        """
        Scan the QR
        Returns whether the image produced a link
        """
        # return_detections returns the detection details
        # https://pypi.org/project/qreader/#QReader_detect_table
        link: str = self._reader.detect_and_decode(image=img)
        decoded_strings = self._reader.detect_and_decode(image=img)

        # Iterate over each decoded string
        for decoded_str in decoded_strings:
            if decoded_str is not None and "http" in decoded_str:
                self.cur_link = decoded_str
                return True

        return False

    def web_info(self, url) -> str:
        if url:
            page = req.get(url)
            html_bytes = page.content

            soup = Soup(html_bytes, "html.parser")

            all_text = soup.get_text(" ", strip=True)

            return all_text

        return ""


# if __name__ == "__main__":
#     scanner = PosterQRScanner()
#     test_images = ["./after-image/youtubee.png", "./after-image/Untitled (30).png"]
#     for img_path in test_images:
#         imgg = cv2.imread(img_path, 0)
#         if imgg is None:
#             print(f"Failed to load image from {img_path}")
#         else:
#             img = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)
#         if scanner.readQR(img):
#             print(f"Found URL: {scanner.cur_link}")
#             print(scanner.webInfo(scanner.cur_link))
#         else:
#             print("No URL found in this image")
