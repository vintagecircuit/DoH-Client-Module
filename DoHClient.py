import requests
import struct
import time
import logging
from collections import OrderedDict

# Set up logging for the library
logger = logging.getLogger('DoHClient')

class Cache:
    """A simple in-memory LRU cache for domain names."""

    def __init__(self, duration, max_size=100, eviction_frequency=60):
        self.cache = OrderedDict()  # Maintains order of entries based on their use.
        self.duration = duration  # Time duration (seconds) after which an entry becomes stale.
        self.max_size = max_size  # Maximum cache size.
        self.last_eviction_time = time.time()  # Timestamp for the last eviction action.
        self.eviction_frequency = eviction_frequency  # Interval (seconds) between eviction checks.

    def add(self, key, value):
        """Add an entry to the cache."""
        # If the key already exists, remove it so the new entry becomes the latest.
        if key in self.cache:
            self.cache.pop(key)
        # If cache is full, evict entries until we are under max_size.
        elif len(self.cache) >= self.max_size:
            while len(self.cache) >= self.max_size:
                evicted_key, _ = self.cache.popitem(last=False)
                logger.debug(f"Evicted oldest entry from cache for IP: {evicted_key}")
        # Add the new entry.
        self.cache[key] = (value, time.time())
        logger.debug(f"Added entry to cache for IP: {key}")

    def retrieve(self, key):
        """Retrieve an entry from the cache if it's not stale."""
    
        # Check if it's time to evict based on time and size
        current_time = time.time()
        if current_time - self.last_eviction_time > self.eviction_frequency:
            self.evict()  # Handle time-based eviction.
            # Handle size-based eviction.
            while len(self.cache) > self.max_size:
                evicted_key, _ = self.cache.popitem(last=False)
                logger.debug(f"Evicted oldest entry from cache for IP: {evicted_key}")
            self.last_eviction_time = current_time
        
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
            logger.debug(f"Evicted stale entry from cache for IP: {key}")

class DoHClient:
    """A simple DNS over HTTPS client for reverse DNS lookups with caching."""

    QUAD9_DOH_ENDPOINT = "https://dns.quad9.net/dns-query"
    CACHE_DURATION = 300  # Cache duration in seconds (5 minutes).
    TIMEOUT = 30  # Request timeout in seconds.
    RETRIES = 3  # Number of retries for failed requests.

    def __init__(self):
        self.cache = Cache(self.CACHE_DURATION)

    @staticmethod
    def _convert_to_reverse_format(ip_address):
        """Convert an IP address to its reverse DNS format."""
        reversed_ip = ".".join(ip_address.split(".")[::-1])
        return f"{reversed_ip}.in-addr.arpa"

    @staticmethod
    def _build_dns_query(ip_address):
        """Build a binary DNS query for a given IP address."""
        domain = DoHClient._convert_to_reverse_format(ip_address)
        # Create a DNS header. Byte values are based on DNS message structure.
        header = b'\x12\x34' + b'\x01\x00' + b'\x00\x01' + b'\x00\x00' * 3
        qname = b''.join(bytes([len(part)]) + part.encode() for part in domain.split('.')) + b'\x00'
        qtype = b'\x00\x0c'  # PTR record type
        qclass = b'\x00\x01'  # IN class for Internet
        return header + qname + qtype + qclass

    def _fetch_from_doh(self, ip_address):
        """Fetch the DNS response from the DoH server."""
        dns_query = self._build_dns_query(ip_address)
        headers = {
            "Content-Type": "application/dns-message",
            "Accept": "application/dns-message"
        }
        # Retry the request if it fails.
        for attempt in range(self.RETRIES):
            try:
                response = requests.post(self.QUAD9_DOH_ENDPOINT, data=dns_query, headers=headers, timeout=self.TIMEOUT)
                response.raise_for_status()
                logger.info(f"Sent request for IP: {ip_address}")
                return response.content
            # Handle various types of request exceptions.
            except requests.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1} for IP {ip_address}")
            except requests.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1} for IP {ip_address}")
            except requests.HTTPError as e:
                logger.error(f"HTTP error on attempt {attempt + 1} for IP {ip_address}: {e}")
            except requests.RequestException:
                logger.error(f"Request failed on attempt {attempt + 1} for IP {ip_address}")
        # Return None if all attempts failed.
        return None

    def _parse_dns_response(self, response):
        """Parse the DNS response to extract the domain name."""
        # DNS message structure means domain data starts from the 13th byte.
        # Next 2 bytes represent the domain name length.
        domain_length = struct.unpack('>H', response[12:14])[0]
        # Extract and decode the domain name.
        domain_name = response[14:14 + domain_length].decode()
        return domain_name

    def reverse_lookup(self, ip_address):
        """Perform a reverse DNS lookup."""
        # Check if the domain is in the cache.
        cached_domain = self.cache.retrieve(ip_address)
        if cached_domain:
            logger.info(f"Cache hit for IP: {ip_address}")
            return cached_domain
        
        # If not in cache, fetch from the DoH server.
        response = self._fetch_from_doh(ip_address)
        if response:
            domain_name = self._parse_dns_response(response)
            self.cache.add(ip_address, domain_name)  # Add the domain name to the cache.
            return domain_name
        else:
            logger.error(f"Failed to retrieve domain for IP: {ip_address}")
            return None

    @staticmethod
    def _extract_domain_name(data, offset):
        """Recursively extract the domain name from the DNS response."""
        domain_name = ""
        while True:
            # Ensure we don't access out of bounds
            if offset >= len(data):
                logger.warning("Received a malformed DNS response. Unexpected end of data.")
                return ""

            length = data[offset]
            if length == 0:
                break

            # DNS compression pointer detection
            if (length & 0xC0) == 0xC0:  
                # Decompress the pointer
                pointer_offset = ((length & 0x3F) << 8) + data[offset + 1]
                domain_name += DoHClient._extract_domain_name(data, pointer_offset)
                break

            # Read the domain name segment
            domain_name += data[offset + 1:offset + 1 + length].decode() + "."
            offset += 1 + length

        return domain_name


# For users who want to see logs, they can set up logging as follows:
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Example usage:
# client = DoHClient()
# domain = client.reverse_lookup("8.8.8.8")
# print(domain)
