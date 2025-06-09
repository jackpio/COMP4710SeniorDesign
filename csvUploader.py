import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

"""
csvUploader.py
Written By: Jack Piotrowski
Description: Uploads a single csv to a specified SharePoint list. This specfic file is a test version that tests the ability to
            upload new records to a SharePoint List within the Baseball Stats Raw site. Production version of this file with
            correct column mapping is perGameListAPIRecordUploader.py
"""

# SharePoint Credentials (DO NOT SHARE)
site_url = "https://tigermailauburn.sharepoint.com/sites/BaseballStatsRaw"
client_id =
client_secret =

#Read csv into a pandas dataframe for row by row processing
df = pd.read_csv('API_Test_Addon.csv')

#Authentication
credentials = ClientCredential(client_id, client_secret)
ctx = ClientContext(site_url).with_credentials(credentials)
#Reference sharepoint list that will be added to
sharepoint_list = ctx.web.lists.get_by_title('API_Test')  #Replace with the SharePoint List you are trying to upload records to

#Convert dataframe to dictionary, each entry in the dictionary is a row of data in the csv
data = df.to_dict('records')

#Map the columns of the csv to the columns of the SharePoint List
mapped_data = []
for item in data:
    mapped_item = {
        'Title': item['Name'],
        'field_1': item['Number'],
        'field_2': item['Age']
    }
    mapped_data.append(mapped_item)

#Upload every record/row to SharePoint
for item in mapped_data:
    sharepoint_list.add_item(item)
    ctx.execute_query()

