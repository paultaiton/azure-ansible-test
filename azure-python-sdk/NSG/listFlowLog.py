#!/usr/bin/env python
import csv
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from msrestazure.azure_exceptions import CloudError

# ### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/flow_logs.csv'  # should be *.csv
subscription_names = ["az-subscription-name-01"]  # list of strings of the full display name of desired subscriptions
property_names = ["display_name"]  # tag key names to include in dump

if __name__ == "__main__":
    print('')  # I like clean breaks
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file=file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Headers
        csvwriter.writerow(["RESOURCE NAME", "SUBSCRIPTION", "RESOURCE GROUP"]
                           + [x.upper() for x in property_names])

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
            network_client = get_client_from_cli_profile(NetworkManagementClient,
                                                         subscription_id=subscription.id)

            flow_log_list = None
            while not flow_log_list:
                # If Azure API gives error (like API limit), wait 10 seconds and try again.
                try:
                    flow_log_list = network_client.flow_logs.list()
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            for flowlog in flow_log_list:
                pass