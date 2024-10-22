from curl_cffi import requests
from random import choice, randint

class ipIntelligence:
    
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def getIpInfo(self) -> dict:
        responseJson = self.session.get("https://api.ipgeolocation.io/ipgeo", headers={"Origin": "https://ipgeolocation.io", "Referer": "https://ipgeolocation.io/"}).json()
        timezone = responseJson['time_zone']

        timezoneOffset = timezone["current_time"][-3] if timezone["current_time"][-4] == "0" else timezone["current_time"][-4:-2]
        timezoneOffset = -int(timezoneOffset) * 60 if timezone["current_time"][-5] == "+" else int(timezoneOffset) * 60

        languages = responseJson["languages"].split(",")[0]
        
        if len(languages) == 2:
            languages = f"{languages}-{languages.upper()}"
        
        mainLanguage = languages if "," not in languages else languages

        languages = []

        languages.append(mainLanguage)
        languages.append(mainLanguage.split('-')[0])

        for _ in range(randint(1, 2)):
            while True:
                languageToAdd = self.getRandomLanguage().split("-")[0]

                if languageToAdd not in languages:
                    break

            languages.append(languageToAdd)

        languages = ','.join(languages)

        acceptLanguage = self.languagesToAcceptLanguage(languages)

        return {
            "timezoneOffset": timezoneOffset,
            "language": mainLanguage,
            "languages": languages,
            "acceptLanguage": acceptLanguage
        }

    def languagesToAcceptLanguage(self, languages) -> str:
        languages = languages.split(',')
        result = []
        
        for i, lang in enumerate(languages):
            if i == 0:
                result.append(lang)
            else:
                qValue = 1.0 - (i * 0.1)
                result.append(f"{lang};q={qValue:.1f}")
        
        return ','.join(result)
    
    def getRandomLanguage(self) -> str:
        languages = [
            "af-ZA", "ar-AE", "ar-BH", "ar-DZ", "ar-EG", "ar-IQ", "ar-JO", "ar-KW", "ar-LB", "ar-LY", "ar-MA", "ar-OM", "ar-QA", 
            "ar-SA", "ar-SY", "ar-TN", "az-AZ", "be-BY", "bg-BG", "bs-BA", "ca-ES", "cy-GB", "da-DK", "de-AT", "de-CH", "de-DE", 
            "de-LI", "de-LU", "dv-MV", "el-GR", "en-AU", "en-BZ", "en-CA", "en-CB", "en-GB", "en-IE", "en-JM", "en-NZ", "en-PH", 
            "en-TT", "en-US", "en-ZA", "en-ZW", "es-AR", "es-BO", "es-CL", "es-CO", "es-CR", "es-DO", "es-EC", "es-ES", "es-GT", 
            "es-HN", "es-MX", "es-NI", "es-PA", "es-PE", "es-PR", "es-PY", "es-SV", "es-UY", "es-VE", "et-EE", "eu-ES", "fa-IR", 
            "fi-FI", "fo-FO", "fr-BE", "fr-CA", "fr-CH", "fr-FR", "fr-LU", "fr-MC", "gl-ES", "gu-IN", "he-IL", "hi-IN", "hr-BA", 
            "hr-HR", "hu-HU", "hy-AM", "id-ID", "is-IS", "it-CH", "it-IT", "ja-JP", "ka-GE", "kk-KZ", "kn-IN", "ko-KR", "kok-IN", 
            "ky-KG", "lt-LT", "lv-LV", "mi-NZ", "mk-MK", "mn-MN", "mr-IN", "ms-BN", "ms-MY", "mt-MT", "nb-NO", "nl-BE", "nl-NL", 
            "nn-NO", "ns-ZA", "pa-IN", "pl-PL", "ps-AR", "pt-BR", "pt-PT", "qu-BO", "qu-EC", "qu-PE", "ro-RO", "ru-RU", "sa-IN", 
            "se-FI", "se-NO", "se-SE", "sk-SK", "sl-SI", "sq-AL", "sr-BA", "sr-SP", "sv-FI", "sv-SE", "sw-KE", "syr-SY", "ta-IN", 
            "te-IN", "th-TH", "tl-PH", "tn-ZA", "tr-TR", "tt-RU", "ts", "uk-UA", "ur-PK", "uz-UZ", "vi-VN", "xh-ZA", "zh-CN", 
            "zh-HK", "zh-MO", "zh-SG", "zh-TW", "zu-ZA"
        ]

        return choice(languages)