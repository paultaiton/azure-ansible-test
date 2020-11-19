#!/usr/bin/env python
from time import sleep
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError


if __name__ == "__main__":
    model_parameters = dict(

    )

    storage_account_parameters = dict(
        # access_tier = kwargs.get('access_tier', None),
        # custom_domain = kwargs.get('custom_domain', None),
        # enable_https_traffic_only = kwargs.get('enable_https_traffic_only', False),
        # encryption = kwargs.get('encryption', None),
        # identity = kwargs.get('identity', None),
        # is_hns_enabled = kwargs.get('is_hns_enabled', False)
        # kind = kwargs.get('kind', None),
        # location = kwargs.get('location', None),
        # network_rule_set = kwargs.get('network_rule_set', None),
        # sku = kwargs.get('sku', None),
        # tags = kwargs.get('tags', None),
    )

    storage_client = get_client_from_cli_profile(StorageManagementClient)
    storage_models = StorageManagementClient.models("2019-06-01")

    storage_name = 'storagename'
    resource_group_name = 'resource-group-name'

    storage_accounts = []
    try:
        storage_accounts = storage_client.storage_accounts.list()
        # storage_accounts = [storage_client.storage_accounts.get_properties(resource_group_name=resource_group_name, account_name=storage_name)]
        # storage_accounts = [storage_client.storage_accounts.create(resource_group_name=resource_group_name, account_name=storage_name, parameters)]
        # storage_accounts = storage_client.storage_accounts.delete()
        # storage_accounts = storage_client.storage_accounts.failover()
        # storage_accounts = storage_client.storage_accounts.list_account_sas()
        # storage_accounts = storage_client.storage_accounts.list_by_resource_group()
        # storage_accounts = storage_client.storage_accounts.list_keys()
        # storage_accounts = storage_client.storage_accounts.list_service_sas()
        # storage_accounts = storage_client.storage_accounts.regenerate_key()
        # storage_accounts = storage_client.storage_accounts.restore_blob_ranges()
        # storage_accounts = storage_client.storage_accounts.revoke_user_delegation_keys()
        # storage_accounts = storage_client.storage_accounts.update()
    except CloudError:
        pass
    if not storage_accounts:
        name_check_response = storage_client.storage_accounts.check_name_availability(name=storage_name)

    for account in storage_accounts:
        account_dict = account.as_dict()
        print(account_dict.get('sku', {}).get('name'))
        print(account.id)
        print('minimum_tls_version: ' + str(account.minimum_tls_version))
        print('allow_blob_public_access: ' + str(account.allow_blob_public_access))
        print('enable_https_traffic_only: ' + str(account.enable_https_traffic_only))
        print('')
