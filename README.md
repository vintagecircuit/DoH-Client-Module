# DoHClient Python Module

## Description

The DoHClient module performs reverse DNS lookups for IPv4 addresses via DNS over HTTPS (DoH) using the Quad9 DoH endpoint. It includes caching and logging functionalities for efficiency and easier debugging.

**Note**: This module currently only supports IPv4 addresses.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Logging](#logging)
  - [Cache Duration](#cache-duration)
- [Components](#components)
  - [DoHClient](#dohclient)
  - [Cache](#cache)
  - [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- **IPv4 Support**: Limited to IPv4 addresses.
- **Quad9 DoH Endpoint**: Uses Quad9's secure DNS over HTTPS endpoint for domain resolution.
- **Caching**: Incorporates a caching mechanism to reduce redundant queries.
- **IPv4 Validation**: Validates IPv4 addresses.
- **Retries**: Includes retries for failed requests.
- **Logging**: Logs events and errors using the `doh_logger` custom module.

## Installation

To install this module manually, download the code and run the following command in the directory where the code is stored:

```
python setup.py install

```

## Dependencies
- Python (>= 3.6)
- `requests`
- `ipaddress`

**Note**: `doh_cache` and `doh_logger` are custom modules; ensure they are included in your project directory.

## Usage

### Basic Usage
Here's a simple example of how to use the DoHClient module:

```
python from DoHClient import DoHClient

```

doh_client = DoHClient()
result = doh_client.reverse_lookup("8.8.8.8")
print(result)


## Logging
Ensure the custom logging module, `doh_logger`, is set up before running the main module to capture all debug information.

## Cache Duration
The caching duration is set to 5 minutes by default and can be modified by adjusting the `CACHE_DURATION` static variable in the `DoHClient` class.

## Components

### DoHClient
The `DoHClient` class is responsible for reverse DNS lookups for IPv4 addresses. It integrates a caching mechanism to reduce the number of network requests. For an in-depth understanding, refer to the code documentation.

### Cache
The `Cache` class acts as an LRU (Least Recently Used) cache that retains DNS lookups for a specified timeframe. The cache has a size limit and autonomously evicts the oldest or stale entries based on size and duration.

- **Eviction Based on Time**: Cache drops entries surpassing a certain age.
- **Eviction Based on Size**: The cache keeps its size consistent by ousting the oldest entries when adding a new one, and it reaches its size cap.

### Logging
The `doh_logger` module offers a configurable logging mechanism to monitor the application's behavior, track down errors, and comprehend its flow. Each log entry consists of a timestamp, logger's name, log level, and the message.

## Contributing
Pull requests are welcome. For significant modifications, please initiate an issue first to discuss the intended changes.

## License
MIT License.

