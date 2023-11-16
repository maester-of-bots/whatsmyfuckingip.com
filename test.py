import whois

domain = "thc-lab.net"  # Replace with the domain you want to look up

try:
    domain_info = whois.whois(domain)
    print(domain_info)
except Exception as e:
    print(f"Error retrieving WHOIS information: {e}")

# After retrieving domain_info as shown above
registrar = domain_info.registrar
creation_date = domain_info.creation_date
expiration_date = domain_info.expiration_date

print(f"Registrar: {registrar}")
print(f"Creation Date: {creation_date}")
print(f"Expiration Date: {expiration_date}")
