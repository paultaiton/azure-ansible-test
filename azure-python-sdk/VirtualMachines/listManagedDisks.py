#!/usr/bin/env python

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

resource_group_name = ''
disk_name = ''

if __name__ == "__main__":
    compute_client = get_client_from_cli_profile(ComputeManagementClient)

    disk_list = compute_client.disks.list()
#   disk_list = [compute_client.disks.get(resource_group_name, disk_name)]
#   disk_list = compute_client.disks.list_by_resource_group(resource_group_name)

    print('###################################')
    for disk in disk_list:
        print(disk.managed_by)
        print(None)
