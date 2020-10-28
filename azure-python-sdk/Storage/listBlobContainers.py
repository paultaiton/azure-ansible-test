#!/usr/bin/env python
import uuid
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.storage import StorageManagementClient

subscription_id = ''

if __name__ == "__main__":
    storage_client = get_client_from_cli_profile(StorageManagementClient)  # , subscription_id=subscription_id )

    storage_list = storage_client.storage_accounts.list()

    print('########################################################')
    for storage_account in storage_list:
        resource_group_name = storage_account.id.split('/')[4]
        for blob_container in storage_client.blob_containers.list(resource_group_name=resource_group_name, account_name=storage_account.name):
            if blob_container.public_access:
                print(blob_container.id)
