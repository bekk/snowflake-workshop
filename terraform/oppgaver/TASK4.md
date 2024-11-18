# Oppgave 4: Oppsett av bruker

## Fyll inn i users.tf
```hcl
resource "snowflake_user" "user" {
    provider          = snowflake.security_admin
    name              = "<brukernavn>" # <--- Fyll inn brukernavn her
    password          = "<passord>" # <---- Fyll inn ditt passord her
    default_warehouse = snowflake_warehouse.warehouse.name
    default_role      = snowflake_account_role.role.name
    default_namespace = "${snowflake_database.db.name}.${snowflake_schema.schema.name}"
}

resource "snowflake_grant_privileges_to_account_role" "user_grant" {
  provider          = snowflake.security_admin
  privileges        = ["MONITOR"]
  account_role_name = snowflake_account_role.role.name  
  on_account_object {
    object_type = "USER"
    object_name = snowflake_user.user.name
  }
}

resource "snowflake_grant_account_role" "grants" {
  provider  = snowflake.security_admin
  role_name = snowflake_account_role.role.name
  user_name = snowflake_user.user.name
}
```

## Apply og logg inn
Kjør `terraform apply` og se om du får logget inn [her](https://xc63545.europe-west4.gcp.snowflakecomputing.com/)
