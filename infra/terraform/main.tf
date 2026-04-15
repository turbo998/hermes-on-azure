terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.20"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

locals {
  rg_name = "${var.resource_prefix}-${var.environment_name}-rg"
}

resource "azurerm_resource_group" "this" {
  name     = local.rg_name
  location = var.location
}

resource "azurerm_log_analytics_workspace" "this" {
  name                = "${var.resource_prefix}-${var.environment_name}-law"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "this" {
  name                       = "${var.resource_prefix}-${var.environment_name}-cae"
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id
}

resource "azurerm_container_app" "hermes" {
  name                         = "${var.resource_prefix}-${var.environment_name}-hermes"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 8080
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1
    max_replicas = 3

    container {
      name   = "hermes-runtime"
      image  = "example.azurecr.io/hermes-agent-on-azure:latest"
      cpu    = 1.0
      memory = "2Gi"
    }
  }
}
