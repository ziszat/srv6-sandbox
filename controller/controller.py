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
GET = "GET"
# Define whether to use HTTP or HTTPS
SECURE = False
# SSL certificate for server validation
CERTIFICATE = "cert_client.pem"
VIEW_PATHS_ENDPOINT = "/view-paths"
VIEW_SID_ENDPOINT = "/view-sid"
ROUTER_IPS = {
    "r0": "[2001:b::1]",
    "r1": "[2001:10::2]",
    "r2": "[2001:12::2]",
    "r3": "[2001:13::2]",
    "r4": "[2001:24::2]",
    "r5": "[2001:35::2]",
    "r6": "[2001:56::2]"
}


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


# Build an HTTP GET requests object
def get_http_get_response(ip_address, port, secure, endpoint):
    """
    Constructs an HTTP GET request for checking SRv6 paths or SIDs.
    """
    # Define URL and headers
    url = "{scheme}://{ip}:{port}/{endpoint}".format(
        scheme=("https" if secure else "http"),
        ip=ip_address,
        port=port,
        endpoint=endpoint,
    )
    # headers = {"Content-Type": CONTENT_TYPE}
    # Create a GET request object
    response = requests.get(url)
    return response


# def view_srv6_paths(ip_address, port, secure):
#     """Send GET request to view all SRv6 paths."""
#     try:
#         url = "{scheme}://{ip}:{port}/{basePath}".format(
#             scheme=("https" if secure else "http"),
#             ip=ip_address,
#             port=port,
#             basePath=VIEW_PATHS_ENDPOINT,
#         )
#         response = requests.get(url)
#         if response.status_code == 200:
#             print("SRv6 Paths:")
#             print(json.dumps(response.json(), indent=2))
#         else:
#             print(f"Failed to retrieve paths. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error retrieving SRv6 paths: {e}")

# def view_sids(ip_address, port, secure):
#     """Send GET request to view all SIDs."""
#     try:
#         url = "{scheme}://{ip}:{port}/{basePath}".format(
#             scheme=("https" if secure else "http"),
#             ip=ip_address,
#             port=port,
#             basePath=VIEW_SID_ENDPOINT,
#         )
#         response = requests.get(url)
#         if response.status_code == 200:
#             print("SID Information:")
#             print(json.dumps(response.json(), indent=2))
#         else:
#             print(f"Failed to retrieve SIDs. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error retrieving SID information: {e}")

def main():
    # User input loop
    while True:
        ip = ROUTER_IPS["r0"]
        router = input("Choose a router(r0, r1, ..., r6): ").strip().lower()
        ip = ROUTER_IPS[router]
        # Get user input for operation and paths
        print(
            "Enter 'create' to add a path, 'remove' to delete a path, or 'exit' to quit."
        )
        operation = input("Operation: ").strip().lower()
        if operation == "exit":
            break

        if operation not in ["create", "remove", "paths", "sids"]:
            print("Invalid operation. Please enter 'create', 'remove', 'paths', 'sids', or 'exit'.")
            continue

        if operation == "paths":
            try:
                url = "{scheme}://{ip}:{port}/{endpoint}".format(
                    scheme=("https" if SECURE else "http"),
                    ip=ip,
                    port=443 if SECURE else 8080,
                    endpoint=VIEW_PATHS_ENDPOINT,
                )
                response = requests.get(url, timeout=50)
                
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.content.decode('utf-8')}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            
        if operation == "sids":
            try:
                response = get_http_get_response(
                    ip, 443 if SECURE else 8080, SECURE, VIEW_SID_ENDPOINT
                )
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.content.decode('utf-8')}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        if operation == "create" or operation == "remove":
            paths = []
            while True:
                # Get user input for path data
                device = input("Enter device (e.g., eth1): ").strip()
                destination = input("Enter destination (e.g., 10.0.0.1/24): ").strip()
                encapmode = input("Enter encapsulation mode (inline or encap): ").strip()
                segments = (
                    input("Enter segments (comma-separated, e.g., fc00:1::a,fc00:2::a): ")
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
