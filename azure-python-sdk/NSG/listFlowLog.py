#!/usr/bin/env python
import csv
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from msrestazure.azure_exceptions import CloudError
from msrestazure.tools import parse_resource_id

# ### VARIABLE CONFIGURATIONS ####
file_path = '/tmp/flow_logs.csv'  # should be *.csv
subscription_names = ["az-subscription-name-01"]  # list of strings of the full display name of desired subscriptions
property_names = ["location", "NSG", "la workspace", "storage account", "type"]  # tag key names to include in dump

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
                                                         subscription_id=parse_resource_id(subscription.id).get('subscription'))

            network_watcher_list = None
            while not network_watcher_list:
                # If Azure API gives error (like API limit), wait 10 seconds and try again.
                try:
                    network_watcher_list = network_client.network_watchers.list_all()
                    if not network_watcher_list:
                        break  # if no flow logs found, go to next subscription without retrying.
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            for network_watcher in network_watcher_list:
                flow_log_list = None
                while not flow_log_list:
                    # If Azure API gives error (like API limit), wait 10 seconds and try again.
                    try:
                        flow_log_list = network_client.flow_logs.list(parse_resource_id(network_watcher.id).get('resource_group'), network_watcher.name)
                        if not flow_log_list:
                            break  # if no flow logs found, go to next subscription without retrying.
                    except CloudError as e:
                        print('EXCEPTION {}'.format(e))
                        sleep(10)
                for flowlog in flow_log_list:
                    flowlog_id_dict = parse_resource_id(flowlog.id)
                    flowlog_dict = flowlog.as_dict()
                    csvwriter.writerow([flowlog.name,
                                        subscription.display_name,
                                        flowlog_id_dict.get('resource_group'),
                                        flowlog_dict.get('location'),
                                        parse_resource_id(flowlog_dict.get('flow_analytics_configuration', {}).get('network_watcher_flow_analytics_configuration', {}).get('workspace_resource_id')).get('name'),
                                        parse_resource_id(flowlog_dict.get('storage_id')).get('name'),
                                        parse_resource_id(flowlog_dict.get('target_resource_id')).get('name'),
                                        parse_resource_id(flowlog_dict.get('target_resource_id')).get('resource_group'),
                                        flowlog_dict.get('type')])
