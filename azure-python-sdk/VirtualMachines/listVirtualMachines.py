#!/usr/bin/env python

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

resource_group_name = ''
location = ''
vm_name = ''

if __name__ == "__main__":
    compute_client = get_client_from_cli_profile(ComputeManagementClient)

    compute_list = compute_client.virtual_machines.list_all()
#   compute_list = compute_client.virtual_machines.list(resource_group_name=resource_group_name)
#   compute_list = compute_client.virtual_machines.list_by_location(location=location)
#   compute_list = compute_client.virtual_machines.list_available_sizes(resource_group_name=resource_group_name, vm_name=vm_name)
#   compute_list = [compute_client.virtual_machines.get(resource_group_name=resource_group_name, vm_name=vm_name)]
    print('###################################')
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
