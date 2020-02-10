from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    UniqueConstraint,
    PrimaryKeyConstraint,
)


meta = MetaData()


def upgrade(migrate_engine):
    pass

def downgrade(migrate_engine):
    pass
