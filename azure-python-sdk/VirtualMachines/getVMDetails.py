#!/usr/bin/env python
import csv
from azure.common.client_factory import get_client_from_cli_profile

from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from msrestazure.tools import parse_resource_id
from msrestazure.azure_exceptions import CloudError

subscription_names = ["subscription-name"]

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    with open(file='/tmp/azure-vm.csv', mode='w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Headers.
        csvwriter.writerow(["NAME", "SERIAL", "SUBSCRIPTION", "RESOURCE GROUP", "PRIVATE IP ADDRESS", "LOCATION", "STATUS",
                            "TAGS", "OPERATING SYSTEM", "SIZE", "PUBLIC IP ADDRESS", "PUBLIC DNS NAME", "HOST"])

        for subscription in subscription_client.subscriptions.list():
            if subscription.display_name in subscription_names:
                compute_client = get_client_from_cli_profile(ComputeManagementClient,
                                                             subscription_id=subscription.subscription_id)
                network_client = get_client_from_cli_profile(NetworkManagementClient,
                                                             subscription_id=subscription.subscription_id)

                compute_list = compute_client.virtual_machines.list_all()
                for vm in compute_list:
                    # Dictionary allows for .get() methods wich return NULL if not found.
                    vmdict = vm.as_dict()
                    vm_parse_fields = parse_resource_id(vmdict.get('id'))
                    # CSV fields :
                    # "NAME", "SERIAL", "SUBSCRIPTION", "RESOURCE GROUP", "PRIVATE IP ADDRESS", "LOCATION", "STATUS",
                    # "TAGS", "OPERATING SYSTEM", "SIZE", "PUBLIC IP ADDRESS", "PUBLIC DNS NAME", "HOST"
                    name = vmdict.get('name')
                    serial = vmdict.get('vm_id')
                    # subscription already set above.
                    resource_group = vm_parse_fields.get('resource_group').lower()

                    private_ip_address = []
                    public_ip_address = []
                    for vm_nic in vm.network_profile.network_interfaces:
                        nic_parse_fields = parse_resource_id(vm_nic.id)
                        nic = network_client.network_interfaces.get(resource_group_name=nic_parse_fields.get('resource_group'),
                                                                    network_interface_name=nic_parse_fields.get('name'))
                        for config in nic.ip_configurations:
                            if config.private_ip_address:
                                private_ip_address.append(config.private_ip_address)
                            if config.public_ip_address and config.public_ip_address.ip_address:
                                public_ip_address.append(config.public_ip_address.ip_address)

                    location = vmdict.get('location')
                    status = '-'
                    tags = vmdict.get('tags')

                    # try:
                    operating_system = vm.storage_profile.os_disk.os_type
                    # except:
                    #   operating_system = ''

                    size = vmdict.get('hardware_profile', {}).get('vm_size')
                    public_dns_name = '-'
                    host = vm.host

                    csvwriter.writerow([name, serial, subscription.display_name.lower(), resource_group, ','.join(private_ip_address), location, status,
                                        tags, operating_system, size, ','.join(public_ip_address), public_dns_name, host])
