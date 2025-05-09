import inspect
import logging
from ma_parser_sdk.test_base.any_parser_test import TestAnyParser
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.visitors.MAJson_visitors import MAObjectJsonWriter, MAValueJsonWriter

logger = logging.getLogger(__name__)


class TestMAParser(TestAnyParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    # Subclasses should ideally only define the following class variables, e.g.:

    '''
    # Descriptions of parsed items
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
    '''
    object_writer = MAObjectJsonWriter()
    value_writer = MAValueJsonWriter()
    # In some cases it may be necessary to override _verify_parsed_items method

    def _verify_parsed_items(self) -> None:
        """Validates the parsed items against the expected items."""
        logger.info("Verifying parsed items...")
        self.assertEqual(len(self.parsed_items), len(self.expected_data), "Number of parsed items doesn't match")
        item_num = 0
        for parsed_item in self.parsed_items:
            expected_desc = self.expected_data[item_num][0]
            expected_item = self.expected_data[item_num][1]
            logger.debug(
                f"Validating parsed item #{item_num} ({list(filter(lambda x: not x[0].startswith('__'), inspect.getmembers(parsed_item)))}) "
                f"against the expected item ({list(filter(lambda x: not x[0].startswith('__'), inspect.getmembers(expected_item)))})"
                )
            errs = expected_desc.validate(parsed_item)
            self.assertEqual(len(errs), 0, f"Item #{item_num} ({parsed_item!r}) validation failed: {errs}")
            if isinstance(expected_desc, MAContainer):
                try:
                    parsed_str = self.object_writer.write_json(parsed_item, expected_desc)
                except RecursionError:
                    parsed_str = f"{parsed_item!r}(has cyclic references)"
            else:
                parsed_str = self.value_writer.write_json(parsed_item, expected_desc)
            if isinstance(expected_desc, MAContainer):
                try:
                    expected_str = self.object_writer.write_json(expected_item, expected_desc)
                except RecursionError:
                    expected_str = f"{expected_item!r}(has cyclic references)"
            else:
                expected_str = self.value_writer.write_json(expected_item, expected_desc)
            logger.debug(f"Comparing parsed item #{item_num} ({parsed_str}) with the expected item ({expected_str})")
            self.assertTrue(
                self.parser_meta["equality_tester"].equal(
                    parsed_item,
                    expected_item,
                    expected_desc,
                    ),
                f"Parsed item #{item_num} ({parsed_str}) is not equal to the expected item ({expected_str})",
                )
            item_num += 1
