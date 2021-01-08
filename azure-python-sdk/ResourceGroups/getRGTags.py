#!/usr/bin/env python
# Script to dump all resource groups in the list of subscriptions along with the tags from the tag_names list.
import csv
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

#### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/azure-rg-tags.csv'  # should be *.csv
subscription_names = ["az-sub-name-01", "az-sub-name-02"]  # list of strings of the full display name of desired subscriptions
tag_names = ["costcenter", "environment", "portfolio", "appcode", "appname", "drtier"]  # tag key names to include in dump

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file=file_path, mode='w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Headers.
        csvwriter.writerow(["NAME", "SUBSCRIPTION"] + tag_names)

        for subscription in subscription_client.subscriptions.list():
            if subscription.display_name in subscription_names:
                resource_client = get_client_from_cli_profile(ResourceManagementClient,
                                                              subscription_id=subscription.subscription_id)

                rg_list = resource_client.resource_groups.list()
                for rg in rg_list:
                    # Dictionary allows for .get() methods wich return NULL if not found.
                    rg_dict = rg.as_dict()
                    name = rg.name
                    tag_values = [rg_dict.get('tags', {}).get(x) for x in tag_names]

                    csvwriter.writerow([rg.name, subscription.display_name] + tag_values)
