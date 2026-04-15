param location string
param resourcePrefix string
param environmentName string

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-${environmentName}-law'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

output workspaceCustomerId string = law.properties.customerId
@secure()
output workspaceSharedKey string = listKeys(law.id, '2023-09-01').primarySharedKey
