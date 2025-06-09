# Import Module
from ftplib import FTP_TLS
from datetime import datetime, timedelta
import os
import time

"""
ftpDownload.py
Written By: Jack Piotrowski
Description: Downloads all files uploaded to the FTP server in the last week. Also provides methods for testing ftp connection
            and single file download.
"""


#function to test the ftp connection

def check_ftp_connection(server, username, password):
    try:
        # Open connection to the FTP server using TLS
        ftp = FTP_TLS(server)
        ftp.login(username, password)
        ftp.prot_p()
        print("Connection established successfully.")

        # Close the connection
        ftp.quit()
        print("Connection closed.")
    except Exception as e:
        print(f"Failed to connect: {e}")

#function to test the download of one file off the Trackman FTP server

def download_file(server, username, password):
    try:
        # Open connection to the FTP server using TLS
        ftp = FTP_TLS(server)
        ftp.login(username, password)
        ftp.prot_p()
        print("Secure connection established successfully.")
    except Exception as e:
        print(f"Failed to connect: {e}")

    #ftp.dir()
    ftp.cwd("/v3/2025/04/19/CSV")  #Provide a directory to switch to
    #ftp.dir()

    local_filename = "test/20250419-Texas-1_unverified.csv"  #local file
    filename = "20250419-Texas-1_unverified.csv"   #file on ftp server

    # Download file
    with open(local_filename, 'wb') as local_file:
        ftp.retrbinary(f'RETR {filename}', local_file.write)
    print(f"File '{filename}' downloaded successfully as '{local_filename}'.")

    #Close ftp connection
    ftp.quit()
    print("Connection closed.")

#Downloads the last week's worth of files
#Designed to run in a VM scheduled job
#The results of this download should be fed into our playerStatsConverter.py to generate the individual game statistics

def download_new_files(server, username, password):

    #Form the directory path using the current date
    directory = ""
    current_date = datetime.now()
    #current_date = datetime(2025, 4, 24) #Testing purposes

    downloaded_file_directory = os.path.join("downloadedFiles", str(current_date.date())) #create directory name for downloaded files
    print(downloaded_file_directory)

    #check if the directory exists locally, if not, it will create it
    if not os.path.exists(downloaded_file_directory) or not os.path.isdir(downloaded_file_directory):
        os.makedirs(downloaded_file_directory)
    folder_date = current_date - timedelta(days=6)  #folder_date starts 6 days before current date to get all new data uploaded in last week

    #For loop to iterate through each directory of the last week
    #Establishes connection for each directory to ensure connection does not timeout during download
    #Downloads all csvs files from the last week and puts them in a folder named MM-DD-YYYY
    #MM-DD-YYYY corresponds to the day of the download
    for i in range(7):
        try:
            # Open connection to the FTP server
            ftp = FTP_TLS(server)
            ftp.login(username, password)
            ftp.prot_p()
            print("Secure connection established successfully.")
        except Exception as e:
            print(f"Failed to connect: {e}")

        #Store date information for directory path formation
        year_numeric = folder_date.year
        month_numeric = folder_date.month
        month_numeric_string = folder_date.month
        if month_numeric < 10:
            month_numeric_string = "0" + str(month_numeric)
        day_numeric = folder_date.day
        day_numeric_string = folder_date.day
        if day_numeric < 10:
            day_numeric_string = "0" + str(day_numeric)

        #print(f"Year (numeric): {year_numeric}")
        #print(f"Month (numeric): {month_numeric}")
        #print(f"Month (string): {month_numeric_string}")
        #print(f"Day (numeric): {day_numeric}")

        #Formulate the directory and change to that directory
        #First iterate gets the data files from 6 days ago, last iteration pulls csvs from current day
        directory = "/v3/{}/{}/{}/CSV".format(year_numeric,month_numeric_string,day_numeric_string)
        print(directory)
        ftp.cwd(directory)


        files = ftp.nlst()    #get all files in the directory
        print(f"Files in directory '{directory}': {files}")

        #For each file, check if it is a .csv and is game stats (exclude playerpositioning)
        #Download each file into the MM-DD-YYYY directory
        for file in files:
            if file.endswith('.csv') and '_playerpositioning' not in file:
                local_filename = os.path.join(downloaded_file_directory, file)
                with open(local_filename, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {file}', local_file.write)
                print(f"File '{file}' downloaded successfully as '{local_filename}'.")
                time.sleep(0.1)  #ensure we do not overload ftp server with requests

        ftp.quit()  #close the connection before moving to the next directory
        print("Connection closed.")


        folder_date += timedelta(days=1)  #increment folder_date to move to the next day
        time.sleep(10.0) #sleep to give time between disconnection and reconnection to ftp server


def main():
    # Server Information
    # Provided by Everett Teaford, also in documentation
    HOSTNAME = "ftp.trackmanbaseball.com"
    USERNAME =
    PASSWORD =

    #check_ftp_connection(HOSTNAME, USERNAME, PASSWORD)
    #download_file(HOSTNAME, USERNAME, PASSWORD)
    download_new_files(HOSTNAME, USERNAME, PASSWORD)

if __name__ == "__main__":
    main()
