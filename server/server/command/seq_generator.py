
import threading

current_seq_id = 0
lock = threading.Lock()


# This is a naive implementation of seq_generator. It should be backed by
# DB or some equivilant, so the seq_id is unique across peers.
def next_seq_id():
    with lock:
        global current_seq_id
        current_seq_id += 1
        return current_seq_id


# Mainly for test purpose
def _set_seq_id(seq_id):
    with lock:
        global current_seq_id
        current_seq_id = seq_id
