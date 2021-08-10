#!/usr/bin/env python
# Script to dump all resource groups in the list of subscriptions along with the tags from the tag_names list.
import csv
from time import sleep
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.locks import ManagementLockClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

# ### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/azure-rg-locks.csv'  # should be *.csv
subscription_names = ["az-subscription-name-01"]  # list of strings of the full display name of desired subscriptions

if __name__ == "__main__":
    print('')  # I like clean breaks
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file=file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Headers
        csvwriter.writerow(["RG NAME", "SUBSCRIPTION", "LOCK NAME"])

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
            lock_client = get_client_from_cli_profile(ManagementLockClient,
                                                               subscription_id=subscription.subscription_id)

            rg_list = None
            while not rg_list:
                # If Azure API gives error (like API limit), wait 10 seconds and try again.
                try:
                    rg_list = resource_client.resource_groups.list()
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)

            sub_lock_list = None
            while not sub_lock_list:
                # If Azure API gives error (like API limit), wait 10 seconds and try again.
                try:
                    sub_lock_list = lock_client.management_locks.list_at_subscription_level()
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            lock_dictionary = dict()
            for lock in sub_lock_list:
                lock_id_parse = parse_resource_id(lock.id)
                lock_dictionary[lock_id_parse.get('name').lower()] = lock.as_dict()

            for rg in rg_list:
                # Dictionary allows for .get() methods wich return NULL if not found.
                rg_dict = rg.as_dict()
                name = rg.name
                csvwriter.writerow([rg.name, subscription.display_name, lock_dictionary.get(rg.name.lower() + '-lock', {}).get('name')])
