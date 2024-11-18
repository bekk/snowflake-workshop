# Oppgave 2: Oppsett av roller

## Fyll inn i database.tf
```hcl
resource "snowflake_database" "db" {
  provider = snowflake.accountadmin
  name = "<ditt_database_navn>" # <--- Fyll inn databasenavn
}
```

## Fyll inn i roles.tf
```hcl
resource "snowflake_account_role" "role" {
  provider = snowflake.security_admin
  name     = "<ditt_rollenavn>" # <--- fyll inn ditt rollenavn
}

resource "snowflake_grant_privileges_to_account_role" "database_grant" {
  provider          = snowflake.security_admin
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.role.name
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.db.name
  }
}

```

## Apply og logg inn
Kjør `terraform apply` og se om ressursene blir opprettet som forventet
