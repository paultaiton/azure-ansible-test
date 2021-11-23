#!/usr/bin/env python
# Script to dump all resources in a subscription that have a tag in 'tag_names' that differe from RG level tag.
import csv
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError
from time import sleep

# ### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/azure-resource-different-rg-tags.csv'  # should be *.csv
tag_names = ["costcenter", "appcode"]  # tag key names to include in dump
subscription_names = [
    "az-sub-name-01",
    "az-sub-name-02"
]  # list of strings of the full display name of desired subscriptions

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file=file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["RESOURCE NAME", "RESOURCE GROUP NAME", "SUBSCRIPTION", "TYPE"]
                           + [x.upper() for x in tag_names]
                           + [('RG ' + x.upper()) for x in tag_names])

        # Subscription names are not case sensitive in Azure, but python comparisons are.
        subscription_names = [x.lower() for x in subscription_names]

        subscription_list = None
        while not subscription_list:
            # If Azure API gives error (like API limit), wait 10 seconds and try again.
            try:
                subscription_list = [x for x in subscription_client.subscriptions.list() if x.display_name.lower() in subscription_names]
                if not subscription_list:
                    print('No subscriptions matched filter list "subscription_names".')
                    exit()
            except CloudError as e:
                print('EXCEPTION {}'.format(e))
                sleep(10)

        for subscription in subscription_list:
            resource_client = get_client_from_cli_profile(ResourceManagementClient,
                                                          subscription_id=subscription.subscription_id)
            rg_list = None
            while not rg_list:
                # If Azure API gives error (like API limit), wait 10 seconds and try again.
                try:
                    rg_list = resource_client.resource_groups.list()
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            for rg in rg_list:
                # Dictionary allows for .get() methods wich return NULL if not found.
                rg_dict = rg.as_dict()
                # name = rg.name
                rg_tag_values = [rg_dict.get('tags', {}).get(x) for x in tag_names]

                resource_list = None
                while not resource_list:
                    try:
                        resource_list = resource_client.resources.list_by_resource_group(rg.name)
                    except CloudError as e:
                        print('EXCEPTION {}'.format(e))
                        sleep(10)
                for resource in resource_list:
                    resource_dict = resource.as_dict()
                    tags_differ = False
                    for tag_name in tag_names:
                        tags_differ = tags_differ or (resource_dict.get('tags', {}).get(tag_name) != rg_dict.get('tags', {}).get(tag_name))
                    if tags_differ:
                        resource_tag_values = [resource_dict.get('tags', {}).get(x) for x in tag_names]
                        csvwriter.writerow([resource.name, rg.name, subscription.display_name, resource.type] + resource_tag_values + rg_tag_values)
