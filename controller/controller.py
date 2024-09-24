#!/usr/bin/python3

import requests
import json

# Global variables

# Base path for the URL
SRV6_BASE_PATH = "srv6-explicit-path"
# HTTP definitions
ACCEPT = "application/json"
CONTENT_TYPE = "application/json"
POST = "POST"
# Define whether to use HTTP or HTTPS
SECURE = False
# SSL certificate for server validation
CERTIFICATE = "cert_client.pem"


# Build an HTTP requests object
def get_http_requests(ip_address, port, secure, params, data):
    # Create a request, build the URL and headers
    url = "{scheme}://{ip}:{port}/{basePath}".format(
        scheme=("https" if secure else "http"),
        ip=ip_address,
        port=port,
        basePath=SRV6_BASE_PATH,
    )
    headers = {"Accept": ACCEPT, "Content-Type": CONTENT_TYPE}
    request = requests.Request(POST, url, data=data, headers=headers, params=params)
    return request.prepare()


def main():
    # User input loop
    while True:
        ip = "[fc00:1::1]"
        flag = input("Change route ip? (y/N)").strip().lower()
        if flag == "y":
            ip = input("Router IP: ").strip().lower()
        # Get user input for operation and paths
        print(
            "\nEnter 'create' to add a path, 'remove' to delete a path, or 'exit' to quit."
        )
        operation = input("Operation: ").strip().lower()
        if operation == "exit":
            break

        if operation not in ["create", "remove"]:
            print("Invalid operation. Please enter 'create', 'remove', or 'exit'.")
            continue

        paths = []
        while True:
            # Get user input for path data
            device = input("Enter device (e.g., eth0): ").strip()
            destination = input("Enter destination (e.g., 2222:4::2/128): ").strip()
            encapmode = input("Enter encapsulation mode (inline or encap): ").strip()
            segments = (
                input("Enter segments (comma-separated, e.g., 2222:3::2,3333:2::2): ")
                .strip()
                .split(",")
            )

            # Construct path data
            path = {
                "device": device,
                "destination": destination,
                "encapmode": encapmode,
                "segments": segments,
            }
            paths.append(path)

            # Check if user wants to add more paths
            more_paths = input("Add another path? (yes/no): ").strip().lower()
            if more_paths != "yes":
                break
        # Create data payload for HTTP request
        data = json.dumps({"paths": paths})
        params = {"operation": operation}

        # Send request
        session = requests.Session()
        try:
            request = get_http_requests(
                ip, 443 if SECURE else 8080, SECURE, params, data
            )
            response = session.send(request, verify=(CERTIFICATE if SECURE else None))
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content.decode('utf-8')}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    main()
