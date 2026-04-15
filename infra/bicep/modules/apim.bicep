param location string
param resourcePrefix string
param environmentName string
param backendUrl string

var apimName = take(replace('${resourcePrefix}-${environmentName}-apim', '-', ''), 50)

resource apim 'Microsoft.ApiManagement/service@2023-05-01-preview' = {
  name: apimName
  location: location
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherEmail: 'platform@example.com'
    publisherName: 'Platform Team'
  }
}

output gatewayUrl string = 'https://${apim.name}.azure-api.net'
