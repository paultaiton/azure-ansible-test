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
            print('###########  ' + subscription.display_name + '  ###############')
            storage_client = get_client_from_cli_profile(StorageManagementClient,
                                                         subscription_id=subscription.subscription_id)
            storage_accounts = storage_client.storage_accounts.list()
            storage_accounts = [account for account in storage_accounts if account.minimum_tls_version != 'TLS1_2' or
                                                                           account.as_dict().get('allow_blob_public_access', True) or
                                                                           not account.enable_https_traffic_only]
            for account in storage_accounts:
                print(account.id)
                print('minimum_tls_version: ' + account.minimum_tls_version)
                print('allow_blob_public_access: ' + str(account.allow_blob_public_access))
                print('enable_https_traffic_only: ' + str(account.enable_https_traffic_only))
