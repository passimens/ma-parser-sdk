from ma_parser_sdk.test_base.ma_parser_test import TestMAParser
from Magritte.visitors.MAEqualityTester_visitor import MAEqualityTester
from parser_api.error import FormatError

# parser to test:
from ma_parser_sdk.examples.host_port_parser.host_port_parser import HostPortParser
# models to validate parsed items against:
from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
# Magritte descriptions/accessors:
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor


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
    host1 = Host()
    host2 = Host()
    host3 = Host()
    host1.ip = "1.2.3.4"
    host2.ip = "2.3.4.5"
    host3.ip = "9.8.7.6"
    port1_10 = Port()
    port1_22 = Port()
    port1_80 = Port()
    port1_10.host = host1
    port1_10.numofport = 10
    port1_22.host = host1
    port1_22.numofport = 22
    port1_80.host = host1
    port1_80.numofport = 80
    port2_123 = Port()
    port2_443 = Port()
    port2_123.host = host2
    port2_123.numofport = 123
    port2_443.host = host2
    port2_443.numofport = 443
    port3_8080 = Port()
    port3_8080.host = host3
    port3_8080.numofport = 8080

    host1.ports = [port1_10, port1_22, port1_80]
    host2.ports = [port2_123, port2_443]
    host3.ports = [port3_8080]

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
