from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
change = Table('change', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=255)),
    Column('task', Integer),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('path', String(length=255)),
    Column('change', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['change'].create()
    post_meta.tables['image'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['change'].drop()
    post_meta.tables['image'].drop()
