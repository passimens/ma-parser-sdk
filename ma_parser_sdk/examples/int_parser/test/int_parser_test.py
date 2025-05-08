import unittest
from ma_parser_sdk.examples.int_parser.int_parser import IntParser
from ma_parser_sdk.test_base.any_parser_test import TestAnyParser


class TestIntParser(TestAnyParser):
    """Common behavior for the tests for any specific parser inheriting from BaseParser/XmlBaseParser."""

    # Subclasses should ideally override only the following class variable:
    parser_meta = {
        "parser_class": IntParser,
        "dataset": {
            # <src_file>: { 'exc': <expected_exception>, 'res': [<expected_items>] }
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            # for invalid <src_file> expected error should be specified in 'exc' field
            "data/int_data_1.txt": {
                "exc": None,
                # "res": ["1", "1", "2", "3", "5", "8", "13", "21", "34"],
                "res": [1, 1, 2, 3, 5, 8, 13, 21, 34],
                },
            "data/str_data_1.txt": {
                "exc": ValueError,
                "res": ["abc", "cde", "efg", "ghi", "ijk", "klm", "mno", "opq", "qrs"],
                },
            },
        }

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
