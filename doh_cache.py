import time
import logging
from collections import OrderedDict

logger = logging.getLogger('Cache')

class Cache:
    """Cache class for storing DNS lookups.
    
    This class implements an in-memory LRU cache with eviction policies based on time duration 
    and maximum size. It is used for caching DNS responses to minimize network requests.
    """
    def __init__(self, duration, max_size=100, eviction_frequency=60):
        """Initialize the Cache object."""
        self.cache = OrderedDict()  # Maintains order of entries based on their use.
        self.duration = duration  # Time duration (seconds) after which an entry becomes stale.
        self.max_size = max_size  # Maximum cache size.
        self.last_eviction_time = time.time()  # Timestamp for the last eviction action.

    def add(self, key, value):
        """Add a key-value pair to the cache.
        Parameters:
            key: The key for the cache entry, generally an IP address.
            value: The value to be stored, usually a domain name.
        """
        # If the key already exists, remove it so the new entry becomes the latest.
        if key in self.cache:
            self.cache.pop(key)
        # If cache is full, evict entries until we are under max_size.
        elif len(self.cache) >= self.max_size:
            while len(self.cache) >= self.max_size:
                evicted_key, _ = self.cache.popitem(last=False)
                #logger.debug(f"Evicted oldest entry from cache for IP: {evicted_key}")
        # Add the new entry.
        self.cache[key] = (value, time.time())
        #logger.debug(f"Added entry to cache for IP: {key}")
        
    def _evict_based_on_size(self):
        """Remove entries from the cache until the size is under max_size."""
        while len(self.cache) > self.max_size:
            evicted_key, _ = self.cache.popitem(last=False)
            #logger.debug(f"Evicted oldest entry from cache for IP: {evicted_key}")
            
    def _evict_based_on_time(self):
        """Remove stale entries from the cache."""
        current_time = time.time()
        keys_to_remove = [key for key, (_, timestamp) in self.cache.items() if current_time - timestamp >= self.duration]
        for key in keys_to_remove:
            del self.cache[key]
            #logger.debug(f"Evicted stale entry from cache for IP: {key}")

    def retrieve(self, key):
        """Retrieve an entry from the cache if it's not stale."""
        # Call the evict method to remove stale or unnecessary items
        self.evict()
    
        # If the key is present and not stale, return the associated value.
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.duration:
                return value
        # Return None if no valid entry was found.
        return None


    def evict(self):
        """Remove stale entries from the cache."""
        current_time = time.time()
        # Identify stale entries.
        keys_to_remove = [key for key, (_, timestamp) in self.cache.items() if current_time - timestamp >= self.duration]
        # Remove identified entries.
        for key in keys_to_remove:
            del self.cache[key]
            #logger.debug(f"Evicted stale entry from cache for IP: {key}")
        self._evict_based_on_size()  # Call the private method here