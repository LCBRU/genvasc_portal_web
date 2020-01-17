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
        "etl_ccg",
        meta,
        Column("id", Integer, primary_key=True),
        Column("project_id", Integer, primary_key=True),
        Column("ccg_id", Integer, primary_key=True),
        Column("name", NVARCHAR(255), nullable=False),
        UniqueConstraint(
            'project_id',
            'ccg_id',
            name='uix__etl_ccg__project_id__ccg_id'
        ),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("etl_ccg", meta, autoload=True)
    t.drop()
