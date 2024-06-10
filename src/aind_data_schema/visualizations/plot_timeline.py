""" experimental methods for visualizing subject and procedure timelines """

import json
import os
from datetime import datetime
from typing import List, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def load_metadata_from_folder(folder: str, models: List[str] = None) -> dict:
    """Load metadata from a folder containing JSON files."""

    models = ["subject", "procedures", "session", "acquisition", "processing"] if models is None else models

    # identify what metadata is present
    md = {}
    for k in models:
        path = os.path.join(folder, f"{k}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                md[k] = json.load(f)

    return md


def plot_date_of_birth(ax: plt.Axes, date_of_birth: datetime) -> None:
    """add date of birth marker to the timeline plot"""
    ax.scatter(date_of_birth, [1], marker="o", color="blue", s=100)
    ax.text(date_of_birth, 1.1, "Birth", rotation=90, ha="center", va="bottom")
    ax.text(date_of_birth, 0.9, "Age in days", va="top", ha="right")


def plot_procedures(ax: plt.Axes, procedures: dict, date_of_birth: datetime) -> None:
    """add procedure start and end dates to the timeline plot"""
    for proc in procedures["subject_procedures"]:
        date = datetime.strptime(proc["start_date"], "%Y-%m-%d").date()
        ax.scatter(date, [1], marker="o", color="blue", s=100)
        ax.text(date, 1.1, proc["procedure_type"], rotation=90, ha="center", va="bottom")
        age = (date - date_of_birth).days
        ax.text(date, 0.9, age, ha="center", va="top")

    for proc in procedures["specimen_procedures"]:
        start_date = datetime.strptime(proc["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(proc["end_date"], "%Y-%m-%d")
        ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
        ax.scatter(start_date, [1], marker="|", color="orange", s=120)
        ax.text(start_date, 1.1, proc["procedure_name"], rotation=90, ha="center", va="bottom")


def plot_date_of_acquisition(ax: plt.Axes, date_of_acquisition: datetime, date_of_birth: datetime) -> None:
    """add data of acquisition marker to the timeline plot"""
    ax.scatter(date_of_acquisition, [1], marker="o", color="blue", s=100)
    ax.text(date_of_acquisition, 1.1, "Acquisition", rotation=90, ha="center", va="bottom")

    age = (date_of_acquisition - date_of_birth).days
    ax.text(date_of_acquisition, 0.9, age, ha="center", va="top")


def plot_timeline(
    subject: dict = None,
    procedures: dict = None,
    acquisition: dict = None,
    session: dict = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """Creates a timeline of including date of birth, all subject and specimen procedures, and date of
    data acquisition.

    Args:
        subject (dict): dictionary containing subject metadata
        procedures (dict): dictionary containing procedures metadata
        acquisition (dict): dictionary containing acquisition metadata
        session (dict): dictionary containing session metadata
    """

    fig, ax = plt.subplots(figsize=(10, 5))

    # Date of birth
    if subject:
        date_of_birth = datetime.strptime(subject["date_of_birth"], "%Y-%m-%d").date()
        plot_date_of_birth(ax, date_of_birth)

    # Procedures
    if procedures:
        plot_procedures(ax, procedures, date_of_birth)

    # Date of data acquisition
    da = session or acquisition
    if da:
        acq_start_date = datetime.fromisoformat(da["session_start_time"]).date()
        plot_date_of_acquisition(ax, acq_start_date, date_of_birth)

    # Formatting x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha="right")

    ax.yaxis.set_visible(False)
    plt.tight_layout()

    return fig, ax


if __name__ == "__main__":
    md = load_metadata_from_folder(".")
    plot_timeline(
        subject=md.get("subject"),
        procedures=md.get("procedures"),
        session=md.get("session"),
        acquisition=md.get("acquisition"),
    )
    plt.show()
