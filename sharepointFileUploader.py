from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.files.file import File

"""
FOR TESTING PURPOSES
sharePointFileUploader.py
Written By: Jack Piotrowski
Description: Uploads "example.txt" to the example_folder on the Baseball Stats Raw SharePoint site
             This was written to test the SharePoint permissions and make sure a file could be
             succesfully uploaded to our site. An XML permission needed to be
             applied to our Azure Active Directory registration in order to allow connection.
"""

# SharePoint Credentials (DO NOT SHARE)
site_url = "https://tigermailauburn.sharepoint.com/sites/BaseballStatsRaw"
client_id =
client_secret =

# Authenticate
ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

#Establish connection to SharePoint site
web = ctx.web
ctx.load(web)
ctx.execute_query()

# Create a file, write content to it
file_name = "example.txt"
file_content = "Hello, SharePoint!"
with open(file_name, "w") as file:
    file.write(file_content)

# Path to the file you want to upload
local_path = "example.txt"
# Target folder on SharePoint, if you look at the url you can find the path going to the chosen folder
# The path is viewable in the browser url box when within the folder on SharePoint
target_folder_url = "/sites/BaseballStatsRaw/Shared Documents/example_folder"

#Read file contents to be uploaded
with open(local_path, "rb") as file:
    file_content = file.read()

#Reference folder that exists on the Baseball Stats Raw SharePoint site
target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
#Upload the file to SharePoint
target_file = target_folder.upload_file(file_name, file_content).execute_query()

print(f"File has been uploaded to {target_file.serverRelativeUrl}")
