import sqlalchemy as sa

metadata = sa.MetaData()

UserSQL = sa.Table(
    'USER', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('display_name', sa.String),
    sa.Column('password_salt', sa.String, nullable=False),
    sa.Column('password_hash', sa.String, nullable=False),
    sa.Column('enabled', sa.Boolean, nullable=False, default=False)
)

AccountSQL = sa.Table(
    'ACCOUNT', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('acronym', sa.String),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('USER.id'))
)

TransactionFamilySQL = sa.Table(
    'TRANSACTION_FAMILY', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False, unique=True)
    )

TransactionCategorySQL = sa.Table(
    'TRANSACTION_CATEGORY', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('USER.id')),
    sa.Column('family_id', sa.Integer, sa.ForeignKey('TRANSACTION_FAMILY.id'))
)

TransactionSQL = sa.Table(
    'TRANSACTION', metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('name', sa.String),
    sa.Column('value', sa.Float, nullable=False),
    sa.Column('description', sa.String),
    sa.Column('category_id', sa.Integer, sa.ForeignKey('TRANSACTION_CATEGORY.id')),
    sa.Column('account_id', sa.Integer, sa.ForeignKey('ACCOUNT.id')),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('USER.id'))
)

PermanentTransactionSQL = sa.Table(
    'PERMANENT_TRANSACTION', metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('frequency', sa.String, nullable=False),
    sa.Column('name', sa.String),
    sa.Column('value', sa.Float, nullable=False),
    sa.Column('description', sa.String),
    sa.Column('category_id', sa.Integer, sa.ForeignKey('TRANSACTION_CATEGORY.id')),
    sa.Column('account_id', sa.Integer, sa.ForeignKey('ACCOUNT.id')),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('USER.id'))
)