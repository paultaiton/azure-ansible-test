#/usr/bin/env python

#import azure
from azure.common.client_factory import get_client_from_cli_profile

#import azure.mgmt.subscription as SubscriptionModule
#from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource.subscriptions import SubscriptionClient

#import azure.mgmt.resource as ResourceModule
from azure.mgmt.resource import ResourceManagementClient
#import azure.mgmt.resource.mode as ResourceModule

from azure.mgmt.authorization import AuthorizationManagementClient
subscription_id=''

if __name__ == "__main__":
    authorization_client = get_client_from_cli_profile(AuthorizationManagementClient, subscription_id=subscription_id )
    role_assignment_list = authorization_client.role_assignments.list()
    role_scope_assignment_list = authorization_client.role_assignments.list_for_scope('/subscriptions/' + subscription_id)
    subscription_client = get_client_from_cli_profile(SubscriptionClient, subscription_id=subscription_id)
    subscription_get = subscription_client.subscriptions.get(subscription_id)
    #subscription_list = subscription_client.subscriptions.list()
    #subscription_listcast = list(subscription_client.subscriptions.list())
    for role_assignment in role_assignment_list:
        print('display_name: {}'.format(role_assignment.display_name))
        print('')
    print('Hello world!')
