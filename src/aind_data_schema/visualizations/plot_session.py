import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
import os


def plot_session(datapath):
    """Creates a timeline of events during a session including Data Streams and Stimulus Epochs.

    Args:
        datapath (str): path to folder containing all metadata files
    """

    # identify what metadata is present
    session_path = os.path.join(datapath, "session.json")
    with open(session_path) as json_data:
        d = json.load(json_data)
        json_data.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    for stream in d["data_streams"]:
        stream_start_time = datetime.fromisoformat(stream["stream_start_time"]).replace(tzinfo=None)
        stream_end_time = datetime.fromisoformat(stream["stream_end_time"]).replace(tzinfo=None)
        ax.hlines(
            1, mdates.date2num(stream_start_time), mdates.date2num(stream_end_time), linewidth=8, alpha=0.3, color="r"
        )
    #     ax.scatter(mdates.date2num(stream_start_time), [1], marker='|', color='blue', s=100)

    for epoch in d["stimulus_epochs"]:
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


if __name__ == "__main__":
    plot_session(".")
    plt.show()
