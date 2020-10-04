#/usr/bin/env python

#import azure
from azure.common.client_factory import get_client_from_cli_profile

#import azure.mgmt.subscription as SubscriptionModule
#from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource.subscriptions import SubscriptionClient

#import azure.mgmt.resource as ResourceModule
#from azure.mgmt.resource import ResourceManagementClient
#import azure.mgmt.resource.mode as ResourceModule

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    #subscription_get = subscription_client.subscriptions.get('subscription_id')
    subscription_list = subscription_client.subscriptions.list()
    subscription_listraw = list(subscription_client.subscriptions.list())
    for sub in subscription_list:
        print('display_name: {}'.format(sub.display_name))
        print('id: {}'.format(sub.id))
        print('state: {}'.format(sub.state))
        print('subscription_id: {}'.format(sub.subscription_id))
        print('')
    print('Hello world!')
