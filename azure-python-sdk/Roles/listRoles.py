#/usr/bin/env python

#import azure
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.authorization import AuthorizationManagementClient
subscription_id=''

if __name__ == "__main__":
    authorization_client = get_client_from_cli_profile(AuthorizationManagementClient) #, subscription_id=subscription_id )

    role_get = authorization_client.role_assignments.get(scope=None, role_assignment_name='8b07e10d-ed4a-45a1-9f57-ca1bb23b29c5')
    #role_list = authorization_client.role_assignments.list()
    #role_list_for_resource_group = authorization_client.role_assignments.list_for_resource_group(resource_group_name='')
    #role_list_for_scope = authorization_client.role_assignments.list_for_scope(scope='')
    #role_get_by_id = authorization_client.role_assignments.get_by_id(role_id='')
    #role_list_for_resource = authorization_client.role_assignments.list_for_resource(resource_group_name='', resource_provider_namespace='', parent_resource_path='', resource_type='', resource_name='')
    

    for role_assignment in role_list:
        print('id: {}'.format(role_assignment.id))
        print('name: {}'.format(role_assignment.name))
        print('principal_id: {}'.format(role_assignment.principal_id))
        print('principal_type: {}'.format(role_assignment.principal_type))
        print('role_definition_id: {}'.format(role_assignment.role_definition_id))
        print('scope: {}'.format(role_assignment.scope))
        print('type: {}'.format(role_assignment.type))
        print('')
