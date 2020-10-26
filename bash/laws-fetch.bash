#!/usr/bin/bash
# copyright 2020 Paul Aiton (@paultaiton)
# requires the azure cli to be installed and user to be logged in.

# Will loop through all subscriptions for an account, listing all 
# log analytics workspaces while printing in YAML format a list of dictionaries
# for each subscription + location pair with the guid, fqid, and primary shared key.

for subscription in $( az account list | jq -r '.[].name' )
do
    echo "${subscription}:" 
    for laws in $(az monitor log-analytics workspace list --subscription $subscription | jq -c '.[] | { location, name, resourceGroup, customerId, id }' | egrep "esla-.*-(non|)prod-log-laws-0" | sed 's/west us/westus/') 
        do 
                echo "  $(echo $laws | jq -r '.location'):" 
                echo "    workspace_guid: $(echo $laws | jq -r '.customerId')" 
                echo "    workspace_fqid: $(echo $laws | jq -r '.id')" 
                echo "    workspace_key: $(az monitor log-analytics workspace get-shared-keys --subscription $subscription --resource-group $( echo $laws | jq -r '.resourceGroup') --workspace-name $( echo $laws | jq -r '.name') | jq -r '.primarySharedKey' )" 
    done 
done 