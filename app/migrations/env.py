import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool

from alembic import context

# Add the path to your models module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Base  # Import your Base model here

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Ensure the environment variable 'DATABASE_URL' is set to the correct database URL
# This is required for the migration to work
from models import Base
target_metadata = Base.metadata
# Load the database configuration from the URL
config.set_main_option('sqlalchemy.url', )

# Add your metadata object to the Alembic context
target_metadata = Base.metadata

# This function should return the SQLAlchemy engine instance
# you want to use for autogenerate migrations.
# By default, it uses the engine specified in the Alembic config file.
# Modify it if you want to use a different engine.
def get_engine():
    return engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

# This function should return the connection string to the database.
# By default, it uses the connection string specified in the Alembic config file.
# Modify it if you want to use a different connection string.
def get_url():
    return config.get_main_option("sqlalchemy.url")

# Load models for autogenerate support
context.configure(
    url=get_url(),
    target_metadata=target_metadata,
    compare_type=True,
    compare_server_default=True,
    compare_metadata=False,
)

# Add the "models" module to the context, so autogenerate can detect your models
context.configure(
    include_object=lambda name, obj: name if obj.schema == 'public' else False,
    version_table_schema="public",
)

# This line allows the --sql option to generate SQL scripts instead of running migrations
if context.is_offline_mode():
    context.configure(
        url=get_url(), target_metadata=target_metadata, literal_binds=True
    )

# Associate the Alembic environment with the SQLAlchemy engine
with context.begin_transaction():
    context.run_migrations()
