# DoH Client with Caching

## Overview

This Python module implements a simple DNS over HTTPS (DoH) client for performing reverse DNS lookups. It utilizes the Quad9 DoH endpoint and includes a Least Recently Used (LRU) cache with time-based eviction policies to minimize network requests and improve performance.

## Features

- **Reverse DNS Lookup**: Translates IP addresses to domain names using DoH.
- **Cache Support**: Includes a caching mechanism to store previous lookups.
- **Error Handling**: Implements retries for network errors.
- **Logging**: Detailed logging to assist in debugging.
- **Time-based Cache Eviction**: Removes stale cache entries based on a configurable time duration.

## Requirements

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```bash
pip install requests
```

## Usage

To use this DoH client, simply import the `DoHClient` class and create an instance. Then, you can perform a reverse DNS lookup by calling the `reverse_lookup` method:

```python
from doh_client import DoHClient  # Assume your file is named doh_client.py

client = DoHClient()
domain = client.reverse_lookup("8.8.8.8")
print(domain)
```

### Logging

To enable logging, set up logging as follows:

```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

## Classes and Methods

### Cache Class

This class is an LRU cache with eviction policies based on time duration and maximum size. Methods include:

- `add(key, value)`: Adds a key-value pair to the cache.
- `retrieve(key)`: Retrieves a non-stale value from the cache if available.
- `evict()`: Evicts stale entries from the cache.

### DoHClient Class

This is the main class for handling DNS over HTTPS queries. Methods include:

- `reverse_lookup(ip_address)`: Performs a reverse DNS lookup for the given IP address.

## Potential Enhancements

- Add configurable parameters for DoH endpoint and other constants.
- Introduce asynchronous handling for multiple requests.
- Increase test coverage for more robust functionality.

```

