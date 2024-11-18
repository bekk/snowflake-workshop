# Oppgave 5: Oppsett av datavarehus

## Fyll inn i warehouse.tf
```hcl
resource "snowflake_warehouse" "warehouse" {
  provider       = snowflake.accountadmin
  name           = "${local.my_prefix}-warehouse"
  warehouse_size = "x-small"
}

resource "snowflake_grant_privileges_to_account_role" "warehouse_grant" {
  provider          = snowflake.security_admin
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.role.name
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.warehouse.name
  }
}

```

## Apply og logg inn
Kjør `terraform apply` og se om du får logget inn [her](https://xc63545.europe-west4.gcp.snowflakecomputing.com/)
