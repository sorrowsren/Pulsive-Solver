from curl_cffi import requests
from re import search, sub
from subprocess import run, PIPE

class dapib:

    def __init__(self, session: requests.Session, url: str, surl: str) -> None:
        self.session = session
        self.url = url
        self.surl = surl
    
    def getTguess(self, answers: list, tguessCalled: int) -> str:
        pattern = r'([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/(\d+)'
        match = search(pattern, self.url)

        uuid = match.group(1)
        number = match.group(2)

        if tguessCalled == 0:
            self.session.headers.pop("Origin")
            self.session.get(f"{self.surl}/params/sri/dapib/{uuid}/{number}")
            self.session.headers["Origin"] = self.surl

        self.session.headers["Sec-Fetch-Dest"] = "script"
        self.jsCode = self.session.get(self.url).text
        self.session.headers["Sec-Fetch-Dest"] = "empty"

        self.jsCode = self.jsCode.replace("(function(){const ", "function main(){const ")
        pattern = r'function\s+(\w+)\(answers\)'
        match = search(pattern, self.jsCode)
        functionName = match.group(1)
        self.jsCode = sub(r'try{.+', '{try{console.log(JSON.stringify(' + functionName + '(' + str(answers) + ')));}catch(e){}}};main();', self.jsCode)

        result = run(["node", "-e", self.jsCode], stdout=PIPE).stdout.decode("utf-8").strip("\n")
        
        return result