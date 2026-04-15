param location string
param resourcePrefix string
param environmentName string

var vnetName = '${resourcePrefix}-${environmentName}-vnet'
var nsgName = '${resourcePrefix}-${environmentName}-nsg'
var acaSubnetName = 'aca-infra-subnet'
var peSubnetName = 'private-endpoints-subnet'

resource nsg 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: nsgName
  location: location
}

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.80.0.0/16'
      ]
    }
    subnets: [
      {
        name: acaSubnetName
        properties: {
          addressPrefix: '10.80.0.0/23'
          delegations: [
            {
              name: 'acaDelegation'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
          networkSecurityGroup: {
            id: nsg.id
          }
        }
      }
      {
        name: peSubnetName
        properties: {
          addressPrefix: '10.80.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
          networkSecurityGroup: {
            id: nsg.id
          }
        }
      }
    ]
  }
}

output containerAppsSubnetId string = resourceId('Microsoft.Network/virtualNetworks/subnets', vnet.name, acaSubnetName)
output privateEndpointSubnetId string = resourceId('Microsoft.Network/virtualNetworks/subnets', vnet.name, peSubnetName)
