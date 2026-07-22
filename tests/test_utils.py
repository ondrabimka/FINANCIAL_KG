import pathlib
import sys
import unittest
import uuid

SRC_DIR = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from utils import setup_custom_logger  # noqa: E402


class TestSetupCustomLogger(unittest.TestCase):
    def test_setup_custom_logger_is_idempotent_for_same_name(self):
        logger_name = f"test_logger_{uuid.uuid4().hex}"

        first_logger = setup_custom_logger(logger_name)
        first_handler_count = len(first_logger.handlers)

        second_logger = setup_custom_logger(logger_name)
        second_handler_count = len(second_logger.handlers)

        self.assertIs(first_logger, second_logger)
        self.assertEqual(first_handler_count, second_handler_count)
        self.assertEqual(second_handler_count, 2)


if __name__ == "__main__":
    unittest.main()
