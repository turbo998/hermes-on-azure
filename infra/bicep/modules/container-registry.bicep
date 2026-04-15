param location string
param resourcePrefix string
param environmentName string

var acrName = take(toLower(replace('${resourcePrefix}${environmentName}acr', '-', '')), 50)

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Premium'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
  }
}

output loginServer string = acr.properties.loginServer
