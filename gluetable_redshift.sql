-- this creates a schema called "name_of_schema_in_redshift" in Redshift,
-- that works as an alias for the Athena/Glue database "name_of_database_in_glue".
CREATE EXTERNAL SCHEMA name_of_schema_in_redshift
FROM DATA CATALOG
DATABASE 'name_of_database_in_glue'
REGION 'us-east-1'
IAM_ROLE 'arn:aws:iam::456064453472:role/xyz';
