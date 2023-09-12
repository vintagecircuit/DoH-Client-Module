# DoH-Client-Module
The DoHClient module provides a simple DNS over HTTPS client for reverse DNS lookups with caching. Powered by the secure Quad9 DoH endpoint, this module ensures that your DNS queries are encrypted, private, and reliable.

## **Features**

- **Quad9 Endpoint**: Utilizes the secure and privacy-focused Quad9 DNS over HTTPS endpoint.
- **Caching**: Reduces redundant requests and improves speed by caching DNS results.
- **Retry Mechanism**: In case of failures, the client will attempt retries for a set number of times.
- **Logging**: Detailed logs for a clear understanding and easier debugging.
- **Error Handling**: Gracefully handles various potential errors for a more robust experience.
- Reverse DNS lookups over HTTPS.

- Getting Started

- ### **Prerequisites**

  - Python 3.x
- **`requests`** library (**`pip install requests`**)
- ### **Usage**

To use the **`DoHClient`** in your project:

1. Copy the **`doh_client.py`** (or whatever you've named it) to your project directory.
2. Import and create an instance of the **`DoHClient`**:

## **Configuration**

While the default DoH endpoint is Quad9, configurations like cache duration or the DoH endpoint can be altered directly in the module. For more specific or dynamic configurations, consider extending or modifying the module based on your requirements.

## **Feedback**

If you have any feedback or issues, please open a GitHub issue in this repository.
