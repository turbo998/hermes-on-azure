param location string
param resourcePrefix string
param environmentName string

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${resourcePrefix}-${environmentName}-uami'
  location: location
}

output managedIdentityId string = uami.id
output managedIdentityClientId string = uami.properties.clientId
