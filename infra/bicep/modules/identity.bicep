param location string
param resourcePrefix string
param environmentName string
param storageAccountId string

var identityName = '${resourcePrefix}-${environmentName}-uami'

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

resource storageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(storageAccountId)) {
  name: guid(storageAccountId, uami.id, 'Storage Blob Data Contributor')
  scope: resource(storageAccountId, 'Microsoft.Storage/storageAccounts')
  properties: {
    principalId: uami.properties.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalType: 'ServicePrincipal'
  }
}

output managedIdentityId string = uami.id
output managedIdentityClientId string = uami.properties.clientId
output managedIdentityPrincipalId string = uami.properties.principalId
