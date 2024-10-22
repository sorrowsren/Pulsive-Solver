from xrequests import Session
from urllib.parse import urlencode

class imgClassification:

    @staticmethod
    def classifyImage(b64EncodedImg, variant) -> int:
        session = Session()

        jsonFormData = {
            "method": "image",
            "imginstructions": variant,
            "body": b64EncodedImg.decode("utf-8"),
            "json": "1"
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        requestId = session.request(method="POST", url="http://127.0.0.1:8080/in.php", data=urlencode(jsonFormData), headers=headers).json()["request"]
        correctIndex = session.request(method="GET", url=f"http://127.0.0.1:8080/res.php?action=get&id={requestId}&json=1").json()["request"]

        return int(correctIndex) - 1