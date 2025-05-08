from ma_parser_sdk.test_base.ma_parser_test import TestMAParser
from Magritte.visitors.MAEqualityTester_visitor import MAEqualityTester

# parser to test:
from ma_parser_sdk.examples.int_str_parser.int_str_parser import IntStrParser

# Magritte descriptions/accessors:
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor


class TestIntStrParser(TestMAParser):
    """Common behavior for tests for any specific parser inheriting from BaseParser/XmlBaseParser,
    using Magritte descriptions for parsed items validation."""

    # Subclasses should ideally override only the following class variables:
    parser_meta = {
        "parser_class": IntStrParser,
        "equality_tester": MAEqualityTester(),
        "dataset": {
            # <src_file>: { 'exc': <expected_exception>, 'res': [<expected_items>] }
            # any number of <src_file> can be specified, but only one will be used in each test run
            # specific <src_file> can be specified via the PARSER_SRC_FILE environment variable
            # for invalid <src_file> expected error should be specified in 'exc' field
            "data/int_data_1.txt": {
                "exc": None,
                "res": [
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
                },
            "data/str_data_1.txt": {
                "exc": None,
                "res": [
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
                }
            },
        }
