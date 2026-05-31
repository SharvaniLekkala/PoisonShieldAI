# memory/short_term.py

from collections import deque

short_term_memory = deque(maxlen=10)


def add_memory(memory):

    short_term_memory.append(memory)


def get_memory():

    return list(short_term_memory)