#!/usr/bin/env python
from time import sleep
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

subscription_names = [
    "az-core-nonprod-01",
    "az-core-prod-01",
    "az-entaks-nonprod-01",
    "az-entaks-nonprod-02",
    "az-entaks-prod-01",
    "az-entaks-prod-02",
    "az-entapp-nonprod-01",
    "az-entapp-prod-01",
    "az-entcore-prod-01",
    "az-imvd-prod-01",
    "az-metrc-nonprod-01",
    "az-pciapp-nonprod-01",
    "az-pciapp-prod-01",
    "az-phiapp-nonprod-01",
    "az-phiapp-prod-01",
    "az-resapp-nonprod-01",
    "az-resapp-prod-01",
    "az-resibm-nonprod-01",
    "az-resibm-prod-01",
    "az-resmetrc-nonprod-01",
    "az-resmetrc-prod-01"
]


if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    for subscription in subscription_client.subscriptions.list():
        if subscription.display_name in subscription_names:
            print('###########  ' + subscription.display_name + '  ###############')
            storage_client = get_client_from_cli_profile(StorageManagementClient,
                                                         subscription_id=subscription.subscription_id)

            storage_accounts = []
            try:
                storage_accounts = storage_client.storage_accounts.list()
                storage_accounts = [account for account in storage_accounts if account.as_dict().get('allow_blob_public_access', True)]
            except CloudError as error:
                print('Azure Cloud Error: {}'.format(error))
                sleep(5)

            for storage_account in storage_accounts:
                try:
                    resource_group_name = parse_resource_id(storage_account.id).get('resource_group')
                    for blob_container in storage_client.blob_containers.list(resource_group_name=resource_group_name,
                                                                              account_name=storage_account.name):
                        if blob_container.public_access and blob_container.public_access != 'None':
                            print(blob_container.id)
                            print("Blob Public Access: {}".format(blob_container.public_access))
                except CloudError as error:
                    print('Azure Cloud Error: {}'.format(error))
                    sleep(5)
