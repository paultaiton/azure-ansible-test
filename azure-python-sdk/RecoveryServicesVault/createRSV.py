#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.recoveryservices.models import (Vault, Sku, SkuName, VaultProperties)


if __name__ == "__main__":
    subscription_client = get_client_from_cli_profile(SubscriptionClient)
    recoveryservices_client = get_client_from_cli_profile(RecoveryServicesClient)

    # sku_parameter = Sku(name=SkuName.standard)
    # sku_parameter = Sku(name=SkuName.rs0)
    # sku_parameter = Sku(name='RS0')
    sku_parameter = Sku(name='Standard')
    vault_model = Vault(location='westus', sku=sku_parameter, properties=VaultProperties(), tags={'tagname': 'tagvalue'})

    rsv = recoveryservices_client.vaults.create_or_update(resource_group_name='rgname',
                                                          vault_name='vaultname',
                                                          vault=vault_model)

    rsv_dict = rsv.as_dict()
    print('#####')
