# Oppgave 3: Oppsett av schema

## Fyll videre inn i database.tf
```hcl
...

resource "snowflake_schema" "schema" {
  provider = snowflake.accountadmin
  database   = snowflake_database.db.name
  name       = "<ditt_schema_navn>" # <--- Fyll inn ditt schemanavn
  with_managed_access = false
}
```

## Fyll videre inn i roles.tf
```hcl
resource "snowflake_grant_privileges_to_account_role" "schema_grant" {
  provider          = snowflake.security_admin
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.role.name
  on_schema {
    schema_name = "\"${snowflake_database.db.name}\".\"${snowflake_schema.schema.name}\""
  }
}
```

## Apply og logg inn
Kjør `terraform apply` og se om ressursene blir opprettet som forventet
