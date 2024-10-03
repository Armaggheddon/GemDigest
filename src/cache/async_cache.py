from collections import OrderedDict
from typing import Callable
from functools import wraps

class AsyncCache:
    
    @staticmethod
    def lru_cache(max_size: int = 128):
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
                    # If no exception is raised,
                    # then the result is in the cache
                    val = _cache[key]
                    _cache.move_to_end(key)
                    result = val
                    
                    
                except KeyError:
                    # Result needs to be cached
                    result = await func(*args, **kwargs)
                    _cache[key] = result
                    
                    # If the cache is full, remove the first item
                    if len(_cache) > max_size:
                        _cache.popitem(last=False)
                    
                return result
            
            return wrapper
        return decorator
    
