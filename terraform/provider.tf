terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.78.0"
    }
    # vault = {
    #   source  = "hashicorp/vault"
    #   version = "2.22.1"
    # }
    # archive = {
    #   source  = "hashicorp/archive"
    #   version = "2.2.0"
    # }
  }
}

// Configure the Google Cloud provider
provider "google" {
  credentials = file("./tofuchicbot-terraform.json")
  project     = "tofuchicbot"
  region      = "asia-northeast1"
}

# provider "vault" {
#   # Configuration options
# }

# provider "archive" {
#   # Configuration options
# }
