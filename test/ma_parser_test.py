from any_parser_test import TestAnyParser

from some_parsers.int_str_parser import IntStrParser
from MAIntDescription_class import MAIntDescription
from MAStringDescription_class import MAStringDescription


class TestMAParser(TestAnyParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    # Subclasses should ideally override only the following class variable:
    parser_meta = {
        "parser_class": IntStrParser,
        "dataset": {
            # <src_file>: [(<item_description>, <expected_item>)]
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            "data/test_data_1.txt": [
                (MAIntDescription(), 1),
                (MAIntDescription(), 1),
                (MAIntDescription(), 2),
                (MAIntDescription(), 3),
                (MAIntDescription(), 5),
                (MAIntDescription(), 8),
                (MAIntDescription(), 13),
                (MAIntDescription(), 21),
                (MAIntDescription(), 34),
                ],
            "data/test_data_2.txt": [
                (MAStringDescription(), "abc"),
                (MAStringDescription(), "cde"),
                (MAStringDescription(), "efg"),
                (MAStringDescription(), "ghi"),
                (MAStringDescription(), "ijk"),
                (MAStringDescription(), "klm"),
                (MAStringDescription(), "mno"),
                (MAStringDescription(), "opq"),
                (MAStringDescription(), "qrs"),
                ],
            },
        }
    # In some cases it may be necessary to override _verify_parsed_items method

    def _verify_parsed_items(self) -> None:
        """Validates the parsed items against the expected items."""
        item_num = 0
        for item in self.parsed_items:
            errs = self.parser_meta["dataset"][self.src_file][item_num][0].validate(item)
            self.assertEqual(len(errs), 0)
            self.assertEqual(item, self.parser_meta["dataset"][self.src_file][item_num][1])
            item_num += 1

