#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.managementgroups import ManagementGroupsAPI
from msrestazure.azure_active_directory import UserPassCredentials


def main():
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    management_groups_api = ManagementGroupsAPI(subscription_client.config.credentials)
    print('')

    for group in management_groups_api.management_groups.list():
        print('display_name: {}'.format(group.display_name))
        print('id: {}'.format(group.id))
        print('name: {}'.format(group.name))
        print('tenant_id: {}'.format(group.tenant_id))
        print('type: {}'.format(group.type))
        print('')


if __name__ == '__main__':
    main()
