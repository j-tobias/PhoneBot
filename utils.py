import pandas as pd
import json
import glob
import os


# REPORTSPATH = "C:\Users\Justus Tobias\Desktop\PhoneBotDashboard\Reports"
REPORTSPATH = "Reports/"

def getReportPaths()-> list:
    return glob.glob(REPORTSPATH+"/*")

def getReport(name: str):

    path = REPORTSPATH+"/"+name+".json"

    try:
        with open(path, "r") as f:
            report = json.load(f)
            
        return report
    except:
        return False

def updateBasicDF():

    report_paths = getReportPaths()



    BasicDF = pd.read_csv("BasicDF.csv", index_col="Index")

    report_names = BasicDF["ReportName"].to_list()

    for report_path in report_paths:
        report_name = report_path.split(".")[0].split(os.sep)[-1]

        if int(report_name) not in report_names:
            report = getReport(report_name)

            
            # get duration
            duration = report["durationMinutes"]
            # get Date
            date = report["startedAt"]
            date = date[0:-14]
            # get Caller Number
            callernumber = report["customer"]["number"]
            # append new information to df

            new_row = pd.DataFrame({'ReportName': [report_name], 'Date': [date], 'Duration':[duration], 'CallerNumber': [callernumber]})
            BasicDF = pd.concat([BasicDF, new_row], ignore_index=True)


    BasicDF.to_csv("BasicDF.csv",index_label="Index", index=True)

def loadBasicDF()-> pd.DataFrame:

    updateBasicDF()

    return pd.read_csv("BasicDF.csv", index_col="Index")

def computeMetrics(df: pd.DataFrame) -> list:
    """
    Compute various metrics from a call log DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing call logs with columns:
        - Date: date of the call
        - Duration: call duration in minutes
        - CallerNumber: phone number of the caller
    
    Returns:
    list: List containing:
        [0] Number of calls in last week
        [1] Total number of calls
        [2] Average call duration
        [3] Dictionary of calls per unique caller
    """
    try:
        # Convert Date column to datetime if it isn't already
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Get current date from the most recent entry
        most_recent_date = df['Date'].max()
        week_ago = most_recent_date - pd.Timedelta(days=7)
        
        # 1. Number of Calls in Last Week
        calls_last_week = len(df[df['Date'] >= week_ago])
        
        # 2. Number of Calls in Total
        total_calls = len(df)
        
        # 3. Average Call Duration
        avg_duration = df['Duration'].mean()
        
        # 4. Amount of Calls per unique Caller Number
        calls_per_number = df['CallerNumber'].value_counts().to_dict()
        
        return [
            calls_last_week,
            total_calls,
            avg_duration,
            calls_per_number
        ]
        
    except Exception as e:
        print(f"Error computing metrics: {str(e)}")
        return [0, 0, 0.0, {}]
