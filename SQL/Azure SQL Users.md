---
id: tech_azure_sql_users
title: Azure SQL User Setup
domain: sql
layer: agnostic
artifact: database_user
technology: azure_sql
status: draft
---
# Azure SQL User Setup

## User types

For Entra identities, SQL uses two user types:

- `E` represents an Entra user, app, or managed identity. Use the **Object ID** for a person and the **Application (client) ID** for an app or managed identity.
- `X` represents an Entra group. Use the group's **Object ID**.

The type describes the identity, not its database permissions.

## Option 1: Exact Entra display name

Using the existing Entra display name is the simplest option to write. SQL resolves the identity through `FROM EXTERNAL PROVIDER`.

```sql
CREATE USER [Warehouse Integration] FROM EXTERNAL PROVIDER;
```

If the display name is duplicated in Entra, the statement fails. Use Option 2 to identify the intended object by its GUID and give it a unique database username.

## Option 2: Modified display name

Suggested prefixes:

- **Entra user:** `User | <display name>`
- **Entra security group:** `Security Group | <display name>`
- **Application:** `App Registration | <display name>`
- **Managed identity:** `Managed Identity | <display name>`

Set the database display name, identity GUID, and user type below. SQL uses the supplied GUID without validating it against Entra. This example is configured for an application; replace the all-zero GUID with its client ID.

```sql
DECLARE @userName SYSNAME = N'App Registration | Warehouse Integration';
DECLARE @identityId UNIQUEIDENTIFIER = '00000000-0000-0000-0000-000000000000';
-- E = Entra user, app, or managed identity; X = Entra group.
DECLARE @userType CHAR(1) = 'E';

DECLARE @sid VARCHAR(34) = CONVERT(VARCHAR(34), CONVERT(BINARY(16), @identityId), 1);
DECLARE @sql NVARCHAR(MAX) =
    N'CREATE USER ' + QUOTENAME(@userName)
    + N' WITH SID = ' + @sid + N', TYPE = ' + @userType + N';';
EXEC sys.sp_executesql @sql;
```

## Recover the related GUID

The query returns each user's GUID and explains where to look for the identity in Azure. Perform the lookup in the SQL server's Entra tenant.

```sql
SELECT
      dp.name AS UserName
     -- Translate SQL's external principal types.
     ,CASE dp.type
          WHEN 'E' THEN 'Entra user, app, or managed identity'
          WHEN 'X' THEN 'Entra group'
      END     AS IdentityType
     -- SID is binary; convert only 16-byte GUID SIDs.
     ,CASE
          WHEN DATALENGTH(dp.sid) = 16 THEN CONVERT(UNIQUEIDENTIFIER, dp.sid)
      END     AS EntraGuid
     -- Identify the Azure object category and searchable ID field.
     ,CASE dp.type
          WHEN 'E' THEN 'Enterprise applications: Application (client) ID; or Entra users: Object ID'
          WHEN 'X' THEN 'Entra groups: Object ID'
      END     AS AzureLookup
FROM sys.database_principals AS dp
WHERE dp.type IN ('E', 'X')
ORDER BY dp.name;
```

SQL uses `E` for people, apps, and managed identities, so the query cannot distinguish between them. For an app or managed identity, the GUID is its client ID. For a person or group, it is the Object ID.

## Open decisions (not standards)

The default naming option and identity-type prefixes remain undecided.

## Supporting references

- [Microsoft: CREATE USER, including SID and TYPE examples](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql?view=sql-server-ver17)
