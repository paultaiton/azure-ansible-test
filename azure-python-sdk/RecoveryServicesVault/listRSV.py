#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from msrestazure.tools import parse_resource_id


if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    recoveryservices_client = get_client_from_cli_profile(RecoveryServicesClient)

    # rsv_list = recoveryservices_client.vaults.list_by_subscription_id()
    rsv_list = recoveryservices_client.vaults.list_by_resource_group(resource_group_name='rgname')

    for rsv in rsv_list:
        print('#######')
        print('id: {}'.format(rsv.id))
        print('location: {}'.format(rsv.location))
        print('name: {}'.format(rsv.name))
        print('type: {}'.format(rsv.type))
        if rsv.tags:
            print('tags: ')
            for tag in rsv.tags:
                print('{0}: {1}'.format(tag, rsv.tags.get(tag)))
        print('sku_name: ' + rsv.sku.name)
        print('sku_tier: {0}'.format(rsv.sku.additional_properties.get('tier')))
