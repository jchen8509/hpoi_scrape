import asyncio
import aiohttp
from collections import namedtuple
from dotenv import load_dotenv
import json
import os
from urllib.parse import quote

load_dotenv()
apiKey = str(os.getenv("API_KEY"))

# --Model to store results--
TranslateReponseModel = namedtuple('TranslateReponseModel', 
                                   ['sourceText', 'translatedText', 'detectedSourceLanguage']) 

# --Logging json0--
def Logger(json_message):
    print(json.dumps(json_message))

async def DownloadString(session, url, index):
    while True:         # Will retry if client error
        try:
            r = await session.get(url)
            text = await r.text()
            # Logger({"data": html, "status": r.status})
            r.raise_for_status()        # Will error if API returns 4xx or 5xx status
            return text
        except aiohttp.ClientConnectionError as e:
            Logger({"Exception": f"Index{index}) - connection was dropped before we finished", 'Details': str(e), 'Url': url })
        except aiohttp.ClientError as e:
            Logger({'Exception': f"Index {index} - something went wrong. Not a connection error, that was handled", 'Details': str(e), 'Url': url})

def FormatResponse(sourceText, responseText):
    jsonResponse = json.loads(responseText)
    return TranslateReponseModel(sourceText, jsonResponse["data"]["translations"][0]["translatedText"], jsonResponse["data"]["translations"][0]["detectedSourceLanguage"])

def TranslatorUriBuilder(targetLanguage, sourceText):
    # TODO This is a 41 characters API Key. You'll need to generate one (it's not part of the json certificate)
    return f"https://translation.googleapis.com/language/translate/v2?key={apiKey}={quote(sourceText)}&target={targetLanguage}"

async def Process(session, sourceText, lineNumber):
    translateUri = TranslatorUriBuilder('en', sourceText) # Country code is set to en (English)
    translatedResponseText = await DownloadString(session, translateUri, lineNumber)
    response = FormatResponse(sourceText, translatedResponseText)
    return response

async def main():       
    statements = ["this is another sentence"] # 20000

    Logger({'Message': f'Start running Google Translate API for {len(statements)}'})
    results = []
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[Process(session, val, idx) for idx, val in enumerate(statements)]  )  

    Logger({'Message': f'Results are: {", ".join(map(str, [x.translatedText for x in results]))}'})
    Logger({'Message': f'Finished running Google Translate API for {str(len(statements))} and got {str(len(results))} results'})

if __name__ == '__main__':
    asyncio.run(main())

