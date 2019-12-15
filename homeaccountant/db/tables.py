import sqlalchemy as sa

metadata = sa.MetaData()

UserSQL = sa.Table('USER', metadata,
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('email', sa.String, nullable=False, unique=True),
                   sa.Column('display_name', sa.String),
                   sa.Column('password_salt', sa.String, nullable=False),
                   sa.Column('password_hash', sa.String, nullable=False),
                   sa.Column('enabled', sa.Boolean, nullable=False, default=False))
