#!/usr/bin/python3
if not azureTag:
  if direction == "Inbound":
    nsg.security_rules.append(SecurityRule(protocol=protocol, access=access, direction=direction, description=description, source_port_range='*', destination_port_ranges=dport, source_address_prefixes=peer, destination_address_prefix=snet, priority=priority, name=ruleName) )
  if direction == "Outbound":
    nsg.security_rules.append(SecurityRule(protocol=protocol, access=access, direction=direction, description=description, source_port_range='*', destination_port_ranges=dport, source_address_prefix=snet, destination_address_prefixes=peer, priority=priority, name=ruleName) )
if azureTag:
  if direction == "Inbound":
    nsg.security_rules.append(SecurityRule(protocol=protocol, access=access, direction=direction, description=description, source_port_range='*', destination_port_ranges=dport, source_address_prefix=peer, destination_address_prefix=snet, priority=priority, name=ruleName) )
  if direction == "Outbound":
    nsg.security_rules.append(SecurityRule(protocol=protocol, access=access, direction=direction, description=description, source_port_range='*', destination_port_ranges=dport, source_address_prefix=snet, destination_address_prefix=peer, priority=priority, name=ruleName) )

nsg.flow_logs = []
network_client.network_security_groups.create_or_update(resource_group_name=resourceGroup, network_security_group_name=networkSecurityGroup, parameters=nsg)
