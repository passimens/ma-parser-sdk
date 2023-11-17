from test_base.ma_parser_test import TestMAParser
from visitors.MAEqualityTester_visitor import MAEqualityTester
from error import FormatError

# parser to test:
from host_port_parser.host_port_parser import HostPortParser
# models to validate parsed items against:
from model_for_tests.Host import Host
from model_for_tests.Port import Port
# Magritte descriptions/accessors:
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAContainer_class import MAContainer
from descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from accessors.MAAttrAccessor_class import MAAttrAccessor


class TestHostPortParser(TestMAParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    # Subclasses should ideally override only the following class variables:

    # Descriptions of parsed items
    host_desc = MAContainer()
    port_desc = MAContainer()
    host_desc.setChildren(
        [
            MAStringDescription(name="ip", accessor=MAAttrAccessor("ip")),
            MAToManyRelationDescription(name="ports", accessor=MAAttrAccessor("ports"), reference=port_desc),
            ]
        )
    port_desc.setChildren(
        [
            MAToOneRelationDescription(name="host", accessor=MAAttrAccessor("host"), reference=host_desc),
            MAIntDescription(name="numofport", accessor=MAAttrAccessor("numofport")),
            ]
        )

    # Parsed items expected models
    host1 = Host("1.2.3.4", [])
    host2 = Host("2.3.4.5", [])
    host3 = Host("9.8.7.6", [])
    host1.ports = [Port(host1, 10), Port(host1, 22), Port(host1, 80)]
    host2.ports = [Port(host2, 123), Port(host2, 443)]
    host3.ports = [Port(host3, 8080)]

    parser_meta = {
        "parser_class": HostPortParser,
        "equality_tester": MAEqualityTester(),
        "dataset": {
            # <src_file>: { 'exc': <expected_exception>, 'res': [<expected_items>] }
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            # for invalid <src_file> expected error should be specified in 'exc' field
            "data/host_port_ok.txt": {
                "exc": None,
                "res": [
                    (host_desc, host1),
                    (port_desc, host1.ports[0]),
                    (port_desc, host1.ports[1]),
                    (port_desc, host1.ports[2]),
                    (host_desc, host2),
                    (port_desc, host2.ports[0]),
                    (port_desc, host2.ports[1]),
                    (host_desc, host3),
                    (port_desc, host3.ports[0]),
                    ],
                },
            "data/host_port_invalid.txt": {
                "exc": FormatError,
                "res": [],
                },
            "data/host_port_empty.txt": {
                "exc": None,
                "res": [],
                },
            },
        }
