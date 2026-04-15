param location string
param resourcePrefix string
param environmentName string
param subnetId string

var storageName = take(toLower(replace('${resourcePrefix}${environmentName}st', '-', '')), 24)
var blobContainerName = 'hermes-workspace'

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    publicNetworkAccess: 'Enabled'
  }
}

resource blobSvc 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: sa
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      enabled: true
      days: 14
    }
    containerDeleteRetentionPolicy: {
      enabled: true
      days: 14
    }
    isVersioningEnabled: true
  }
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobSvc
  name: blobContainerName
  properties: {
    publicAccess: 'None'
  }
}

output storageAccountName string = sa.name
output storageAccountId string = sa.id
output blobContainerName string = blobContainerName
