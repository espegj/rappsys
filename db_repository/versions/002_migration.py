from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
connection = Table('connection', post_meta,
    Column('user', Integer, primary_key=True, nullable=False),
    Column('project', Integer, primary_key=True, nullable=False),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=255), nullable=False),
    Column('password', String(length=255), nullable=False),
    Column('registered_on', DateTime, nullable=False),
    Column('admin', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('connection_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['connection'].create()
    post_meta.tables['user'].columns['connection_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['connection'].drop()
    post_meta.tables['user'].columns['connection_id'].drop()
