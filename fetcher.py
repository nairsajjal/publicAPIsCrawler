import logging
import asyncio
import aiohttp
import time
import json
import urllib3
import attr
import requests_async as requests
from urllib.parse import quote

SERVER_UPPER_LIMIT = 9
DELAY_RATE = round(60/(SERVER_UPPER_LIMIT+1))
AUTH_TOKEN = {}

#Configs for logger
LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)

URL = "https://public-apis-api.herokuapp.com/api/v1/"

#The main Fetcher Class
@attr.s
class Fetcher:
    server_upper_limit = attr.ib()
    delay_rate = attr.ib(default=5, converter=int)

    async def fetchToken(self):
        tokenurl = URL+'auth/token/'
        try:
            response = await requests.get(url=tokenurl)
        except requests.exceptions.ConnectionError as err:
            print("Error\n")
            print(err)
            exit()
        else:
            try:
                status = response.status_code
                json = response.json()
                token = json["token"]
                print("Fetched the token\n")
                return token

            except json.decoder.JSONDecodeError:
                print(f"Error !")
                exit()


    async def fetchAllCategories(self, session, categories, pageNum):
        listUrl = URL+'apis/categories?page='+str(pageNum)
        try:
            response = await session.get(listUrl)
        except requests.exceptions.ConnectionError as err:
            print("Error!! \n")
            print(err)
        else:
            status = int(response.status_code)
            if(status!=200):
                if(status==429):
                    await asyncio.sleep(20)
                if(status==400 | status==401 |status==403 | status==429):
                    AUTH_TOKEN = await self.fetchToken()
                    session.headers.update({"Authorization":"Bearer= "+str(AUTH_TOKEN)})
                    await self.fetchAllCategories(session, categories, pageNum)
            else:
                try:
                    log.info(f"Current request: {listUrl}")
                    json = response.json()
                    result = json['categories']
                    # Base Condition
                    if(len(result)==0):
                        return
                    categories+=result
                    await asyncio.sleep(self.delay_rate)
                
                    await self.fetchAllCategories(session, categories, pageNum+1)
                except aiohttp.client_exceptions.ContentTypeError:
                    print(f"Error !!")
                    exit()
    
    async def fetchApiList(self, session, apiList, pageNum, category):

        url=URL+'apis/entry?page='+str(pageNum)+'&category='+quote(str(category))
    
        try:
            response = await session.get(url)
        except requests.exceptions.ConnectionError as err:
            print("Error!! \n")
            print(err)
            exit()
        else:
            status = int(response.status_code)
            if(status!=200):
                if(status==429):
                    await asyncio.sleep(20)
                if(status==403 | status==429 | status==401):
                    AUTH_TOKEN = await self.fetchToken()
                    session.headers.update({"Authorization":"Bearer= "+ str(AUTH_TOKEN)})
                    await self.fetchApiList(session, apiList, pageNum, category)
            else:
                try:
                    log.info(f"Current Category: {url}")
                    json = response.json()
                    results = json['categories']
                    #Base Condition
                    if(len(results)==0):
                        return
                    
                    apiList+=results
                    await asyncio.sleep(self.delay_rate)
                    
                    await self.fetchApiList(session,apiList, pageNum+1, category)
                except aiohttp.client_exceptions.ContentTypeError:
                    print(f"Error !!")
                    exit()

    async def main(self):
        async with self.server_upper_limit:
            AUTH_TOKEN = await self.fetchToken()

            session = requests.Session()
            session.headers.update({"Authorization":"Bearer= "+str(AUTH_TOKEN)})
            async with session:
                entire_data = {}
                categories = []
                await self.fetchAllCategories(session, categories, 1)
                await asyncio.sleep(self.delay_rate)
                for i in categories:
                    apiList = []
                    await self.fetchApiList(session, apiList, 1, i)
                    await asyncio.sleep(self.delay_rate)
                    entire_data[i] = apiList
                return entire_data