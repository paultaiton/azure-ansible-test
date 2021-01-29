#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.managementgroups import ManagementGroupsAPI
from msrestazure.azure_active_directory import UserPassCredentials


def main():
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    management_groups_api = ManagementGroupsAPI(subscription_client.config.credentials)

    for group in management_groups_api.management_groups.list():
        # print('{}'.format(group.display_name))
        print('')
    print('Hello world!')


def get_entities(tenant_id=None):
    credentials = get_credential(tenant_id)

    mgmt_groups_api = ManagementGroupsAPI(credentials)
    entities = mgmt_groups_api.entities.list()
    entity_infos = [entity for entity in entities]
    entity_names = [entity.display_name for entity in entity_infos]
    print(f'    entities: {entity_names}')


if __name__ == '__main__':
    main()
