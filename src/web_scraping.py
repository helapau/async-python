import asyncio
import datetime

import requests
import bs4
from colorama import Fore


# this is a cpu-bound thing - parsing text
async def get_title(queue: asyncio.Queue, max_num_episdoes):
    processed = 0
    while processed < max_num_episdoes:
        episode_number, html = await queue.get()
        print(Fore.YELLOW + f"Processing item no {processed+1}", flush=True)
        print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        header = soup.select_one('h1')
        if not header:
            print("MISSING", flush=True)
        print(Fore.WHITE + f"Title found : {header.text.strip()}", flush=True)
        queue.task_done()
        processed += 1
    return


# this is I/O bound - we're waiting for network response
async def get_html(episode_number: int, queue: asyncio.Queue):
    loop = asyncio.get_event_loop()
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    resp = await loop.run_in_executor(None, requests.get, url)
    resp.raise_for_status()
    await queue.put((episode_number, resp.text))


async def main():
    queue = asyncio.Queue()
    producer_tasks = []
    for n in range(20, 30):
        producer_tasks.append(asyncio.create_task(get_html(n, queue)))

    consumer_task = asyncio.create_task(get_title(queue, 10))
    await asyncio.gather(*producer_tasks, consumer_task)
    consumer_task.cancel()
    await consumer_task
    return




if __name__ == "__main__":
    asyncio.run(main())