targetScope = 'subscription'

@description('Azure location for deployment')
param location string = 'eastus2'

@description('Environment name')
param environmentName string = 'dev'

@description('Resource prefix')
param resourcePrefix string = 'hermes-az'

var resourceGroupName = '${resourcePrefix}-${environmentName}-rg'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: {
    workload: 'hermes-agent'
    environment: environmentName
    architecture: 'caf-waf'
  }
}

module network 'modules/network.bicep' = {
  name: 'network'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
  }
}

module identity 'modules/identity.bicep' = {
  name: 'identity'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
    subnetId: network.outputs.privateEndpointSubnetId
  }
}

module keyvault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
    tenantId: subscription().tenantId
  }
}

module acr 'modules/container-registry.bicep' = {
  name: 'acr'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
  }
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
  }
}

module containerApp 'modules/container-app.bicep' = {
  name: 'containerapp'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
    infrastructureSubnetId: network.outputs.containerAppsSubnetId
    managedIdentityId: identity.outputs.managedIdentityId
    managedIdentityClientId: identity.outputs.managedIdentityClientId
    acrLoginServer: acr.outputs.loginServer
    storageAccountName: storage.outputs.storageAccountName
    keyVaultUri: keyvault.outputs.keyVaultUri
    logAnalyticsCustomerId: monitoring.outputs.workspaceCustomerId
    logAnalyticsSharedKey: monitoring.outputs.workspaceSharedKey
  }
}

module apim 'modules/apim.bicep' = {
  name: 'apim'
  scope: rg
  params: {
    location: location
    resourcePrefix: resourcePrefix
    environmentName: environmentName
    backendUrl: containerApp.outputs.ingressUrl
  }
}
