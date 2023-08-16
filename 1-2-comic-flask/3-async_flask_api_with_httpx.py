# https://flask.palletsprojects.com/en/2.3.x/
# https://www.python-httpx.org/async/
# https://flask.palletsprojects.com/en/2.3.x/quickstart/#rendering-templates

import asyncio
import time
from random import randint
import httpx
from flask import Flask, render_template

app = Flask(__name__)

#converted to coroutine
async def get_xkcd_image(session):
    comicid = randint(0, 1000)
    resp_img = await session.get(f'https://xkcd.com/{comicid}/info.0.json')

    return resp_img.json()['img']

#converted to coroutine
async def get_multiple_images(number): 

    async with httpx.AsyncClient() as client:
        tasks = [get_xkcd_image(client) for _ in range(number)]
        urls = await asyncio.gather(*tasks)

    return urls

@app.get('/comic')
async def hello(): 

    start = time.perf_counter()
    urls = await get_multiple_images(100)
    print(urls)
    end = time.perf_counter()

    return render_template('index.html', end=end, start=start, urls=urls)
    

if __name__ == '__main__':
    app.run(debug=True, port=5555)