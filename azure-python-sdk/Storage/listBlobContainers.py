#!/usr/bin/env python
import uuid
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from msrestazure.tools import parse_resource_id

subscription_names = ["subscription-name"]

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    for subscription in subscription_client.subscriptions.list():
        if subscription.display_name in subscription_names:
            print('###########' + subscription.display_name + '###############')
            storage_client = get_client_from_cli_profile(StorageManagementClient,
                                                         subscription_id=subscription.subscription_id)
            for storage_account in storage_client.storage_accounts.list():
                resource_group_name = parse_resource_id(storage_account.id).get('resource_group')
                for blob_container in storage_client.blob_containers.list(resource_group_name=resource_group_name,
                                                                          account_name=storage_account.name):
                    if blob_container.public_access != 'None':
                        print(blob_container.id)
