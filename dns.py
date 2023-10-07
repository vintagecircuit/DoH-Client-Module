from DoHClient import DoHClient

ip_address = input("Please enter the IP address for reverse lookup: ")

client = DoHClient()
result = client.reverse_lookup(ip_address)
print(result)
