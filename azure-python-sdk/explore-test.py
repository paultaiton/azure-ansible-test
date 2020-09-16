#/usr/bin/env python

#import azure
from azure.common.client_factory import get_client_from_cli_profile

import azure.mgmt.subscription as SubscriptionModule
from azure.mgmt.subscription import SubscriptionClient

#import azure.mgmt.resource as ResourceModule
#from azure.mgmt.resource import ResourceManagementClient
#import azure.mgmt.resource.mode as ResourceModule

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    print('Hello world!')
