#!/usr/bin/env python
from time import sleep
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

subscription_names = ["subscription-name"]

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    for subscription in subscription_client.subscriptions.list():
        if subscription.display_name in subscription_names:
            print('### ' + subscription.display_name + ' ###')
            compute_client = get_client_from_cli_profile(ComputeManagementClient,
                                                         subscription_id=subscription.subscription_id)
            network_client = get_client_from_cli_profile(ComputeManagementClient,
                                                         subscription_id=subscription.subscription_id)

            compute_list = compute_client.virtual_machines.list_all()
            for vm in compute_list:
                print(vm.availability_set)
                print(vm.id)
                print(vm.diagnostics_profile)
                print(vm.location)
                print(vm.name)
                print(vm.network_profile)
                print(vm.os_profile)
                print(vm.provisioning_state)
                print(vm.storage_profile)
                print(vm.tags)
                print(vm.type)
                print(vm.vm_id)
                print(None)
