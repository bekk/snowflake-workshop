# Oppgave 1: Oppsett av provider credentials

## Fyll inn i providers.tf
```hcl
provider "snowflake" {
  alias             = "accountadmin"
  organization_name = "URCGQRA"   
  account_name      = "GU27095"   
  user              = "<brukernavn>" # <--- Ditt brukernavn
  password          = "<passord>" # # <--- Ditt passord

  role = "ACCOUNTADMIN"
}

provider "snowflake" {
  alias             = "security_admin"
  organization_name = "URCGQRA"   
  account_name      = "GU27095"
  user              = "<brukernavn>" # <--- Ditt brukernavn
  password          = "<passord>" # # <--- Ditt passord

  role = "SECURITYADMIN"
}

provider "google" {
    project     = "vibber"
    region      = "europe-west4"
    credentials = "./sa-key.json" # <--- last ned og legg i legg rot av Terraform-mappen
}
```

## Test om du får kjørt
Note: `./sa-key.json` blir sendt i faggruppe-kanalen. Når du har har fått inn detaljene, prøv å kjør terraform init