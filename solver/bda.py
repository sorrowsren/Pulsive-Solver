from time import time
from random import randint, choice
from re import sub
from json import dumps
from base64 import b64encode
from mmh3 import hash128
from solver.cryptoJs import cryptojsEncrypt
from solver.fingerprint import fingerprint
from typing import Union

class bda:

    def __init__(self, ipInfo: dict, challengeInfo: dict, browserInfo: dict) -> None:
        self.ipInfo = ipInfo
        self.challengeInfo = challengeInfo
        self.browserInfo = browserInfo
        self.userAgent = self.browserInfo["User-Agent"]
        self.fingerprint = fingerprint(self.ipInfo, self.challengeInfo, self.browserInfo)
        self.fe = self.fingerprint.getFe()
        self.preparedFe = self.jsonStringify(self.prepareFe(self.fe))
        self.preparedF = self.jsonStringify(self.prepareF(self.fe))
        self.enhancedFp = list(map(lambda x: {'key': x[0], 'value': x[1]}, self.fingerprint.getEnhancedFp().items()))
        self.ife = self.jsonStringify(dumps(self.prepareFe(self.fe))[1:-1])

    def x64hash128(self, t: str, r: int) -> str:
        o = hash128(t, r)
        return str(hex(((o & 0xffffffffffffffff) << 64) + (o >> 64))).removeprefix("0x")

    def jsonStringify(self, values: Union[str, list]) -> str:
        if type(values) == str:
            return values.replace("None", "null").replace("True", "true").replace("False", "false").replace('"', "")
        else:
            newList = []
            for value in values:
                newList.append(value.replace("None", "null").replace("True", "true").replace("False", "false").replace('"', ""))
            return newList
        
    def formatBda(self, bda: str) -> str:
        bda = sub(r'{"key":"window__tree_index","value":\[(\d+,\s*\d+)\]}', lambda match: sub(r'\s', '', match.group(0)), bda)
        return bda.replace("\\\\\\", "\\").replace('\\u2062', 'â¢').replace('\\u2063', 'â£')

    def prepareF(self, fingerprint: dict) -> str:
        f = []
        keys = list(fingerprint.keys())
        for i in range(len(keys)):
            f.append(str(fingerprint[keys[i]]))
        return ";".join(f)
    
    def prepareFe(self, fingerprint: dict) -> list:
        fe = []
        keys = list(fingerprint.keys())
        for i in range(len(keys)):
            fe.append(f"{keys[i]}:{fingerprint[keys[i]]}")
        return fe

    def getBda(self) -> str:
        currentTime = int(time())
        roundedTime = str((currentTime - (currentTime % 21600)))
        base64EncodedTime = b64encode(str(currentTime).encode("utf-8")).decode("utf-8")

        historyLength = str(randint(1, 8))

        bda = []

        bda.append(dict(
            key="api_type", value='js'
        ))

        bda.append(dict(
            key="f", value=self.x64hash128(self.preparedF, 0)
        ))

        bda.append(dict(
            key="n", value=base64EncodedTime
        ))

        bda.append(dict(
            key="wh", value=f"{''.join(choice('0123456789abcdef') for _ in range(32))}|b2e9874a9367e9bc759ed931a04f29ed"
        ))

        bda.append(dict(
            key="enhanced_fp", value=self.enhancedFp
        ))

        bda.append(dict(
            key="fe", value=self.preparedFe
        ))

        bda.append(dict(
            key="ife_hash", value=self.x64hash128(self.ife, 0)
        ))

        bda.append(dict(
            key="jsbd", value='{\\"HL\\":' + historyLength + ',\\"NCE\\":false,\\"DT\\":\\"\\",\\"NWD\\":\\"false\\",\\"DMTO\\":1,\\"DOTO\\":1}'
        ))

        bda = self.formatBda(dumps(bda, separators=(',', ':')))
        
        key = self.userAgent + roundedTime

        bda = cryptojsEncrypt(bda, key, True)

        return bda
