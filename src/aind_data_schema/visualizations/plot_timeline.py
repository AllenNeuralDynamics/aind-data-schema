import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime
import json
import os



def plot_date_of_birth(date_of_birth, ax):
    ax.scatter(date_of_birth, [1], marker="o", color="blue", s=100)
    ax.text(date_of_birth, 1.1, "Birth", rotation=90, ha="center", va="bottom")
    ax.text(date_of_birth, 0.9, "Age in days", va="top", ha="right")


def plot_procedures(procedures, date_of_birth, ax):
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


def plot_date_of_acquisition(date_of_acquisition, date_of_birth, ax):
    ax.scatter(date_of_acquisition, [1], marker="o", color="blue", s=100)
    ax.text(date_of_acquisition, 1.1, "Acquisition", rotation=90, ha="center", va="bottom")

    age = (date_of_acquisition - date_of_birth).days
    ax.text(date_of_acquisition, 0.9, age, ha="center", va="top")


def plot_processing(processing, start_date, end_date, ax):
    for proc in processing["processing_pipeline"]["data_processes"]:
        ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
        ax.scatter(start_date, [1], marker="|", color="red", s=120)
        ax.text(start_date, 1.1, proc["name"], rotation=90, ha="center", va="bottom")
    for proc in processing["processing_pipeline"]["data_processes"]:
        ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
        ax.scatter(start_date, [1], marker="|", color="red", s=120)
        ax.text(start_date, 1.1, proc["name"], rotation=90, ha="center", va="bottom")


def plot_timeline(datapath, savepath, processing_flag=False):
    """Creates a timeline of including date of birth, all subject and specimen procedures, and date of
    data acquisition. Optionally can include data processing as well.

    Args:
        datapath (str): path to folder containing all metadata files
        savepath (str): path to location to save figure
        processing_flag (Bool): Making this True adds the processing dates to the timeline. Defaults to False.
    """

    # identify what metadata is present
    md = {}
    for k in ["subject", "procedures", "session", "acquisition", "processing"]:
        path = os.path.join(datapath, f"{k}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                md[k] = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Date of birth
    if "subject" in md:
        date_of_birth = datetime.strptime(md["subject"]["date_of_birth"], "%Y-%m-%d").date()
        plot_date_of_birth(date_of_birth, ax)

    # Procedures
    if "procedures" in md:
        plot_procedures(md["procedures"], date_of_birth, ax)

    # Date of data acquisition    
    da = md.get("session", md.get("acquisition", None))    
    if da:
        
        acq_start_date = datetime.fromisoformat(da["session_start_time"]).date()
        acq_end_date = datetime.fromisoformat(da["session_end_time"]).date()
        plot_date_of_acquisition(acq_start_date, date_of_birth, ax)
        
        if processing_flag and "processing" in md:
            plot_processing(md["processing"], acq_start_date, acq_end_date, ax)

    # Formatting x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha="right")

    ax.yaxis.set_visible(False)
    plt.tight_layout()
    plt.savefig(savepath)
    plt.show()

if __name__ == "__main__":
    plot_timeline('.','.',True)