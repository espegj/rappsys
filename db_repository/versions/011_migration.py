from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
test = Table('test', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('test', INTEGER),
)

test2 = Table('test2', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('test', INTEGER),
)

project = Table('project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('connection_id', Integer),
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
    pre_meta.tables['test'].drop()
    pre_meta.tables['test2'].drop()
    post_meta.tables['project'].columns['connection_id'].create()
    post_meta.tables['user'].columns['connection_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['test'].create()
    pre_meta.tables['test2'].create()
    post_meta.tables['project'].columns['connection_id'].drop()
    post_meta.tables['user'].columns['connection_id'].drop()
