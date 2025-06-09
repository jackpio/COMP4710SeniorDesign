import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

"""
sharePointListRecordUpdate.py
Written By: Jack Piotrowski
Description: Updates records within the provided SharePoint List to reflect the values within the provided csv.
            This scripts objective was to test the capability of updating records that already exist on the
            SharePoint list.
"""

# SharePoint Credentials (DO NOT SHARE)
site_url = "https://tigermailauburn.sharepoint.com/sites/BaseballStatsRaw"
client_id =
client_secret =

# Read in csv records as a dataframe
df = pd.read_csv('API_Test_Addon.csv')

#Authenticate
credentials = ClientCredential(client_id, client_secret)
ctx = ClientContext(site_url).with_credentials(credentials)
#Reference SharePoint List that will be updated
sharepoint_list = ctx.web.lists.get_by_title('API_Test')

#Convert dataframe to dictionary for row by row referencing
data = df.to_dict('records')

#Map the columns in the csv to the columns in the SharePoint List
mapped_data = []
for item in data:
    mapped_item = {
        'Title': item['Name'],
        'field_1': item['Number'],
        'field_2': item['Age']
    }
    mapped_data.append(mapped_item)

#Iterate through each record, query the existing record on SharePoint
#After querying the existing record on SharePoint, update the records contents with the values it has in the new csv
for item in mapped_data:
    title = item['Title']
    query = sharepoint_list.items.filter(f"Title eq '{title}'").get().execute_query()  #retrieving record by primary key
    if query:    #if record exists on SharePoint
        sharepoint_item = query[0]
        for key, value in item.items():  #iterate through each data value in the row
            sharepoint_item.set_property(key, value) #update the corresponding cell in the SharePoint List record
        sharepoint_item.update()
        ctx.execute_query() #apply the update
