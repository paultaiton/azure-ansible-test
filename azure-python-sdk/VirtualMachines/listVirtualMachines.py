#/usr/bin/env python

#import azure
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.compute import ComputeManagementClient

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    compute_client = get_client_from_cli_profile( ComputeManagementClient )
    subscription_list = subscription_client.subscriptions.list()

    compute_list_all = compute_client.virtual_machines.list_all()
    #compute_list_by_location = compute_client.virtual_machines.list_by_location(location='xyz')
    #compute_list = compute_client.virtual_machines.list(resource_group_name='xyz')
    #compute_get = compute_client.virtual_machines.get(resource_group_name='xyz', vm_name='xyz')
    for vm in compute_list_all:
        print( 'Hello World ')

    #for sub in subscription_list:
        #print('display_name: {}'.format(sub.display_name))
        #print('id: {}'.format(sub.id))
        #print('state: {}'.format(sub.state))
        #print('subscription_id: {}'.format(sub.subscription_id))
        #if sub.tags:
            #print('tags: ')
            #for key in sub.tags:
                #print('  {}: {}'.format(key, sub.tags.get(key)) )
        #print('tenant_id: {}'.format(sub.tenant_id))
        #print('')
    #print('Hello world!')
