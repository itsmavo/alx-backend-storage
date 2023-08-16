#!/usr/bin/env python3
''' Module used to carry out the Redis NoSQL tasks '''
import uuid
import redis
from typing import Any, Callable, Union
from functools import wraps

def count_calls(method: Callable) -> Callable:
    ''' Tracks num of calls made to a method in Cache class'''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''wrap decorated and return the wrapper'''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    ''' Tracks call details of a method in a Cache class '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        ''' Returns the method's output after storing its inputs and output '''
        inp_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        self._redis.rpush(inp_key, str(args))
        self._redis.rpush(out_key, method(self, *args, **kwargs))
        return method(self, *args, **kwargs)
    return wrapper

def replay(fn: Callable) -> None:
    ''' Shows history of calls of particular function '''
    rd = redis.Redis()
    fn_name = fn.__qualname__
    c = rd.get(fn_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0

    print("{} was called {} times:".format(fn_name, c))
    inp = rd.lrange("{}:inputs".format(fn_name), 0, -1)
    out = rd.lrange("{}:outputs".format(fn_name), 0, -1)
    for inpt, outp in zip(inp, out):
        print('{}(*{}) -> {}'.format(fn_name, inpt, outp))

class Cache:
    ''' Object stores data in Redis data storage '''
    def __init__(self) -> None:
        ''' Inits a Cache instance '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history        
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' Stores value in Redis and returns key'''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key
    def get(self, key: str, fn: Callable = None,) -> Union[str, bytes, int, float]:
        ''' Retrieves value from Redis '''
        return fn(self._redis.get(key)) if fn is not None else self._redis.get(key)
    
    def get_str(self, key: str) -> str:
        ''' Gets string value from Redis '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        ''' Gets int value from Redis '''
        return self.get(key, lambda x: int(x))

