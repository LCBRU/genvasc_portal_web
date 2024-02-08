import datetime
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Date,
    Boolean,
    DateTime,
    BigInteger,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table("user", meta, autoload=True)

    fs_uniquifier = Column("fs_uniquifier", String(255))
    fs_uniquifier.create(t)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
