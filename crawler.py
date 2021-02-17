import asyncio
import fetcher
import time
import json

# An object to store the entire data
resultDataSet = {}

# To handle the total limit of 10 set by the server
SERVER_UPPER_LIMIT = 9
DELAY_RATE = 60/(SERVER_UPPER_LIMIT+1)

""" This function takes in a limit parameter and converts it into a semaphore, this semaphore is then passed onto the 
fetcher constructor to throttle the rate of requests sent per minute. After the result is fetched this entire result is then 
stored in a json file called data.json"""

async def main(delay_rate, server_upper_limit):
    server_upper_limit = asyncio.Semaphore(server_upper_limit)
    obj = fetcher.Fetcher(delay_rate=delay_rate, server_upper_limit=server_upper_limit)
    resultDataSet = await obj.main()
    resultDataSet = {"database":resultDataSet}
    with open('./data.json', 'w') as json_file:
        json_file.write(json.dumps(resultDataSet))
    
    time.sleep(0.1)


resultDataSet = asyncio.get_event_loop().run_until_complete(main(DELAY_RATE,SERVER_UPPER_LIMIT))