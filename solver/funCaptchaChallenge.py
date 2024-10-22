from solver.funCaptcha import funCaptcha
from solver.imgClassification import imgClassification
from typing import Optional
from threading import Lock
from random import uniform
from time import sleep

lock = Lock()

class funCaptchaChallenge:

    def __init__(self, challengeInfo: dict, browserInfo: dict, proxy: Optional[str] = None) -> None:
        self.interactor = funCaptcha(challengeInfo, browserInfo, proxy)

    def solve(self) -> str:
        self.interactor.getCfCookie()
        self.interactor.getToken()

        if self.interactor.token == None:
            with lock:
                print("Rejected BDA/blob")
            
            raise ValueError("Rejected BDA/blob, make sure you've sent the correct json data.")

        if "sup=1" in self.interactor.token:
            with lock:
                print("silent_pass", 0)
            
            return {"success": True, "solution": self.interactor.token}
        
        self.interactor.getChallenge()

        with lock:
            print(self.interactor.variant, self.interactor.waves)

        oldHeaders = self.interactor.session.headers.copy()

        for _ in range(self.interactor.waves):
            img = self.interactor.getBase64Image()
            self.interactor.session.headers = oldHeaders

            correctIndex = imgClassification.classifyImage(img, self.interactor.variant)
            
            self.interactor.setBiometrics()

            sleep(uniform(1, 2))

            answerResponse = self.interactor.submitIndexAnswer(correctIndex) if self.interactor.gameType == 4 else self.interactor.submitTileAnswer(correctIndex)
            solved = answerResponse["solved"]
            
            if solved == True:
                return {"success": True, "solution": self.interactor.token}
            elif solved == False:
                return {"success": False, "solution": "Failed to solve the captcha."}