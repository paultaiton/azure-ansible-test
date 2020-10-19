#!/usr/bin/env python
import uuid
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.authorization import AuthorizationManagementClient

subscription_id = ''
scope = ''
role_assignment_name = '199d4427-8709-4d93-a15b-61d377708ae6'
role_assignment_id = '' + '199d4427-8709-4d93-a15b-61d377708ae6'
role_definition_id = ''
principal_id = ''

if __name__ == "__main__":
    authorization_client = get_client_from_cli_profile(AuthorizationManagementClient)  # , subscription_id=subscription_id )
    authorization_models = AuthorizationManagementClient.models('2018-09-01-preview')

    parameters = authorization_models.RoleAssignmentCreateParameters(role_definition_id=role_definition_id,
                                                                     principal_id=principal_id,
                                                                     principal_type='User',
                                                                     can_delegate=None)

    # role_list = authorization_client.role_assignments.list(filter=None, custom_headers=None, raw=False)

    print('########################################################')

    # for role_assignment in role_list:
    #     print('id: {}'.format(role_assignment.id))
    #     print('name: {}'.format(role_assignment.name))
    #     print('principal_id: {}'.format(role_assignment.principal_id))
    #     print('principal_type: {}'.format(role_assignment.principal_type))
    #     print('role_definition_id: {}'.format(role_assignment.role_definition_id))
    #     print('scope: {}'.format(role_assignment.scope))
    #     print('type: {}'.format(role_assignment.type))
    #     print('')

    results = authorization_client.role_assignments.create(scope=scope, role_assignment_name=role_assignment_name, parameters=parameters)
    #results = authorization_client.role_assignments.create_by_id(role_id=role_definition_id, parameters=parameters)
