from collections import OrderedDict
from typing import Callable, Any
from dataclasses import dataclass, field
from functools import wraps
import time

@dataclass
class CacheEntry:
    """Wraps a cache value with its age.
    """
    age: float = field(default_factory=time.time, init=False)
    value: Any = field(init=True)


def lru_cache_with_age(
    max_size: int = 128, 
    max_age: int = -1, 
    refresh_on_access: bool = False
):
    """
    LRU Cache with max_size, max_age and refresh_on_access parameters.
    The cache key is based on the function arguments that are hashable.

    Args:
    - max_size: the maximum number of items that the cache can store, 
    if the cache is full, the least recently used item is removed. If max_size 
    is -1, the cache has no size limit.
    - max_age: the maximum age of the cache in seconds, if the cache is older
    than max_age, it is removed. If max_age is -1, the cache never expires.
    - refresh_on_access: determines if the cache max_age should be updated on access,
    if False, the cache will expire after max_age seconds regardless of access.

    Returns:
    - wrapper: the decorated function that uses the LRU cache.

    Raises:
    - ValueError: if max_size or max_age is less than -1.
    """

    if max_size < -1:
        raise ValueError("max_size must be greater than or equal to -1")
    
    if max_age < -1:
        raise ValueError("max_age must be greater than or equal to -1")
    
    def decorator(func: Callable):
        
        # Cache specific for each decorated function,
        # so that each function has its own cache
        _cache = OrderedDict()
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Cache key is based on function arguments that are hashable
            key = (args, frozenset(kwargs.items()))
            
            result = None

            try:
                cached_item: CacheEntry = _cache[key]
                age, val = cached_item.age, cached_item.value

                if max_age != -1 and time.time() - age > max_age:
                    _cache.pop(key)
                    raise KeyError # Force cache miss
                else:
                    if refresh_on_access: 
                        _cache[key].age = time.time()
                    _cache.move_to_end(key)
                    result = val
            except KeyError:
                result = await func(*args, **kwargs)
                _cache[key] = CacheEntry(value=result)
                if max_size != -1 and len(_cache) > max_size:
                    _cache.popitem(last=False)
                
            return result
        return wrapper
    return decorator
    
