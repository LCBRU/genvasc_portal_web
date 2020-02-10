from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    ForeignKey,
    NVARCHAR,
)


meta = MetaData()


def upgrade(migrate_engine):
    pass

def downgrade(migrate_engine):
    pass