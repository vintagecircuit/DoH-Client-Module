# DoHClient Python Module

## Description

The DoHClient module performs reverse DNS lookups for IPv4 addresses via DNS over HTTPS (DoH) using the Quad9 DoH endpoint. It includes caching and logging functionalities for efficiency and easier debugging.

**Note**: This module currently only supports IPv4 addresses.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
  - [DoHClient](#dohclient)
  - [Cache](#cache)
  - [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- IPv4 Support: This module is currently limited to IPv4 addresses.
- Uses Quad9 DoH Endpoint for DNS lookups.
- Caches DNS lookups for faster repeated queries.
- Validates IPv4 addresses.
- Includes retries for failed requests.
- Logs events and errors using Python's logging module.

## Installation

To install this module manually, download the code and run the following command in the directory where the code is stored:

```bash
python setup.py install
```

## Dependencies

- Python (>= 3.6)
- `requests`
- `ipaddress`

> **Note**: `doh_cache` and `doh_logger` are custom modules; please ensure you include them in your project directory.

## Usage

### Basic Usage

Here's a simple example of how to use the DoHClient module:

```python
from DoHClient import DoHClient

doh_client = DoHClient()
result = doh_client.reverse_lookup("8.8.8.8")
```

### Logging

This module uses a custom logging module called `doh_logger`. Please make sure you set it up before running this module to capture debug information.

### Cache Duration

The caching duration is set to 5 minutes by default and can be modified by changing the `CACHE_DURATION` static variable in the `DoHClient` class.

## Classes

### DoHClient

The `DoHClient` class performs reverse DNS lookups for IPv4 addresses. It also includes a caching mechanism to minimize network requests. For more details, refer to the code documentation.

### Cache

The `Cache` class is a Least Recently Used (LRU) cache that stores DNS lookups for a specified duration. The cache supports a maximum size and automatically evicts the oldest or stale entries based on size and time.

- **Eviction Based on Time**: The cache removes entries that are older than a specified duration.
- **Eviction Based on Size**: The cache maintains its size by removing the oldest entries when a new entry is added and the cache is full.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License.
