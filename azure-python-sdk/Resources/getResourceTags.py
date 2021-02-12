#!/usr/bin/env python
# Script to dump all resource groups in the list of subscriptions along with the tags from the tag_names list.
import csv
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

# ### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/azure-resource-tags.csv'  # should be *.csv
subscription_names = ["subscription-name-example"]  # list of strings of the full display name of desired subscriptions
tag_names = ["costcenter", "environment", "portfolio", "appcode", "appname", "drtier", "snet", "servicerole"]  # tag key names to include in dump

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file=file_path, mode='w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Headers.
        csvwriter.writerow(["NAME", "SUBSCRIPTION", "GROUP", "TYPE"] + tag_names)

        subscription_list = None

        while not subscription_list:
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
                try:
                    rg_list = resource_client.resource_groups.list()
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            for rg in rg_list:
                # Dictionary allows for .get() methods wich return NULL if not found.
                rg_dict = rg.as_dict()
                name = rg.name
                rg_tag_values = [rg_dict.get('tags', {}).get(x) for x in tag_names]
                csvwriter.writerow([rg.name, subscription.display_name, rg.name, rg.type] + rg_tag_values)

                resource_list = None
                while not resource_list:
                    try:
                        resource_list = resource_client.resources.list_by_resource_group(rg.name)
                    except CloudError as e:
                        print('EXCEPTION {}'.format(e))
                        sleep(10)
                for resource in resource_list:
                    resource_dict = resource.as_dict()
                    resource_tag_values = [resource_dict.get('tags', {}).get(x) for x in tag_names]
                    csvwriter.writerow([resource.name, subscription.display_name, rg.name, resource.type] + resource_tag_values)
