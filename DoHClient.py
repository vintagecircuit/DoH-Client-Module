import requests
import ipaddress
from doh_cache import Cache
from doh_logger import setup_logger


logger = setup_logger('DoHClient')

class DoHClient:
    """
    DoHClient class for performing reverse DNS lookups via DNS over HTTPS (DoH).
    This class uses the Quad9 DoH endpoint to perform reverse DNS lookups and caches the results.
    """

    QUAD9_DOH_ENDPOINT = "https://dns.quad9.net/dns-query"
    CACHE_DURATION = 300  # Cache duration in seconds (5 minutes).
    TIMEOUT = 30  # Request timeout in seconds.
    RETRIES = 3  # Number of retries for failed requests.
    
    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            ipaddress.IPv4Address(ip_address)
            return True
        except ipaddress.AddressValueError:
            return False

    def reverse_lookup(self, ip_address):
        """Perform a reverse DNS lookup for an IP address.

        Parameters:
            ip_address: The IP address to lookup.
    
        Returns:
            The domain name if the lookup is successful, otherwise None.
        """
        if not DoHClient.is_valid_ipv4(ip_address):
            logger.error(f"Invalid IPv4 address: {ip_address}")
            return None

        # Check if the domain is in the cache.
        cached_domain = self.cache.retrieve(ip_address)
        if cached_domain:
            return cached_domain

        # If not in cache, fetch from the DoH server.
        response = self._fetch_from_doh(ip_address)
        if response is not None:  # Make sure response is not None
            domain_name = self._parse_dns_response(response)
            self.cache.add(ip_address, domain_name)  # Add the domain name to the cache.
            return domain_name
        else:
            return None

    def __init__(self):
        """
        Initialize the DoHClient object with a Cache object.
        """
        self.cache = Cache(self.CACHE_DURATION)

    @staticmethod
    def _convert_to_reverse_format(ip_address: str) -> str:
        """
        Convert an IPv4 address to its reverse DNS format.
        
        Parameters:
            ip_address (str): The IPv4 address to convert.
        
        Returns:
            str: The IP address in reverse DNS format.
        """
        reversed_ip = ".".join(ip_address.split(".")[::-1])
        return f"{reversed_ip}.in-addr.arpa"

    @staticmethod
    def _build_dns_query(ip_address: str) -> bytes:
        """
        Build a binary DNS query for a given IP address.
        
        Parameters:
            ip_address (str): The IPv4 address for which to build the query.
        
        Returns:
            bytes: The binary DNS query.
        """
        domain = DoHClient._convert_to_reverse_format(ip_address)
        header = b'\x12\x34' + b'\x01\x00' + b'\x00\x01' + b'\x00\x00' * 3
        qname = b''.join(bytes([len(part)]) + part.encode() for part in domain.split('.')) + b'\x00'
        qtype = b'\x00\x0c'
        qclass = b'\x00\x01'
        return header + qname + qtype + qclass

    def _fetch_from_doh(self, ip_address):
        """Fetch the DNS response from the Quad9 DoH server.
    
        Parameters:
            ip_address (str): The IPv4 address to query.
    
        Returns:
            bytes or None: The binary DNS response, or None if the query fails."""
            
        dns_query = self._build_dns_query(ip_address)
        headers = {
            "Content-Type": "application/dns-message",
            "Accept": "application/dns-message"
        }
        for attempt in range(self.RETRIES):
            try:
                response = requests.post(self.QUAD9_DOH_ENDPOINT, data=dns_query, headers=headers, timeout=self.TIMEOUT)
                response.raise_for_status()
                return response.content

            except requests.Timeout:
                logger.warning(f"Timeout occurred on attempt {attempt + 1} for IP {ip_address}")

            except requests.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1} for IP {ip_address}")

            except requests.HTTPError as e:
                logger.error(f"HTTP error occurred on attempt {attempt + 1} for IP {ip_address}: {e}")

            except requests.RequestException as e:
                logger.error(f"An unknown request error occurred on attempt {attempt + 1} for IP {ip_address}: {e}")

        logger.error(f"All attempts failed for IP {ip_address}")
        return None


    @staticmethod
    def _parse_dns_response(response_data):
        """
        Parse the binary DNS response to extract the domain name.
        
        Parameters:
            response_data (bytes): The binary DNS response.
        
        Returns:
            str: The extracted domain name.
        """
        offset = 12
        while response_data[offset] != 0:
            offset += 1 + response_data[offset]
        offset += 5
        offset += 2
        domain_name = DoHClient._extract_domain_name(response_data, offset + 10)
        return domain_name

    @staticmethod
    def _extract_domain_name(data, offset):
        """
        Recursively extract the domain name from the DNS response.
        
        Parameters:
            data (bytes): The binary DNS response.
            offset (int): The starting point for domain name extraction in the DNS response.
        
        Returns:
            str: The extracted domain name.
        """
        domain_name = ""
        while True:
            length = data[offset]
            if length == 0:
                break
            if (length & 0xC0) == 0xC0:
                pointer_offset = ((length & 0x3F) << 8) + data[offset + 1]
                domain_name += DoHClient._extract_domain_name(data, pointer_offset)
                break
            domain_name += data[offset + 1:offset + 1 + length].decode() + "."
            offset += 1 + length
        return domain_name
