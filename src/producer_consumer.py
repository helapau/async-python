"""
 producer is a part of the system that generates items asynchronously -  ex.
 task is to import this data file -> the producer churns out files
 charge this card -> callback from the bank
 etc.
 consumer is another part of the system that is also running asynchronously and is looking for work to be done,
 it will pick up jobs created by the producer and start working on them

"""
import datetime as dt
import time
import random

import colorama

def generate_data(num: int, data: list):
    for i in range(1, num + 1):
        item = i ** 2
        data.append((item, dt.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {i}", flush=True)
        # flush=True to make sure there is no delay in the buffer when we print stuff
        # as soon as we say print, we see it
        time.sleep(random.random() + 0.5)

def process_data(num: int, data: list):
    processed = 0
    while processed < num:
        item = data.pop(0)
        if item is None:
            time.sleep(0.01)
            continue
        processed += 1
        value = item[0]
        timestamp = item[1]
        time_finished = dt.datetime.now() - timestamp
        print(colorama.Fore.CYAN + " +++ Processed value {} after {:,.2f} sec".format(value, time_finished.total_seconds()))


def main():
    t0 = dt.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    data = []

    generate_data(20, data)
    process_data(20, data)

    time_finished = dt.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(time_finished.total_seconds()))


if __name__ == "__main__":
    main()