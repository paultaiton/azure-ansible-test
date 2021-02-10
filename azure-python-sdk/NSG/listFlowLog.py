#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient

subscription_names = [""]
subscription_names = [x.lower() for x in subscription_names]

if __name__ == "__main__":
    print('')
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    # subscription_list = [subscription_client.subscriptions.get(subscription_id='')]
    subscription_list = subscription_client.subscriptions.list()
    # subscription_list = subscription_client.subscriptions.list_locations()
    # subscription_listraw = list(subscription_client.subscriptions.list())
    for subscription in [subscription for subscription in subscription_list if subscription.display_name.lower() in subscription_names]:
        print('Subscription: {}'.format(subscription.display_name))
        network_client = get_client_from_cli_profile(NetworkManagementClient, subscription_id=subscription.id)
        flow_logs = network_client.flow_logs.list()
        print('')

'NetworkManagementClient': '2019-06-01',