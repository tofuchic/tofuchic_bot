module "scheduled-function" {
  source                    = "terraform-google-modules/scheduled-function/google"
  version                   = "2.0.0"
  project_id                = "tofuchicbot"
  job_name                  = "fire-tofuchicbot"
  job_schedule              = "*/5 * * * *"
  function_entry_point      = "tofav"
  function_source_directory = "${path.module}/../src"
  function_name             = "tofuchicbot"
  region                    = "us-central1"
  function_runtime          = "python38"
}

resource "google_firestore_document" "mydoc" {
  project     = "tofuchicbot"
  collection  = "tofuchic_bot"
  document_id = "trigger_log"
  fields      = "{\"something\":{\"mapValue\":{\"fields\":{\"akey\":{\"stringValue\":\"avalue\"}}}}}"
}
