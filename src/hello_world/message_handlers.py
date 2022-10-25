""" Module to handle printing messages to stdout.
"""

import logging

import pandas as pd


class MessageHandler:
    """
    Class to handle messages.
    """

    def __init__(self, msg):
        """
        Args:
            msg (str): Message to handle.
        """
        self.msg = msg

    def log_msg(self):
        """Simply logs the message."""
        logging.info(self.msg)

    def msg_as_df(self, col_name="message"):
        """Returns message as a dataframe.
        Args:
            col_name (str, optional): Column name for message.
            Defaults to None.

        Returns:
            pandas DataFrame
        """
        return pd.DataFrame.from_dict({col_name: [self.msg]})
