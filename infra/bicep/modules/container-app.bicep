param location string
param resourcePrefix string
param environmentName string
param infrastructureSubnetId string
param managedIdentityId string
param managedIdentityClientId string
param acrLoginServer string
param storageAccountName string
param storageContainerName string
param keyVaultUri string
param logAnalyticsCustomerId string
@secure()
param logAnalyticsSharedKey string

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${resourcePrefix}-${environmentName}-cae'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsCustomerId
        sharedKey: logAnalyticsSharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: infrastructureSubnetId
      internal: false
    }
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${resourcePrefix}-${environmentName}-hermes'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentityId}': {}
    }
  }
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
      }
      registries: [
        {
          server: acrLoginServer
          identity: managedIdentityId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'hermes-runtime'
          image: '${acrLoginServer}/hermes-agent-on-azure:latest'
          env: [
            {
              name: 'AZURE_CLIENT_ID'
              value: managedIdentityClientId
            }
            {
              name: 'WORKSPACE_STORAGE_ACCOUNT'
              value: storageAccountName
            }
            {
              name: 'WORKSPACE_CONTAINER'
              value: storageContainerName
            }
            {
              name: 'WORKSPACE_NAMESPACE'
              value: '${environmentName}-default'
            }
            {
              name: 'KEY_VAULT_URI'
              value: keyVaultUri
            }
            {
              name: 'HERMES_PROVIDER_MODE'
              value: 'azure-openai'
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: 'gpt-4o'
            }
          ]
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/healthz'
                port: 8080
              }
              initialDelaySeconds: 10
              periodSeconds: 15
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/readyz'
                port: 8080
              }
              initialDelaySeconds: 15
              periodSeconds: 10
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

output ingressUrl string = 'https://${app.properties.configuration.ingress.fqdn}'
