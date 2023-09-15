"""test general functions"""

import unittest

from yaml.scanner import ScannerError

from helpers.general import (
    assign_random_weights,
    try_import_messages,
    try_load_config,
)


class TestGeneral(unittest.TestCase):
    """test general functions"""

    def test_try_load_config(self):
        """test lodading config from fixture"""
        # test valid config.yaml
        self.assertEqual(
            try_load_config("tests/fixtures/valid.yaml"), {"key": "value"}
        )
        # test invalid path
        with self.assertRaises(FileNotFoundError):
            try_load_config("")
        # test invalid yaml
        with self.assertRaises(ScannerError):
            try_load_config("tests/fixtures/invalid.yaml")

    def test_try_import_messages(self):
        """test importing messages from fixture"""
        # test multiple lines
        self.assertEqual(
            try_import_messages("tests/fixtures/multiple.txt"),
            ["a", "b", "c", "d", "e"],
        )
        # test single line
        self.assertEqual(
            try_import_messages("tests/fixtures/single.txt"),
            ["a"],
        )
        # test empty
        self.assertEqual(
            try_import_messages("tests/fixtures/empty.txt"),
            ["suipiss"],
        )
        # test invalid path
        self.assertEqual(
            try_import_messages(""),
            ["suipiss"],
        )
        # test default message
        self.assertEqual(
            try_import_messages("tests/fixtures/empty.txt", "test"),
            ["test"],
        )

    def test_assign_random_weights(self):
        """test assigning random weights"""
        # test multiple items
        self.assertEqual(
            assign_random_weights(["a", "b", "c", "d", "e"]),
            [
                0.5,
                0.125,
                0.125,
                0.125,
                0.125,
            ],
        )
        # test single item
        self.assertEqual(
            assign_random_weights(["a"]),
            [1],
        )
        # test empty
        self.assertEqual(
            assign_random_weights([]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
