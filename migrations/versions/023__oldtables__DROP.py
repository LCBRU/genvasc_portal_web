from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    Table("administrator", meta, autoload=True).drop()
    Table("etl_delegationLog", meta, autoload=True).drop()
    Table("etl_practice", meta, autoload=True).drop()
    Table("etl_recruit_status", meta, autoload=True).drop()
    Table("etl_user", meta, autoload=True).drop()
    Table("recruit", meta, autoload=True).drop()
    Table("staff_member", meta, autoload=True).drop()
    Table("practice_registrations_users", meta, autoload=True).drop()
    Table("practice_registration", meta, autoload=True).drop()


def downgrade(migrate_engine):
    pass
