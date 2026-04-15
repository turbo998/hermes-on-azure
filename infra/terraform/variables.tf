variable "subscription_id" {
  type = string
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "environment_name" {
  type    = string
  default = "dev"
}

variable "resource_prefix" {
  type    = string
  default = "hermes-az"
}
