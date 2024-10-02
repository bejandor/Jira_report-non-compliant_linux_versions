# Non-compliant Linux Versions Automated Checkup

**Created by:** Bektemir Myktybek uulu  
**Last modified:** Sep 18, 2023  
**Views:** 20 since Sep 15, 2023  

**Language:** Python  

## Git Repository  
Browse IT Tech Linux / [bek_new_project - Bitbucket](https://ib-ci.com)

## Jenkins Job  
Non-compliant Linux versions checkup [CIS_Linux] - [Jenkins](infobip.local)

## Schedule  
Once a week at 8:55 GMT

## How it Works  
1. Script obtains a list of all laptops with full info from KACE SMA.  
2. Filters the data to keep only Hostname and Version in a Python dictionary.  
3. Extracts non-compliant OS Linux versions and creates a new dictionary.  
4. Creates a Jira task if any laptop has a non-compliant version.  
5. Sends a Slack notification to the #tech_automation channel.
