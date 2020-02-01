import datetime
from sqlalchemy import (
    MetaData,
    Table,
    Column,
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

    project_id = Column("project_id", Integer, index=True)
    project_id.create(t, index_name='idx__user__project_id')
    current_portal_user_yn = Column("current_portal_user_yn", Boolean)
    current_portal_user_yn.create(t)
    gv_end_del_log = Column("gv_end_del_log", Date)
    gv_end_del_log.create(t)
    last_update_timestamp = Column("last_update_timestamp", BigInteger, nullable=True, index=True)
    last_update_timestamp.create(t, index_name="idx__user__last_update_timestamp")
    is_imported = Column("is_imported", Boolean)
    is_imported.create(t)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("user", meta, autoload=True)
    t.c.project_id.drop()
    t.c.current_portal_user_yn.drop()
    t.c.gv_end_del_log.drop()
    t.c.last_update_timestamp.drop()
    t.c.is_imported.drop()
