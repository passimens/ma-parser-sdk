import unittest
from ma_parser_sdk.examples.int_parser.int_parser import IntParser
from ma_parser_sdk.test_base.any_parser_test import TestAnyParser


class TestIntParser(TestAnyParser):
    """Common behavior for the tests for any specific parser inheriting from BaseParser/XmlBaseParser."""

    # Subclasses should ideally override only the following class variable:
    parser_meta = {
        "parser_class": IntParser,
        "dataset_dir": "data"
        }


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
