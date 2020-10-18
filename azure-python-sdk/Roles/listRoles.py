#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.authorization import AuthorizationManagementClient
subscription_id = ''

if __name__ == "__main__":
    authorization_client = get_client_from_cli_profile(AuthorizationManagementClient)  # , subscription_id=subscription_id )
    authorization_models = AuthorizationManagementClient.models('2018-09-01-preview')

    parameters = authorization_models.RoleAssignmentCreateParameters(role_definition_id=''
                                                                     principal_id=''
                                                                     principal_type=''
                                                                     can_delegate='')

    role_list = authorization_client.role_assignments.list(filter=None, custom_headers=None, raw=False)
    role_get = authorization_client.role_assignments.get(scope='', role_assignment_name='', custom_headers=None, raw=False)
    role_list_for_resource_group = authorization_client.role_assignments.list_for_resource_group(resource_group_name='', filter=None, custom_headers=None, raw=False)
    role_list_for_scope = authorization_client.role_assignments.list_for_scope(scope='', filter='atScope()', custom_headers=None, raw=False)
    role_get_by_id = authorization_client.role_assignments.get_by_id(role_id='', custom_headers=None, raw=False)
    role_list_for_resource = authorization_client.role_assignments.list_for_resource(resource_group_name='', resource_provider_namespace='', parent_resource_path='',
                                                                                     resource_type='', resource_name='', filter=None, custom_headers=None, raw=False)

    # for role_assignment in role_list:
    # for role_assignment in [ role_get ]:
    print('########################################################')
    for role_assignment in role_list_for_scope:
        print('id: {}'.format(role_assignment.id))
        print('name: {}'.format(role_assignment.name))
        print('principal_id: {}'.format(role_assignment.principal_id))
        print('principal_type: {}'.format(role_assignment.principal_type))
        print('role_definition_id: {}'.format(role_assignment.role_definition_id))
        print('scope: {}'.format(role_assignment.scope))
        print('type: {}'.format(role_assignment.type))
        print('')
