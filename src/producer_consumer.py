"""
 producer is a part of the system that generates items asynchronously -  ex.
 task is to import this data file -> the producer churns out files
 charge this card -> callback from the bank
 etc.
 consumer is another part of the system that is also running asynchronously and is looking for work to be done,
 it will pick up jobs created by the producer and start working on them

"""
import asyncio
import datetime as dt
import random

import colorama

async def generate_data(num: int, data: asyncio.Queue):
    for i in range(1, num + 1):
        item = i ** 2
        # warning: coroutine 'put' is not awaited
        await data.put((item, dt.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {i}", flush=True)
        # flush=True to make sure there is no delay in the buffer when we print stuff
        # as soon as we say print, we see it
        # time.sleep(random.random() + 0.5)
        # time.sleep() puts the entire loop, the entire thread to sleep
        await asyncio.sleep(random.random() + 0.5)
        # asyncio.sleep() - "I'm done for a while, you can continue working"

async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()

        processed += 1
        value = item[0]
        timestamp = item[1]
        time_finished = dt.datetime.now() - timestamp
        print(colorama.Fore.CYAN + " +++ Processed value {} after {:,.2f} sec".format(value, time_finished.total_seconds()))
        await asyncio.sleep(0.5)

"""
converting into async
1. get the event loop + run until complete 
2. data is a list - use a different data structure -> asyncio.Queue()
    you can continou doing other work until something comes into this queue then you can wake up resume my coroutine and 
    get it running
"""
def main():
    loop = asyncio.get_event_loop()

    t0 = dt.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    data = asyncio.Queue() 
    # like a generator function, it doesn't actually run until you start it
    task1 = loop.create_task(generate_data(20, data))
    task12 = loop.create_task(generate_data(20, data))
    task2 = loop.create_task(process_data(40, data))
    # convenience method for creating one big task to be passed to the event loop - still nothing "happens" here
    full_task = asyncio.gather(task1, task12, task2)
    # stuff start happening here:
    loop.run_until_complete(full_task)

    time_finished = dt.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(time_finished.total_seconds()))


if __name__ == "__main__":
    main()