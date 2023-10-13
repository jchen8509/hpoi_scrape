import asyncio
import aiohttp
from dotenv import load_dotenv
import json
import os
from manual_translation import format_setter, manu_translation

load_dotenv()
apiKey = str(os.getenv("API_KEY"))

# --Logging json0--
def Logger(json_message):
    print(json.dumps(json_message))

async def DownloadString(session: aiohttp.ClientSession, sourceText, targetLanguage):
    base_url = "https://translation.googleapis.com/language/translate/v2"
    payload = {
        "key": apiKey,
        "q": sourceText,
        "target": targetLanguage
    }
    
    while True:         # Will retry if client error
        try:
            r = await session.post(base_url, params = payload)
            text = await r.text()
            # Logger({"data": html, "status": r.status})
            r.raise_for_status()        # Will error if API returns 4xx or 5xx status
            return text
        except aiohttp.ClientConnectionError as e:
            Logger({"Exception": f"Connection was dropped before we finished", 'Details': str(e)})
            return 'error'
        except aiohttp.ClientError as e:
            Logger({'Exception': f"Something went wrong. Not a connection error, that was handled", 'Details': str(e)})
            return 'error'

def FormatResponse(responseText: str) -> list[str]:
    jsonResponse = json.loads(responseText)
    translations = jsonResponse["data"]["translations"]

    return list(map(lambda t: t["translatedText"], translations))

async def Process(session: aiohttp.ClientSession, sourceTexts: list[str]):
    translatedResponseText = await DownloadString(session, sourceTexts, 'en')
    response = FormatResponse(translatedResponseText)
    return response

async def main():       
    statements = ["this is another sentence", "this also is a sentence", "third"] # 20000

    Logger({'Message': f'Start running Google Translate API for {len(statements)}'})
    async with aiohttp.ClientSession() as session:
        await Process(session, statements) 

    # Logger({'Message': f'Results are: {", ".join(map(str, [x.translatedText for x in results]))}'})
    # Logger({'Message': f'Finished running Google Translate API for {str(len(statements))} and got {str(len(results))} results'})

if __name__ == '__main__':
    asyncio.run(main())

