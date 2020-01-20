from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    UniqueConstraint,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "etl_federation",
        meta,
        Column("id", Integer, primary_key=True),
        Column("project_id", Integer, primary_key=True),
        Column("federation_id", Integer, primary_key=True),
        Column("name", NVARCHAR(255), nullable=False),
        UniqueConstraint(
            'project_id',
            'federation_id',
            name='uix__etl_federation__project_id__federation_id'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_federation", meta, autoload=True)
    t.drop()
