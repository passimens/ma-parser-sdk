from MAToOneRelationDescription_class import MAToOneRelationDescription
from any_parser_test import TestAnyParser
from MAEqualityTester_visitor import MAEqualityTester

#from some_parsers.int_str_parser import IntStrParser
from some_parsers.host_port_parser import HostPortParser
from MAIntDescription_class import MAIntDescription
from MAStringDescription_class import MAStringDescription
from accessors.MAIdentityAccessor_class import MAIdentityAccessor
from model_for_tests.Host import Host
from model_for_tests.Port import Port
from MAContainer_class import MAContainer
from MAToManyRelationDescription_class import MAToManyRelationDescription
from accessors.MAAttrAccessor_class import MAAttrAccessor


class TestMAParser(TestAnyParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    host_desc = MAContainer()
    port_desc = MAContainer()
    host_desc.setChildren([
        MAStringDescription(name="ip", accessor=MAAttrAccessor("ip")),
        MAToManyRelationDescription(name="ports", accessor=MAAttrAccessor("ports"), reference=port_desc),
        ])
    port_desc.setChildren([
        MAToOneRelationDescription(name="host", accessor=MAAttrAccessor("host"), reference=host_desc),
        MAIntDescription(name="numofport", accessor=MAAttrAccessor("numofport")),
        ])

    host1 = Host("1.2.3.4", [])
    host2 = Host("2.3.4.5", [])
    host3 = Host("9.8.7.6", [])
    host1.ports = [Port(host1, 10), Port(host1, 22), Port(host1, 80)]
    host2.ports = [Port(host2, 123), Port(host2, 443)]
    host3.ports = [Port(host3, 8080)]

    # Subclasses should ideally override only the following class variable:
    parser_meta = {
        "parser_class": HostPortParser,
        "equality_tester": MAEqualityTester(),
        "dataset": {
            # <src_file>: [(<item_description>, <expected_item>)]
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            "data/test_data_3.txt": [
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
            "data/test_data_1.txt": [
                (MAIntDescription(accessor=MAIdentityAccessor()), 1),
                (MAIntDescription(accessor=MAIdentityAccessor()), 1),
                (MAIntDescription(accessor=MAIdentityAccessor()), 2),
                (MAIntDescription(accessor=MAIdentityAccessor()), 3),
                (MAIntDescription(accessor=MAIdentityAccessor()), 5),
                (MAIntDescription(accessor=MAIdentityAccessor()), 8),
                (MAIntDescription(accessor=MAIdentityAccessor()), 13),
                (MAIntDescription(accessor=MAIdentityAccessor()), 21),
                (MAIntDescription(accessor=MAIdentityAccessor()), 34),
                ],
            "data/test_data_2.txt": [
                (MAStringDescription(accessor=MAIdentityAccessor()), "abc"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "cde"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "efg"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "ghi"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "ijk"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "klm"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "mno"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "opq"),
                (MAStringDescription(accessor=MAIdentityAccessor()), "qrs"),
                ],
            },
        }
    # In some cases it may be necessary to override _verify_parsed_items method

    def _verify_parsed_items(self) -> None:
        """Validates the parsed items against the expected items."""
        item_num = 0
        for item in self.parsed_items:
            errs = self.parser_meta["dataset"][self.src_file][item_num][0].validate(item)
            self.assertEqual(len(errs), 0, f"Item #{item_num} ({item!r}) validation failed: {errs}")
            self.assertTrue(
                self.parser_meta["equality_tester"].equal(
                    item,
                    self.parser_meta["dataset"][self.src_file][item_num][1],
                    self.parser_meta["dataset"][self.src_file][item_num][0],
                    ),
                f"Item #{item_num} ({item!r}) is not equal to the expected item "
                f"({self.parser_meta['dataset'][self.src_file][item_num][1]!r})",
                )
            item_num += 1

