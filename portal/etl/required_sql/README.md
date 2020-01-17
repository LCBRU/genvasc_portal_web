# Description

In order to provide a consistent and manageable view of the data for
production and testing, the ETL uses views in the source databases.

The query for the source accesses a REDCap database, which
can be quite complex and requires the use of MySQL specific coding.
This would not be transferable to Sqlite for testing puposes.

By using a view in MySQL for the query, we can switch using a
table in Sqlite for testing puposes.

# View Definitions

This folder contains the definitions of the views that should be
created in the source REDCap database.