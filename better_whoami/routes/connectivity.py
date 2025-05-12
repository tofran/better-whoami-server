import logging
import socket
from dataclasses import dataclass

import dns.resolver
from litestar import get
from litestar.exceptions import ValidationException


@dataclass
class Connectivity:
    has_external_connectivity: bool
    external_ip_address: str | None


@get(
    "/connectivity",
    name="check_connectivity",
    description="Check the connectivity of the service to the outside world.",
    sync_to_thread=False,
)
def check_connectivity(resolve_timeout: int = 3) -> Connectivity:
    if resolve_timeout <= 0 or resolve_timeout > 10:  # noqa: PLR2004
        raise ValidationException("Timeout must be greater than 0 and less or equal to 10 seconds")

    has_external_connectivity = True
    external_ip_address = None

    try:
        logging.info("Checking external connectivity via socket to 8.8.8.8:53")
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=resolve_timeout,
        )
        has_external_connectivity = True
    except OSError:
        return Connectivity(
            has_external_connectivity=False,
            external_ip_address=None,
        )

    resolver = dns.resolver.Resolver()
    resolver.timeout = resolve_timeout

    try:
        logging.info("Resolving ns1.google.com")
        ns_answers = resolver.resolve(
            "ns1.google.com",
            "A",
        )

        if ns_answers:
            resolver.nameservers = [str(ns_answers[0])]
            logging.info("Retrieving ip from o-o.myaddr.l.google.com")
            answers = resolver.resolve("o-o.myaddr.l.google.com", "TXT")
            if answers:
                external_ip_address = str(answers[0]).strip('"')

    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        logging.exception("Failed to get external IP")

    return Connectivity(
        has_external_connectivity=has_external_connectivity,
        external_ip_address=external_ip_address,
    )
