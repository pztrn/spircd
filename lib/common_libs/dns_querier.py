from dns import resolver
from dns import reversename

from lib.common_libs.library import Library

"""@package dns_querier
Contains class that used for getting client's PTR record, if it
exists.
"""

class Dns_querier(Library):
    """
    This class responsible for all DNS queries spircd might execute.
    """

    def __init__(self):
        Library.__init__(self)

    def get_ptr(self, ip):
        """
        This method responsible for getting PTR record for passed IP
        address.
        """
        ip_to_query = reversename.from_address(ip)

        self.log(2, "Getting PTR record for ip {ip}", {"ip": ip_to_query})

        try:
            ptr = resolver.query(ip, "PTR")[0]
            self.log(2, "PTR found: {ptr}", {"ptr": ptr})
            return ptr
        except resolver.NXDOMAIN:
            self.log(2, "Can't find PTR for {ip}", {"ip": ip})
            return None
