import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime
import json

def plot_timeline(datapath, savepath, processing_flag=False):
    """Creates a timeline of including date of birth, all subject and specimen procedures, and date of
    data acquisition. Optionally can include data processing as well.

    Args:
        datapath (str): path to folder containing all metadata files
        savepath (str): path to location to save figure
        processing_flag (Bool): Making this True adds the processing dates to the timeline. Defaults to False.
    """

    # identify what metadata is present
    session_flag = False
    acquisition_flag = False
    for f in os.listdir(datapath):
        if f.endswith('subject.json'):
            subject_path = os.path.join(datapath, f)
        if f.endswith('procedures.json'):
            procedures_path = os.path.join(datapath, f)
        if f.endswith('session.json'):
            session_path = os.path.join(datapath, f)
            session_flag = True
        if f.endswith('acquisition.json'):
            acquisition_path = os.path.join(datapath, f)
            acquisition_flag = True
        if f.endswith('processing.json'):
            processing_path = os.path.join(datapath, f)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Date of birth
    with open(subject_path) as json_data:
        d = json.load(json_data)
        json_data.close()
    date_of_birth = datetime.strptime(d['date_of_birth'], "%Y-%m-%d").date()
    ax.scatter(date_of_birth, [1], marker='o', color='blue', s=100)
    ax.text(date_of_birth, 1.1, "Birth", rotation=90, ha='center', va='bottom')

    # Procedures
    try:
        with open(procedures_path) as json_data:
            d = json.load(json_data)
            json_data.close()

        # Add each procedure:
        for proc in d['subject_procedures']:
            date = datetime.strptime(proc["start_date"], "%Y-%m-%d").date()
            ax.scatter(date, [1], marker='o', color='blue', s=100)
            ax.text(date, 1.1, proc['procedure_type'], rotation=90, ha='center', va='bottom')
            age = (date-date_of_birth).days
            ax.text(date, 0.9, age, ha='center', va='top')

        for proc in d['specimen_procedures']:
            start_date = datetime.strptime(proc["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(proc["end_date"], "%Y-%m-%d")
            ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
            ax.scatter(start_date, [1], marker='|', color='orange', s=120)
            ax.text(start_date, 1.1, proc["procedure_name"], rotation=90, ha='center', va='bottom')
    except:
        print("Incomplete procedures")

    # Date of data acquisition
    if session_flag:
        with open(session_path) as json_data:
            da = json.load(json_data)
            json_data.close()
    elif acquisition_flag:
        with open(acquisition_path) as json_data:
            da = json.load(json_data)
            json_data.close()
    try:
        date_of_acquisition = datetime.fromisoformat(da['session_start_time']).date()
        ax.scatter(date_of_acquisition, [1], marker='o', color='blue', s=100)
        ax.text(date_of_acquisition, 1.1, "Acquisition", rotation=90, ha='center', va='bottom')
        if session_flag:
            age = (date_of_acquisition-date_of_birth).days
            ax.text(date_of_acquisition, 0.9, age, ha='center', va='top')
    except:
        print("No acquisition date")

    if processing_flag:
        with open(processing_path) as json_data:
            d = json.load(json_data)
            json_data.close()
        for proc in d['processing_pipeline']['data_processes']:
            start_date = datetime.fromisoformat(da['session_start_time']).date()
            end_date = datetime.fromisoformat(da['session_end_time']).date()
            ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
            ax.scatter(start_date, [1], marker='|', color='red', s=120)
            ax.text(start_date, 1.1, proc["name"], rotation=90, ha='center', va='bottom')
        for proc in d['processing_pipeline']['data_processes']:
            start_date = datetime.fromisoformat(da['session_start_time']).date()
            end_date = datetime.fromisoformat(da['session_end_time']).date()
            ax.hlines(1, start_date, end_date, linewidth=8, alpha=0.3)
            ax.scatter(start_date, [1], marker='|', color='red', s=120)
            ax.text(start_date, 1.1, proc["name"], rotation=90, ha='center', va='bottom')

    # Formatting x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha='right') 

    ax.text(date_of_birth, 0.9, "Age in days", va='top', ha='right')

    ax.yaxis.set_visible(False)
    plt.tight_layout()
    plt.savefig(savepath)
    plt.show()
