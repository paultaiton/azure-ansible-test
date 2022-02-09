#!/usr/bin/env python
# Script to convert the value of a tag from old to new on all resources in a subscription.
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from msrestazure.azure_exceptions import CloudError
from time import sleep
import re
import json

# ### VARIABLE CONFIGURATIONS ####
subscription_names = ["az-subscription-name-01"]  # list of strings of the full display name of desired subscriptions
tag_name = 'costcenter'  # as currently written only costcenter is supported. See TODO below to change.

provider_api_dict = dict()

if __name__ == "__main__":
    with open(tag_name + "_conversion_values.json", "r") as tag_file:
        tag_conversion_dictionary = json.loads(tag_file.read())
    subscription_client = get_client_from_cli_profile(SubscriptionClient)

    # Subscription names are not case sensitive in Azure, but python comparisons are.
    subscription_names = [x.lower() for x in subscription_names]

    subscription_list = None
    while not subscription_list:
        # If Azure API gives error (like API limit), wait 10 seconds and try again.
        try:
            subscription_list = [x for x in subscription_client.subscriptions.list() if x.display_name.lower() in subscription_names]
            if not subscription_list:
                print('No subscriptions matched filter list "subscription_names".')
                exit()
        except CloudError as e:
            print('EXCEPTION {}'.format(e))
            sleep(10)

    for subscription in subscription_list:
        print('Evaluating resource tag {0} in subscription {1} for updates.'.format(tag_name, subscription.display_name))
        resource_client = get_client_from_cli_profile(ResourceManagementClient,
                                                      subscription_id=subscription.subscription_id)

        rg_list = None
        while not rg_list:
            # If Azure API gives error (like API limit), wait 10 seconds and try again.
            try:
                rg_list = resource_client.resource_groups.list()
            except CloudError as e:
                print('EXCEPTION {}'.format(e))
                sleep(10)

        for rg in rg_list:
            # Dictionary allows for .get() methods wich return NULL if not found.
            rg_dict = rg.as_dict()

            resource_list = None
            while not resource_list:
                try:
                    resource_list = resource_client.resources.list_by_resource_group(rg.name)
                except CloudError as e:
                    print('EXCEPTION {}'.format(e))
                    sleep(10)
            for resource in resource_list:
                resource_dict = resource.as_dict()
                if resource_dict.get('tags', {}).get(tag_name):
                    # TODO for a generic tag value converter, we need to get rid of the regex substitution to only digits
                    # if tag_conversion_dictionary.get(resource.tags.get(tag_name)):
                    if tag_conversion_dictionary.get(re.sub(r'\D', '', resource.tags.get(tag_name))):  # filter for only digits before lookup in tag dict
                        new_tags = resource.tags
                        new_tags["old" + tag_name] = resource.tags.get(tag_name)
                        new_tags[tag_name] = tag_conversion_dictionary.get(re.sub(r'\D', '', resource.tags.get(tag_name)))
                        print('  Updating resource {0}, {1} tag value {2} to {3}'.format(resource.name,
                                                                                         tag_name,
                                                                                         new_tags.get("old" + tag_name),
                                                                                         new_tags.get(tag_name)))

                        resource_type = resource_dict.get('type')
                        if not provider_api_dict.get(resource_type.lower()):
                            print('  Provider lookup for {0} namespace, triggered by type {1}.'.format(resource_type.split('/')[0],
                                                                                                       ''.join(resource_type.split('/')[1:])))
                            provider = None
                            while not provider:
                                try:
                                    # get call will fetch all versions within the top namespace at once.
                                    provider = resource_client.providers.get(resource_provider_namespace=resource_type.split('/')[0])
                                except CloudError as e:
                                    print('EXCEPTION {}'.format(e))
                                    sleep(10)

                            for type in provider.resource_types:
                                # And we cache all the discrete types separately.
                                provider_api_dict['/'.join([provider.namespace.lower(),
                                                            type.resource_type.lower()])] = type.api_versions[0]

                        resource_client.resources.update_by_id(resource_id=resource.id,
                                                               api_version=provider_api_dict[resource_type.lower()],
                                                               parameters={"tags": new_tags})

                    # # # SECTION TO UNDO
                    # if resource.tags.get("old" + tag_name):
                    #     new_tags = resource.tags
                    #     new_tags[tag_name] = resource.tags.get("old" + tag_name)
                    #     resource_client.resources.begin_update_by_id(resource.id,
                    #                                                  resource_client.DEFAULT_API_VERSION,
                    #                                                  {"location": rg.location,  # location is required for reasons.
                    #                                                   "tags": new_tags})
