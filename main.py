import json,requests,os
from kace_api_get_data import KaceApi  # Import the KaceApi class from the Kace_api_get_data module


#initalizing credentials 
Kace_api_username =os.getenv('Kace_api_username')
Kace_api_password =os.getenv('Kace_api_password')

Jira_api_username =os.getenv('Jira_api_username')
Jira_api_password =os.getenv('Jira_api_password')

def get_incorrect_laptops_version(all_laptops):
    # Define a list of correct OS versions as strings
    correct_versions = [
        "Linux Mint 20", "Linux Mint 21", "Ubuntu 20.04", "Ubuntu 22.04",
    ]

    incorrect_laptops = {}  # a new dictionary for saving incorrect versions

    for machine, version in all_laptops.items():
        # Check if there is no correct version that matches the start of the version string
        if not any(version.startswith(correct) for correct in correct_versions):

            # If the version is incorrect, save it to the dictionary
            incorrect_laptops[machine] = version
            

    print(len(all_laptops),'  :All laptops ')
    print(len(incorrect_laptops),'  :Incorrect version laptops')
    return incorrect_laptops  # returning dictionary of incorrect laptops


# Function for creating a Jira task
def create_jira_task(description):
    jira_api_link = "https://jira.infobip.com/rest/api/2/issue"  # Jira API link

    print(f'Logging in to Jira API with username: {Jira_api_username}')

    # Jira task input data
    task_data = {
        "fields": {
            "project": {"key": "ITSD"},
            "components": [{"name": "KACE_Report"}],
            "summary": "KACE SMA non-compliant Linux versions",
            "description": description,
            "labels": [],
            "issuetype": {"name": "SD Troubleshooting"},
            "customfield_13603": "General Troubleshooting"
        }
    }

    # Set up headers for the API request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Authenticate using the `auth` parameter in the request
    auth = (Jira_api_username, Jira_api_password)

    # Convert our input task data to JSON so the API can understand it
    input_data = json.dumps(task_data)

    # Send the POST request to create the Jira task
    response = requests.post(jira_api_link, headers=headers, data=input_data, auth=auth)
    print("Logged in successfully!")
    print("Starting creating the task with given data!")

    # Check the response
    if response.status_code == 201:
        print("Jira task created successfully.")
        jira_response = json.loads(response.text)
        key = jira_response["key"]
        print(f"Jira task key: {key}")
    else:
        print("Failed to create Jira task. HTTP status code:", response.status_code)
        print(response.text)

# Function for generating a task description
def generate_task_description(info_dict, instructions):
    result = f"{instructions}\n||Hostname||Version||Checked||\n"

    for machine, version in info_dict.items():
        result += f"|\"{machine}\"|\"{version}\"|(x)|\n"
    return result  # Returning the result as a string for Jira table and description


# Creating a KaceApi object using credentials
kace_api1 = KaceApi(Kace_api_username,Kace_api_password)
get_laptops_all = kace_api1.get_laptops_all()  # Retrieve all laptops with only Name and OS version

# Get all laptops and extract all the incorrect versions
incorrect_laptops = get_incorrect_laptops_version(get_laptops_all)


# Check if the non_compliant_laptops dictionary is not empty
if len(incorrect_laptops) > 0:
    instructions = "Please review the following hostnames and versions and reinstall the OS to compliant versions"

    # Generate the task description with non_compliant_laptops data
    task_description = generate_task_description(incorrect_laptops, instructions)
    
    # Create a Jira task with the generated description
    create_jira_task(task_description)

    #if there is no non-complaint laptops no ticket will be created 
else:
    print("There are no non-compliant versions of Linux, so no ticket will be created.")