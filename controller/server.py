#!/usr/bin/python

from optparse import OptionParser
from pyroute2 import IPRoute
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from collections import namedtuple
from urllib.parse import parse_qs

import logging
import time
import json
import socket
import ssl

# Global variables definition

# Server reference
rest_server = None
# Netlink socket
ip_route = None
# Cache of the resolved interfaces
interfaces = ["eth1", "eth2", "eth3"]
idxs = {}
# logger reference
logger = logging.getLogger(__name__)
# Server ip/ports
REST_IP = "2001:b::1"
REST_PORT = 8080
# Debug option
SERVER_DEBUG = False
# SRv6 base path
SRV6_BASE_PATH = "/srv6-explicit-path"
# HTTP utilities
ResponseStatus = namedtuple("HTTPStatus", ["code", "message"])
ResponseData = namedtuple("ResponseData", ["status"])
HTTP_STATUS = {
    "OK": ResponseStatus(code=204, message="OK"),
    "REPLY": ResponseStatus(code=200, message="GET"),
    "NOT_FOUND": ResponseStatus(code=404, message="Not found"),
}
PUT = "PUT"
DELETE = "DELETE"

# SRv6 mapping
OP = {
    "create": "add",
    "remove": "del",
    "destination": "dst",
    "device": "dev",
    "encapmode": "encapmode",
    "segments": "segs",
}
# SSL certificate
CERTIFICATE = "cert_server.pem"


# HTTP utilities class
class HTTPUtils:

    @staticmethod
    def get_srv6_p(http_path):
        # Init steps
        path = {}
        # Get srv6 path
        for k, v in http_path.items():
            # Translating key and saving values
            path[OP[k]] = v
        return path

    @staticmethod
    def get_srv6_ep(request, query):
        # Init steps
        msg = {}
        # Get operation type
        op_type = OP[query["operation"][0]]
        # Let's parse paths
        length = int(request.headers["Content-Length"])
        http_data = request.rfile.read(length)
        http_data = json.loads(http_data)
        # Get paths
        paths = []
        http_paths = http_data["paths"]
        for http_path in http_paths:
            paths.append(HTTPUtils.get_srv6_p(http_path))
        # Finally let's fill the python dict
        msg["operation"] = op_type
        msg["paths"] = paths
        return msg


class HTTPv6Server(HTTPServer):
    address_family = socket.AF_INET6


class SRv6HTTPv6Server(ThreadingMixIn, HTTPv6Server):
    """An HTTP Server that handles each srv6-explicit-path request using a new thread"""

    daemon_threads = True


class SRv6HTTPRequestHandler(BaseHTTPRequestHandler):
    """ "HTTP 1.1 SRv6 request handler"""

    protocol_version = "HTTP/1.1"

    def setup(self):
        self.wbufsize = -1
        self.disable_nagle_algorithm = True
        BaseHTTPRequestHandler.setup(self)

    def send_headers(self, status):
        # Send proper HTTP headers
        self.send_response(status.code, status.message)
        self.end_headers()

    def filter_srv6_paths(self, routes):
        """Filter and format SRv6 paths for JSON serialization."""
        srv6_paths = []
        for route in routes:
            # Filter for SRv6 paths that contain segments
            path_info = {}
            for attr, value in route.get('attrs', []):
                if attr == 'RTA_DST':
                    path_info['destination'] = value
                elif attr == 'RTA_ENCAP':
                    # 确保存在 SRv6 路径信息
                    encap_attrs = value.get('attrs', [])
                    for encap_attr, encap_value in encap_attrs:
                        if encap_attr == 'SEG6_IPTUNNEL_SRH':
                            path_info['segments'] = encap_value.get('segs', [])
            if 'segments' in path_info:  # 确保路径信息完整
                srv6_paths.append(path_info)
        return srv6_paths

    def filter_sids(self, routes):
        """Filter and format SID entries for JSON serialization."""
        sids = []
        for route in routes:
            sid_info = {}
            for attr, value in route.get('attrs', []):
                if attr == 'RTA_DST':
                    sid_info['destination'] = value
                elif attr == 'RTA_ENCAP':
                    # 查找包含 SRv6 本地段（SID）信息的属性
                    encap_attrs = value.get('attrs', [])
                    for encap_attr, encap_value in encap_attrs:
                        if encap_attr == 'SEG6_IPTUNNEL_SRH':
                            sid_info['seglocal'] = encap_value.get('segs', [])
            if 'seglocal' in sid_info:  # 确保 SID 信息完整
                sids.append(sid_info)
        return sids

    def do_POST(self):
        # Extract values from the query string
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)
        # Handle post requests
        if path == SRV6_BASE_PATH:
            srv6_config = HTTPUtils.get_srv6_ep(self, query)

            logger.debug("config received:\n%s", json.dumps(srv6_config, indent=2, sort_keys=True))
            # Let's push the routes
            for path in srv6_config["paths"]:
                ip_route.route(srv6_config["operation"], dst=path['dst'], oif=idxs[path['dev']],
                encap={'type':'seg6', 'mode':path['encapmode'], 'segs':path['segs']})
            # and create the response
            response = ResponseData(status=HTTP_STATUS["OK"])
        else:
            # Unexpected paths
            logger.info("not supported yet")
            response = ResponseData(status=HTTP_STATUS["NOT_FOUND"])
        # Done, send back the respons
        self.send_headers(response.status)
        
    def do_GET(self):
        # Extract values from the query string
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)

        # Handle requests based on path
        if path == "//view-paths":
            # Retrieve SRv6 paths
            try:
                routes = ip_route.get_routes(family=socket.AF_INET)  # Main routing table
                paths = self.filter_srv6_paths(routes)
                print(paths)
                response = ResponseData(status=HTTP_STATUS["REPLY"])
                self.send_response(response.status.code, response.status.message)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(paths, indent=2).encode())
            except Exception as e:
                logger.error(f"Error retrieving SRv6 paths: {e}")
                response = ResponseData(status=HTTP_STATUS["NOT_FOUND"])
                self.send_headers(response.status)

        elif path == "//view-sid":
            # Retrieve SID entries
            try:
                routes = ip_route.get_routes(family=socket.AF_INET6)
                sids = self.filter_sids(routes)
                print(sids)
                response = ResponseData(status=HTTP_STATUS["REPLY"])
                self.send_response(response.status.code, response.status.message)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(sids, indent=2).encode())
            except Exception as e:
                logger.error(f"Error retrieving SID entries: {e}")
                response = ResponseData(status=HTTP_STATUS["NOT_FOUND"])
                self.send_headers(response.status)
                
        else:
            # Path not found
            logger.info("Requested path not supported")
            response = ResponseData(status=HTTP_STATUS["NOT_FOUND"])
            self.send_headers(response.status)



# Start HTTP/HTTPS server
def start_server(secure):
    # Configure Server listener and ip route
    global rest_server, ip_route
    # Setup server
    if rest_server is not None:
        logger.error("HTTP/HTTPS Server is already up and running")
    else:
        rest_server = SRv6HTTPv6Server((REST_IP, REST_PORT), SRv6HTTPRequestHandler)

        # If secure let's protect the socket with ssl
        if secure:
            rest_server.socket = ssl.wrap_socket(
                rest_server.socket, certfile=CERTIFICATE, server_side=True
            )
    # Setup ip route
    if ip_route is not None:
        logger.error("IP Route is already setup")
    else:
        ip_route = IPRoute()
    # Resolve the interfaces
    for interface in interfaces:
        idxs[interface] = ip_route.link_lookup(ifname=interface)[0]
    # Start the loop for REST
    logger.info("Listening %s" % ("HTTPS" if secure else "HTTP"))
    rest_server.serve_forever()


# Parse options
def parse_options():
  global REST_PORT
  parser = OptionParser()
  parser.add_option("-d", "--debug", action="store_true", help="Activate debug logs")
  parser.add_option("-s", "--secure", action="store_true", help="Activate secure mode")
  # Parse input parameters
  (options, args) = parser.parse_args()
  # Setup properly the logger
  if options.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  SERVER_DEBUG = logger.getEffectiveLevel() == logging.DEBUG
  logger.info("SERVER_DEBUG:" + str(SERVER_DEBUG))
  # Return secure/insecure mode
  if options.secure:
    REST_PORT = 443
    return True
  return False

if __name__ == "__main__":
  secure = parse_options()
  start_server(secure)
