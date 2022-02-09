#!/usr/bin/env python
# Script to convert the value of a tag from old to new on all RGs in a subscription.
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resource.resources import ResourceManagementClient
from msrestazure.azure_exceptions import CloudError
from time import sleep
import re
import json

# ### VARIABLE CONFIGURATIONS ####
subscription_names = [
    "az-subscription-name-01",
    "subscription-02",
    "subscription-03"
]  # list of strings of the full display name of desired subscriptions
tag_name = 'costcenter'

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
        print('Updating RG tag {0} in subscription {1}'.format(tag_name, subscription.display_name))
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
            new_tags = rg.tags
            if new_tags and not new_tags.get(tag_name):
                # Azure returns a case sensitive tag dictionary for key names that are in other cases insensitive.
                # This if block will find those tags where the case sensitive tag_name isn't found, but a
                # case insensitive match is found, and convert them to the case passed in the tag_name global variable.
                # In theory it SHOULDN'T be possible to have multiple tags in Azure on a resource that are the same after .lower(), but .... Microsoft.
                for key, value in list(new_tags.items()):  # list wrap to force copy by value at time of lower() call instead of dynamic iterator object.
                    if key.lower() == tag_name.lower():
                        new_tags[tag_name] = value
                        del new_tags[key]

            if new_tags and new_tags.get(tag_name):
                # TODO for a generic tag value converter, we need to get rid of the regex substitution to only digits
                if tag_conversion_dictionary.get(re.sub(r'\D', '', new_tags.get(tag_name))):  # filter for only digits before lookup in tag dict
                    new_tags["old" + tag_name] = new_tags.get(tag_name)
                    new_tags[tag_name] = tag_conversion_dictionary.get(re.sub(r'\D', '', new_tags.get(tag_name)))
                    print('  Updating resource group {0}, {1} tag value {2} to {3}'.format(rg.name,
                                                                                           tag_name,
                                                                                           new_tags.get("old" + tag_name),
                                                                                           new_tags.get(tag_name)))

                    update_results = False
                    while not update_results:
                        try:
                            # location is required for reasons, even if it's not applicable for an "update" operation.
                            update_results = True  # comment out to preserve retries after API throttling.
                            update_results = resource_client.resource_groups.update(rg.name, {"location": rg.location, "tags": new_tags})
                        except CloudError as e:
                            print('EXCEPTION {}'.format(e))
                            # sleep(10)  # uncomment if you need to pause during API throtting.
                else:
                    print(' Skipping resource group {0}, costcenter {1} '.format(rg.name, new_tags.get(tag_name)))

            # # SECTION TO UNDO
            # # has not been tested since case insensitive tag refactor was added.
            # if rg.tags.get("old" + tag_name):
            #     new_tags = rg.tags
            #     new_tags[tag_name] = rg.tags.get("old" + tag_name)
            #     resource_client.resource_groups.create_or_update(rg.name, {"location": rg.location, "tags": new_tags})  # location is required for reasons.
