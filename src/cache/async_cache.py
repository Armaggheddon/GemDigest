from collections import OrderedDict
from typing import Callable, Any
from dataclasses import dataclass, field
from functools import wraps
import time

@dataclass
class CacheEntry:
    age: float = field(default_factory=time.time, init=False)
    value: Any = field(init=True)


def lru_cache_with_age(max_size: int = 128, max_age: int = -1, refresh_on_access: bool = False):
    
    # max_age is in seconds!, use -1 for no expiration
    # refresh_on_access -> determines if the cache max_age should
    # be updated on access, if False, the cache will expire after max_age 
    # seconds regardless of access

    def decorator(func: Callable):
        
        # Cache specific for each decorated function,
        # so that each function has its own cache
        _cache = OrderedDict()
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Cache based on function arguments that are hashable
            key = (args, frozenset(kwargs.items()))
            
            result = None

            try:
                cached_item = _cache[key]
                age, val = cached_item.age, cached_item.value

                if max_age != -1 and time.time() - age > max_age:
                    _cache.pop(key)
                    raise KeyError
                else:
                    # update the age of the cache entry
                    if refresh_on_access: 
                        _cache[key].age = time.time()
                    _cache.move_to_end(key)
                    result = val
            except KeyError:
                result = await func(*args, **kwargs)
                _cache[key] = CacheEntry(value=result)
                if len(_cache) > max_size:
                    _cache.popitem(last=False)
                
            return result
        return wrapper
    return decorator
    
