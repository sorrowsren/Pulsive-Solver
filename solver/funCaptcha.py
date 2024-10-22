from curl_cffi import requests
from time import time
from random import random, randint
from json import dumps
from base64 import b64encode
from urllib.parse import unquote
from solver.cryptoJs import cryptojsEncrypt
from solver.bda import bda
from solver.dapib import dapib
from typing import Optional
from solver.ipIntelligence import ipIntelligence
from solver.biometrics import Biometrics

class funCaptcha:

    def __init__(self, challengeInfo: dict, browserInfo: dict, proxy: Optional[str] = None) -> None:
        self.session = requests.Session(impersonate="chrome")
        self.session.verify = False
        
        if proxy:
            self.session.proxies = {
                "https": proxy,
                "http": proxy
            }

        self.ipInfo = ipIntelligence(self.session).getIpInfo()
        self.challengeInfo = challengeInfo
        self.browserInfo = browserInfo

        self.userAgent = self.browserInfo["User-Agent"]
        self.secChUa = self.browserInfo["Sec-Ch-Ua"]
        self.secPlatform = '"Windows"' if 'Windows NT' in self.userAgent else '"macOS"'

        self.language = self.ipInfo["language"]
        self.acceptLanguage = self.ipInfo["acceptLanguage"]

        self.sc = "{\"sc\":[" + str(randint(100, 200)) + "," + str(randint(100, 200)) + "]}"

        self.answerHistory = []
        self.tguessHistory = []
        
        self.imageCounter = 0
        self.tguessCalled = 0

    def sortHeaders(self, inputHeaders) -> dict:
        desiredOrder = [
            "Host",
            "Connection",
            "Pragma",
            "Cache-Control",
            "sec-ch-ua",
            "Content-Type",
            "x-ark-esync-value",
            "sec-ch-ua-mobile",
            "User-Agent",
            "sec-ch-ua-platform",
            "Accept",
            "Origin",
            "Sec-Fetch-Site",
            "Sec-Fetch-Mode",
            "Sec-Fetch-Dest",
            "Referer",
            "Accept-Language",
            "Cookie",
            "Accept-Encoding",
            "Content-Length"
        ]

        sortedHeaders = dict(sorted(inputHeaders.items(), key=lambda pair: desiredOrder.index(pair[0]) if pair[0] in desiredOrder else len(desiredOrder)))

        return sortedHeaders

    def encode_data(self, data) -> str:
        encoded_data = []
        for c in data:
            if ord(c) > 127 or c in " %$&+,/:;=?@<>#%{}":
                encoded_data.append(f'%{ord(c):02X}')
            else:
                encoded_data.append(c)
        
        return ''.join(encoded_data)

    def urlencode(self, data) -> str:
        dataa = ''

        for index, pair in enumerate(data.items()):
            dataa += f'{pair[0]}={self.encode_data(pair[1])}&' if index != len(data.keys()) - 1 else f'{pair[0]}={self.encode_data(pair[1])}'

        return dataa

    def getNewrelicTimestamp(self) -> str:
        unixTimeMs = int(time() * 1000)
        unixTimeMsStr = str(unixTimeMs)
        return f"{unixTimeMsStr[:7]}00{unixTimeMsStr[7:13]}"
    
    def setBiometrics(self) -> None:
        self.biometrics = 'eyJtYmlvIjoiMTEzMDgsMCwxODYsMTcwOzExMzQzLDEsMTg2LDE3MDsxMTM0MywyLDE4NiwxNzA7MTE0NzIsMSwxODYsMTcwOzExNDcyLDIsMTg2LDE3MDsxMTYyNywwLDE3NSwxNjk7MTE2MjcsMSwxNzUsMTY5OzExNjI4LDIsMTc1LDE2OTsxMTc0MSwxLDE3NSwxNjk7MTE3NDEsMiwxNzUsMTY5OzEyNDQ1LDAsMTc0LDE1MzsxMjQ0NSwxLDE3NCwxNTM7MTI0NDYsMiwxNzQsMTUzOzEyODA4LDAsMjIxLDIwMzsxMjgwOCwxLDIyMSwyMDM7MTI4MDgsMiwyMjEsMjAzOyIsInRiaW8iOiIxMTIxNiwwLDE4NiwxNzA7MTEzNjIsMCwxNzgsMTY2OzExNTI4LDAsMTc1LDE2OTsxMTY2NiwwLDE3NywxNzA7MTIzNTMsMCwxNzQsMTUyOzEyNzI0LDAsMjIxLDIwMzsiLCJrYmlvIjoiIn0='

    def getCfCookie(self) -> None:
        self.session.headers = self.sortHeaders({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Connection': 'keep-alive',
            'Referer': self.challengeInfo["site"],
            
            
            
            
            
            
            'User-Agent': self.userAgent
        })

        response = self.session.get(f"{self.challengeInfo["surl"]}/v2/{self.challengeInfo["publicKey"]}/api.js")

        self.cfuvid = f'_cfuvid={response.cookies.get("_cfuvid").split(";")[0]}'
    
    def parseToken(self, token):
        return dict((unquote(key), unquote(value)) for key, value in (pair.split("=") for pair in token.split("|")))

    def getToken(self) -> None:
        currentTime = int(time())
        roundedTime = str((currentTime - (currentTime % 21600)))

        randomNumber = str(random())

        encryptedBda = bda(self.ipInfo, self.challengeInfo, self.browserInfo).getBda()

        if self.challengeInfo["site"].endswith("/"):
            siteValue = self.challengeInfo["site"][:-1]
        else:
            siteValue = self.challengeInfo["site"]

        payload = {
            "bda": b64encode(encryptedBda.encode("utf-8")).decode("utf-8"),
            "public_key": self.challengeInfo["publicKey"],
            "site": siteValue,
            "userbrowser": self.userAgent,
            "capi_version": "2.11.0",
            "capi_mode": self.challengeInfo["capiMode"],
            "style_theme": self.challengeInfo["styleTheme"],
            "rnd": randomNumber,
        }

        if self.challengeInfo["languageEnabled"]:
            payload["language"] = self.language.lower()

        if "extraData" in list(self.challengeInfo.keys()):
            for key, value in self.challengeInfo["extraData"].items():
                payload[f"data[{key}]"] = value

        self.session.headers = self.sortHeaders({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.challengeInfo["surl"],
            'Referer': f"{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html",
            
            
            
            
            
            
            'User-Agent': self.userAgent,
            "x-ark-esync-value": roundedTime,
        })

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.getNewrelicTimestamp()}'

        response = self.session.post(f"{self.challengeInfo["surl"]}/fc/gt2/public_key/{self.challengeInfo["publicKey"]}", data=self.urlencode(payload))

        try:
            self.token = response.json()["token"]
        except:
            self.token = None
    
    def sendAnalytics(self, analytics, addRequestId) -> None:
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Origin': self.challengeInfo["surl"],
            'Referer': self.embedUrl,
            
            
            
            
            
            
            "User-Agent": self.userAgent,
            "X-NewRelic-Timestamp": self.getNewrelicTimestamp(),
            "X-Requested-With": "XMLHttpRequest",
        }

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.session.headers["X-NewRelic-Timestamp"]}'

        if addRequestId:
            self.session.headers["X-Requested-ID"] = cryptojsEncrypt(self.sc, f"REQUESTED{self.sessionToken}ID", False)

        self.session.headers = self.sortHeaders(self.session.headers)

        self.session.post(f"{self.challengeInfo["surl"]}/fc/a/", data=self.urlencode(analytics))
    
    def getChallenge(self) -> None:
        self.analyticsTier = self.token.split("at=")[1].split("|")[0]
        self.sid = self.token.split("|")[1].split("r=")[1].split("|")[0]
        self.tokenInfo = self.parseToken(f"session={self.token}")
        self.embedUrl = f"{self.challengeInfo["surl"]}/fc/assets/ec-game-core/game-core/1.23.2/standard/index.html?{self.urlencode(self.tokenInfo)}&theme={self.encode_data(self.challengeInfo["styleTheme"])}"

        self.session.headers = self.sortHeaders({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Connection': 'keep-alive',
            'Referer': f"{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html",
            
            
            
            
            
            
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.userAgent
        })

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.getNewrelicTimestamp()}'

        self.session.get(self.embedUrl)

        self.session.headers = self.sortHeaders({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Connection': 'keep-alive',
            'Referer': f"{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html",
            
            
            
            
            
            
            'User-Agent': self.userAgent
        })

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.getNewrelicTimestamp()}'
        
        self.session.get(f"{self.challengeInfo["surl"]}/fc/gc/?token={self.token.split('|')[0]}")

        self.tokenInfo = self.parseToken(f"token={self.token}")

        self.session.headers = {
            "Accept": "*/*",
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Accept-Language": self.acceptLanguage,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.challengeInfo["surl"],
            "Referer": f"{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html",
            
            
            
            
            
            
            "User-Agent": self.userAgent,
            "X-NewRelic-Timestamp": self.getNewrelicTimestamp(),
            "X-Requested-With": "XMLHttpRequest"
        }

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.session.headers["X-NewRelic-Timestamp"]}'

        self.session.headers = self.sortHeaders(self.session.headers)

        challengeData = self.urlencode({
            "token": self.tokenInfo["token"],
            "sid": self.sid,
            "render_type": "canvas",
            "lang": self.language.lower() if self.challengeInfo["languageEnabled"] else "",
            "isAudioGame": "false",
            "is_compatibility_mode": "false",
            "apiBreakerVersion": "green",
            "analytics_tier": str(self.analyticsTier)
        })
        
        response = self.session.post(f"{self.challengeInfo["surl"]}/fc/gfct/", data=challengeData).json()

        self.gameData = response["game_data"]
        self.gameType = self.gameData["gameType"]
        self.sessionToken = response["session_token"]
        self.challengeId = response["challengeID"]
        self.challengeUrl = response["challengeURL"]
        self.dapibUrl = response.get("dapib_url", None)
        if self.gameType == 4:
            self.variant = self.gameData.get("variant", response["game_data"]["instruction_string"])
        elif self.gameType == 3:
            self.variant = self.gameData["game_variant"]
        self.waves = self.gameData["waves"]
        self.challengeImgs = self.gameData["customGUI"]["_challenge_imgs"]

        oldHeaders = self.session.headers.copy()

        self.sendAnalytics({
            'sid': self.sid,
            'session_token': self.sessionToken,
            'analytics_tier': str(self.analyticsTier),
            'disableCookies': 'false',
            'render_type': 'canvas',
            'is_compatibility_mode': 'false',
            'category': 'Site URL',
            'action': f'{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html',
        }, False)

        self.sendAnalytics({
            'sid': self.sid,
            'session_token': self.sessionToken,
            'analytics_tier': str(self.analyticsTier),
            'disableCookies': 'false',
            'game_token': self.challengeId,
            'game_type': str(self.gameType),
            'render_type': 'canvas',
            'is_compatibility_mode': 'false',
            'category': 'loaded',
            'action': 'game loaded',
        }, False)

        self.sendAnalytics({
            'sid': self.sid,
            'session_token': self.sessionToken,
            'analytics_tier': str(self.analyticsTier),
            'disableCookies': 'false',
            'game_token': self.challengeId,
            'game_type': str(self.gameType),
            'render_type': 'canvas',
            'is_compatibility_mode': 'false',
            'category': 'begin app',
            'action': 'user clicked verify',
        }, True)

        self.session.headers = oldHeaders
    
    def getBase64Image(self) -> bytes:
        self.session.headers = self.sortHeaders({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': self.acceptLanguage,
            'Connection': 'keep-alive',
            'Referer': self.embedUrl,
            
            
            
            
            
            
            "User-Agent": self.userAgent,
        })

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.getNewrelicTimestamp()}'

        imgContent = b64encode(self.session.get(self.challengeImgs[self.imageCounter]).content)

        self.imageCounter += 1

        return imgContent
    
    def submitTileAnswer(self, tile) -> dict:
        tile += 1

        if tile > 3:
            x = ((tile - 3) * 100) - randint(2, 98)
            y = randint(102, 200)
        else:
            x = (tile * 100) - randint(2, 98)
            y = randint(1, 98)
        
        px = str((x // 3) / 100)
        py = str((y // 2) / 100)

        self.answerHistory.append({"px": px, "py": py, "x": x, "y": y})

        guess = cryptojsEncrypt(dumps(self.answerHistory).replace(" ", ""), self.sessionToken, False)
        requestedId = cryptojsEncrypt(self.sc, f"REQUESTED{self.sessionToken}ID", False)

        self.session.headers = {
            "Accept": "*/*",
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Accept-Language": self.acceptLanguage,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.challengeInfo["surl"],
            "Referer": self.embedUrl,
            
            
            
            
            
            
            "User-Agent": self.userAgent,
            "X-NewRelic-Timestamp": self.getNewrelicTimestamp(),
            "X-Requested-ID": requestedId,
            "X-Requested-With": "XMLHttpRequest"
        }

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.session.headers["X-NewRelic-Timestamp"]}'

        self.session.headers = self.sortHeaders(self.session.headers)

        data = {
            "session_token": self.sessionToken,
            "game_token": self.challengeId,
            "sid": self.sid,
            "guess": guess,
            "render_type": "canvas",
            "analytics_tier": str(self.analyticsTier),
            "bio": self.biometrics,
            "is_compatibility_mode": "false"
        }

        return self.session.post(f"{self.challengeInfo["surl"]}/fc/ca/", data=self.urlencode(data)).json()
    
    def submitIndexAnswer(self, index) -> dict:
        self.session.headers = self.sortHeaders({
            "Accept": "*/*",
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Accept-Language": self.acceptLanguage,
            'Connection': 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.challengeInfo["surl"],
            "Referer": self.embedUrl,
            
            
            
            
            
            
            "User-Agent": self.userAgent
        })

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.getNewrelicTimestamp()}'

        splitToken = self.sessionToken.split(".")
        tokenPart1, tokenPart2 = splitToken[0], splitToken[1]

        self.answerHistory.append({"index": index})
        self.tguessHistory.append({"index": str(index), tokenPart1: tokenPart2})

        dapibTguess = None
        
        if self.dapibUrl != None:
            dapibSolver = dapib(self.session, self.dapibUrl, self.challengeInfo["surl"])
            dapibTguess = dapibSolver.getTguess(self.tguessHistory, self.tguessCalled)

            self.tguessCalled += 1

        guess = cryptojsEncrypt(dumps(self.answerHistory).replace(" ", ""), self.sessionToken, False)
        tguess = cryptojsEncrypt(dumps(self.tguessHistory).replace(" ", ""), self.sessionToken, False) if dapibTguess == None else cryptojsEncrypt(dapibTguess, self.sessionToken, False)
        requestedId = cryptojsEncrypt(self.sc, f"REQUESTED{self.sessionToken}ID", False)

        self.session.headers = {
            "Accept": "*/*",
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Accept-Language": self.acceptLanguage,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.challengeInfo["surl"],
            "Referer": self.embedUrl,
            
            
            
            
            
            
            "User-Agent": self.userAgent,
            "X-NewRelic-Timestamp": self.getNewrelicTimestamp(),
            "X-Requested-ID": requestedId,
            "X-Requested-With": "XMLHttpRequest"
        }

        self.session.cookies.clear()
        self.session.headers["Cookie"] = f'{self.cfuvid}; timestamp={self.session.headers["X-NewRelic-Timestamp"]}'

        self.session.headers = self.sortHeaders(self.session.headers)

        data = {
            "session_token": self.sessionToken,
            "game_token": self.challengeId,
            "sid": self.sid,
            "guess": guess,
            "render_type": "canvas",
            "analytics_tier": str(self.analyticsTier),
            "bio": self.biometrics,
            "is_compatibility_mode": "false",
            "tguess": tguess
        }

        return self.session.post(f"{self.challengeInfo["surl"]}/fc/ca/", data=self.urlencode(data)).json()