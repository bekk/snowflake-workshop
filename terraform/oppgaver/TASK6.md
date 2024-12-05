# Oppgave 6: Oppsett av storage integration (der man laster inn rådata)

## Fyll inn i storage_integration.tf
```hcl
...

## Fyll inn i storage_integration.tf
```hcl
resource "google_storage_bucket" "snowflake_stage" {
  name          = "<dittnavn>-3123-dqwj" # <--- Fyll inn ditt navn (behold slutten for å holde bøttenavnet unikt)
  location      = "europe-west4"
}

resource "snowflake_storage_integration" "integration" {
  provider = snowflake.accountadmin
  name     = "<ditt integrasjonsnavn>" # <--- Fyll inn ditt integrasjonsnavn her
  comment  = "A GCS storage integration."
  type     = "EXTERNAL_STAGE"
  storage_provider = "GCS"
  storage_allowed_locations = ["gcs://${google_storage_bucket.snowflake_stage.name}/"]
}

resource "google_storage_bucket_iam_member" "integration_storage_admin" {
  bucket = google_storage_bucket.snowflake_stage.name
  role = "roles/storage.admin"
  member = "serviceAccount:${snowflake_storage_integration.integration.storage_gcp_service_account}"
}

resource "google_storage_bucket_iam_member" "integration_storage_object_admin" {
  bucket = google_storage_bucket.snowflake_stage.name
  role = "roles/storage.objectAdmin"
  member = "serviceAccount:${snowflake_storage_integration.integration.storage_gcp_service_account}"
}
```

## Apply og logg inn
Kjør `terraform apply` og opprett et snowflake project (notebook), der du prøver å kjøre SHOW INTEGRATIONS;
