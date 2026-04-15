param location string
param resourcePrefix string
param environmentName string
param backendUrl string

var apimName = take(replace('${resourcePrefix}-${environmentName}-apim', '-', ''), 50)
var apiName = 'hermes-agent-api'

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

resource api 'Microsoft.ApiManagement/service/apis@2023-05-01-preview' = {
  parent: apim
  name: apiName
  properties: {
    path: 'agent'
    protocols: [
      'https'
    ]
    serviceUrl: backendUrl
    displayName: 'Hermes Agent API'
    format: 'openapi+json'
    value: '{"openapi":"3.0.1","info":{"title":"Hermes Agent API","version":"1.0.0"},"paths":{"/invocations":{"post":{"responses":{"200":{"description":"OK"}}}},"/healthz":{"get":{"responses":{"200":{"description":"OK"}}}},"/readyz":{"get":{"responses":{"200":{"description":"OK"}}}}}}'
  }
}

resource policy 'Microsoft.ApiManagement/service/apis/policies@2023-05-01-preview' = {
  parent: api
  name: 'policy'
  properties: {
    format: 'rawxml'
    value: '<policies><inbound><base /><rate-limit calls="120" renewal-period="60" /><set-header name="x-correlation-id" exists-action="skip"><value>@(context.RequestId.ToString())</value></set-header><rewrite-uri template="/invocations" /></inbound><backend><base /></backend><outbound><base /></outbound><on-error><base /></on-error></policies>'
  }
}

output gatewayUrl string = 'https://${apim.name}.azure-api.net'
