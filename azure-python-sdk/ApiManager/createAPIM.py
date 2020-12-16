#!/usr/bin/env python
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.apimanagement import ApiManagementClient
from azure.mgmt.apimanagement.models import ApiManagementServiceUpdateParameters

resource_group_name = ''
service_name = ''

if __name__ == "__main__":
    apimanagement_client = get_client_from_cli_profile(ApiManagementClient)

    apim_create_parameters = ApiManagementServiceUpdateParameters(
        # PARAMETER-DOCS-IN-PYTHONVENV/azure/mgmt/apimanagement/models/_models.py
    )

    apimanagement_client.api_management_service.create_or_update(resource_group_name, service_name, parameters)
