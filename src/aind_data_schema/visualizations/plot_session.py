""" experimental methods for visualizing data streams and stimulus epochs in a session """

from datetime import datetime
from typing import Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from aind_data_schema.visualizations.plot_timeline import load_metadata_from_folder


def plot_session(session: dict) -> Tuple[plt.Figure, plt.Axes]:
    """Creates a timeline of events during a session including Data Streams and Stimulus Epochs.

    Args:
        session (dict): dictionary containing session metadata
    """

    fig, ax = plt.subplots(figsize=(10, 5))
    for stream in session["data_streams"]:
        stream_start_time = datetime.fromisoformat(stream["stream_start_time"]).replace(tzinfo=None)
        stream_end_time = datetime.fromisoformat(stream["stream_end_time"]).replace(tzinfo=None)
        ax.hlines(
            1, mdates.date2num(stream_start_time), mdates.date2num(stream_end_time), linewidth=8, alpha=0.3, color="r"
        )
    #     ax.scatter(mdates.date2num(stream_start_time), [1], marker='|', color='blue', s=100)

    for epoch in session["stimulus_epochs"]:
        stimulus_start_time = datetime.fromisoformat(epoch["stimulus_start_time"]).replace(tzinfo=None)
        stimulus_end_time = datetime.fromisoformat(epoch["stimulus_end_time"]).replace(tzinfo=None)
        ax.hlines(2, mdates.date2num(stimulus_start_time), mdates.date2num(stimulus_end_time), linewidth=8, alpha=0.3)
        #     ax.scatter(mdates.date2num(stimulus_start_time), [2], marker='|', color='red', s=100)
        ax.text(stimulus_start_time, 2.1, epoch["stimulus_name"], rotation=90, ha="center", va="bottom")

    ax.xaxis.set_major_locator(mdates.HourLocator())
    loc = mdates.MinuteLocator(byminute=[0, 15, 30, 45])
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))
    ax.set_yticks([1, 2])
    ax.set_yticklabels(["Streams", "Stimuli"])

    plt.tight_layout()

    return fig, ax


if __name__ == "__main__":
    md = load_metadata_from_folder(".")
    plot_session(md["session"])
    plt.show()
