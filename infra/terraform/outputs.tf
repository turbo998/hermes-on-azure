output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "container_app_name" {
  value = azurerm_container_app.hermes.name
}
