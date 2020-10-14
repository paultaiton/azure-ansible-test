#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    # subscription_get = subscription_client.subscriptions.get('')
    subscription_list = subscription_client.subscriptions.list()
    subscription_listraw = list(subscription_client.subscriptions.list())
    for sub in subscription_list:
        print('display_name: {}'.format(sub.display_name))
        print('id: {}'.format(sub.id))
        print('state: {}'.format(sub.state))
        print('subscription_id: {}'.format(sub.subscription_id))
        if sub.tags:
            print('tags: ')
            for key in sub.tags:
                print('  {}: {}'.format(key, sub.tags.get(key)))
        print('tenant_id: {}'.format(sub.tenant_id))
        print('')
    print('Hello world!')
