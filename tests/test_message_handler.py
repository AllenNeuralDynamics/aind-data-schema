"""Tests hello world printers methods."""

import unittest

import pandas as pd

from hello_world import message_handlers


class MessageHandlerTest(unittest.TestCase):
    """Tests MessageHandler methods."""

    my_msg = "Hello World!!"
    p = message_handlers.MessageHandler(my_msg)

    def test_log_msg(self):
        """Tests that the log_msg method logs a message."""
        with self.assertLogs() as captured:
            self.p.log_msg()

        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), self.my_msg)

    def test_msg_as_df(self):
        """Tests that the message gets returned as a pandas DataFrame."""

        # df from msg with default col_name
        df1 = self.p.msg_as_df()
        # df from msg with non-default col_name
        df2 = self.p.msg_as_df(col_name="non_default")

        # Expected outputs
        expected_df1 = pd.DataFrame.from_dict({"message": [self.my_msg]})
        expected_df2 = pd.DataFrame.from_dict({"non_default": [self.my_msg]})

        self.assertTrue(df1.equals(expected_df1))
        self.assertTrue(df2.equals(expected_df2))
        self.assertTrue(not df1.equals(expected_df2))


if __name__ == "__main__":
    unittest.main()
