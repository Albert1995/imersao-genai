from time import sleep, time
import sys
import math

def ft_progress(lst):

    is_enumerable = type(lst) in [tuple, list, range]

    if not is_enumerable:
        raise Exception("lst must be a list-like")
    
    total_items = len(lst)
    start_time = time()
    last_msg_length = 0

    for idx, num in enumerate(lst):
        curr_item = idx + 1
        progress = (curr_item / total_items) * 100
        progress = math.trunc(progress)
        
        progress_bar = ("=" * (int(progress / 10) - 1)) + ">"

        curr_time = time()
        elapsed_time = curr_time - start_time

        # para evitar divisão por 0 no calculo do ETA, items_per_sec inicia com 1
        if curr_item == 1:
            items_per_sec = 1
        else:
            items_per_sec = ((curr_item - 1) / elapsed_time)

        remaining_items = total_items - curr_item
        eta = remaining_items / items_per_sec

        msg = f"ETA: {eta:.2f}s [{progress:3}%][{progress_bar:10}] {curr_item}/{total_items} | elapsed time {elapsed_time:.2f}s\r"
        
        sys.stdout.write(" " * last_msg_length + "\r")
        sys.stdout.write(msg)
        last_msg_length = len(msg)
        
        yield num


a_list = range(1000)
ret = 0
for elem in ft_progress(a_list):
    ret += (elem + 3) % 5
    sleep(0.01)
print()
print(ret)