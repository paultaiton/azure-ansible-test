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
subscription_names = ["az-subscription-name-01"]  # list of strings of the full display name of desired subscriptions
tag_name = 'costcenter'

if __name__ == "__main__":
    with open(tag_name + "_conversion_values.json", "r") as tag_file:
        tag_conversion_dictionary = json.loads(tag_file.read())
    print('')  # I like clean breaks
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
            if rg.tags.get(tag_name):
                # TODO for a generic tag value converter, we need to get rid of the regex substitution to only digits
                # if tag_conversion_dictionary.get(rg.tags.get(tag_name)):
                if tag_conversion_dictionary.get(re.sub(r'\D', '', rg.tags.get(tag_name))):  # filter for only digits before lookup in tag dict
                    new_tags = rg.tags
                    new_tags["old" + tag_name] = rg.tags.get(tag_name)
                    new_tags[tag_name] = tag_conversion_dictionary.get(re.sub(r'\D', '', rg.tags.get(tag_name)))
                    resource_client.resource_groups.create_or_update(rg.name, {"location": rg.location, "tags": new_tags})  # location is required for reasons.
