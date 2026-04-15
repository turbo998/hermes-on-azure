param location string
param resourcePrefix string
param environmentName string
param tenantId string

var kvName = take(replace('${resourcePrefix}-${environmentName}-kv', '-', ''), 24)

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: kvName
  location: location
  properties: {
    tenantId: tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    publicNetworkAccess: 'Enabled'
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
  }
}

output keyVaultUri string = kv.properties.vaultUri
