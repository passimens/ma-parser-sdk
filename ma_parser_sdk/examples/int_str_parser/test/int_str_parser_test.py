from ma_parser_sdk.test_base.ma_parser_test import TestMAParser
from Magritte.visitors.MAEqualityTester_visitor import MAEqualityTester

# parser to test:
from ma_parser_sdk.examples.int_str_parser.int_str_parser import IntStrParser


class TestIntStrParser(TestMAParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    # Subclasses should ideally override only the following class variables:
    parser_meta = {
        "parser_class": IntStrParser,
        "equality_tester": MAEqualityTester(),
        "dataset_dir": "data",
        }
