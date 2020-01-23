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
        "practice_group",
        meta,
        Column("id", Integer, primary_key=True),
        Column("type", NVARCHAR(255), index=True),
        Column("project_id", Integer, index=True),
        Column("identifier", Integer, index=True),
        Column("name", NVARCHAR(255), nullable=False),
        UniqueConstraint(
            'type',
            'project_id',
            'identifier',
            name='uix__practice_group__type__project_id__identifier'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_group", meta, autoload=True)
    t.drop()
