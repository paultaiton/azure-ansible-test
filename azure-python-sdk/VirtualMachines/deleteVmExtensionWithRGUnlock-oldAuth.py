#!/usr/bin/env python

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource.locks import ManagementLockClient
from msrestazure.azure_exceptions import CloudError
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceExistsError
from msrestazure.tools import parse_resource_id
from time import sleep
import jmespath


# ### VARIABLE CONFIGURATIONS ####
rg_skip_set = set()  # if defined, this will skip VMs that are in one of these RGs

subscription_names_list = [
    "az-subscription-name-01"
]  # list of strings of the full display name of desired subscriptions

vm_extension_names_set = {
    "MDE.Linux",
    "MDE.Windows"
}  # List of VM extensions to delete

if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    # Azure names are not case sensitive in Azure, but python comparisons are.
    subscription_names_list = [x.lower() for x in subscription_names_list]
    rg_skip_set = {x.lower() for x in rg_skip_set}
    vm_extension_names_set = {x.lower() for x in vm_extension_names_set}

    subscription_list = None
    while not subscription_list:
        # If Azure API gives error (like API limit), wait 10 seconds and try again.
        try:
            subscription_list = [x for x in subscription_client.subscriptions.list() if x.display_name.lower() in subscription_names_list]
            if not subscription_list:
                print('No subscriptions matched filter list "subscription_names_list".')
                exit()
        except CloudError as e:
            print('EXCEPTION {}'.format(e))
            sleep(10)

    for subscription in subscription_list:
        print("Starting subscription {0}".format(subscription.display_name))
        rg_bad_vm_set = set()
        compute_client = get_client_from_cli_profile(ComputeManagementClient,
                                                     subscription_id=subscription.subscription_id)
        lock_client = get_client_from_cli_profile(ManagementLockClient,
                                                  subscription_id=subscription.subscription_id)

        all_vm_dictionary_list = [x.as_dict() for x in compute_client.virtual_machines.list_all()
                                  if x.as_dict().get('resources')]
        # Get the lowercase id string from all VMs' resources (extensions) that match the list of extension names
        vm_extension_id_set = {x.get('id').lower() for x in jmespath.search('[].resources[]', all_vm_dictionary_list)
                               if x.get('id').split('/')[-1].lower() in vm_extension_names_set}

        rg_name_set = {x.split('/')[4] for x in vm_extension_id_set} - rg_skip_set

        for rg_name in rg_name_set:
            if rg_bad_vm_set:
                print("\nResource groups with VMs that aren't running:\n{0}\n".format(rg_bad_vm_set))
            delete_lro_poller_list = []
            lock_list = list(lock_client.management_locks.list_at_resource_group_level(rg_name))
            for lock in lock_list:
                lock_parse = parse_resource_id(lock.id)
                print("Delete {0} lock {1} on {2}.".format(lock.level, lock.name, rg_name))
                lock_client.management_locks.delete_at_resource_group_level(rg_name, lock.name)
            for extension_id in vm_extension_id_set:
                extension_parse = parse_resource_id(extension_id)
                if rg_name == extension_parse.get('resource_group').lower():
                    print("Delete extension {0}".format(extension_id))
                    try:
                        delete_lro_poller_list.append(compute_client.virtual_machine_extensions.begin_delete(extension_parse.get('resource_group'),
                                                                                                             extension_parse.get('name'),
                                                                                                             extension_parse.get('child_name_1')))
                    except ResourceExistsError:
                        print("Cannot delete extensions on vm {0}, the machine is most likely not running.".format(extension_parse.get('name')))
                        rg_bad_vm_set.add(rg_name)
            for poller in delete_lro_poller_list:
                poller_finished = False
                while not poller_finished:
                    try:
                        poller_finished = poller.done()
                        # Normal "not-done" state
                        sleep(10)
                    except HttpResponseError:
                        # Abnormal response failure from Azure
                        print('Azure API failure, retrying in 10 seconds')
                        sleep(10)

            for lock in lock_list:
                lock_client.management_locks.create_or_update_at_resource_group_level(rg_name,
                                                                                      lock.name,
                                                                                      {"level": lock.level})
                print("Re-lock {0} on {1}".format(lock.name, rg_name))

            print("")
