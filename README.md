# DoHClient Python Module

## Description

The DoHClient module in Python performs reverse DNS lookups for IPv4 addresses via DNS over HTTPS (DoH) using the Quad9 DoH endpoint. It includes caching and logging functionalities for efficiency and easier debugging. **Note: This module currently only supports IPv4 addresses.**

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

## Features

- **IPv4 Support**: This module is currently limited to IPv4 addresses.
- Uses the Quad9 DoH Endpoint for DNS lookups
- Caches DNS lookups for faster repeated queries
- Validates IPv4 addresses
- Includes retries for failed requests
- Logs events and errors

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License.
