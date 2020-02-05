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
    meta.bind = migrate_engine

    t = Table(
        "practice_group",
        meta,
        Column("type", NVARCHAR(255)),
        Column("project_id", Integer),
        Column("identifier", Integer),
        Column("name", NVARCHAR(255), nullable=False),
        PrimaryKeyConstraint(
            'type',
            'project_id',
            'identifier',
            name='pk__practice_group__type__project_id__identifier'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("practice_group", meta, autoload=True)
    t.drop()
