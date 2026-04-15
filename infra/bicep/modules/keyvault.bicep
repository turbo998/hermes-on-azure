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

resource secretAoaiEndpoint 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: kv
  name: 'azure-openai-endpoint'
  properties: {
    value: 'https://replace-me.openai.azure.com/'
  }
}

resource secretFoundryEndpoint 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: kv
  name: 'azure-ai-foundry-endpoint'
  properties: {
    value: 'https://replace-me.services.ai.azure.com/models'
  }
}

resource secretTelegram 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: kv
  name: 'telegram-bot-token'
  properties: {
    value: 'set-after-deployment'
  }
}

output keyVaultUri string = kv.properties.vaultUri
output keyVaultName string = kv.name
