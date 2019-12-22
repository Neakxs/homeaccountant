import sqlalchemy as sa

metadata = sa.MetaData()

UserSQL = sa.Table(
    'USER', metadata,
    sa.Column('uid', sa.Integer, primary_key=True),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('display_name', sa.String),
    sa.Column('password_salt', sa.String, nullable=False),
    sa.Column('password_hash', sa.String, nullable=False),
    sa.Column('enabled', sa.Boolean, nullable=False, default=False)
)

AccountSQL = sa.Table(
    'ACCOUNT', metadata,
    sa.Column('uid', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('summary', sa.Float),
    sa.Column('acronym', sa.String),
    sa.Column('user_uid', sa.Integer, sa.ForeignKey('USER.uid'))
)

TransactionFamilySQL = sa.Table(
    'TRANSACTION_FAMILY', metadata,
    sa.Column('uid', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False, unique=True)
    )

TransactionCategorySQL = sa.Table(
    'TRANSACTION_CATEGORY', metadata,
    sa.Column('uid', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False, unique=True),
    sa.Column('user_uid', sa.Integer, sa.ForeignKey('USER.uid')),
    sa.Column('transaction_family_uid', sa.Integer, sa.ForeignKey('TRANSACTION_FAMILY.uid'))
)

TransactionSQL = sa.Table(
    'TRANSACTION', metadata,
    sa.Column('uid', sa.BigInteger, primary_key=True),
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('name', sa.String),
    sa.Column('value', sa.Float, nullable=False),
    sa.Column('description', sa.String),
    sa.Column('transaction_category_uid', sa.Integer, sa.ForeignKey('TRANSACTION_CATEGORY.uid')),
    sa.Column('account_uid', sa.Integer, sa.ForeignKey('ACCOUNT.uid')),
    sa.Column('user_uid', sa.Integer, sa.ForeignKey('USER.uid'))
)

PermanentTransactionSQL = sa.Table(
    'PERMANENT_TRANSACTION', metadata,
    sa.Column('uid', sa.BigInteger, primary_key=True),
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('frequency', sa.String, nullable=False),
    sa.Column('name', sa.String),
    sa.Column('value', sa.Float, nullable=False),
    sa.Column('description', sa.String),
    sa.Column('transaction_category_uid', sa.Integer, sa.ForeignKey('TRANSACTION_CATEGORY.uid')),
    sa.Column('account_uid', sa.Integer, sa.ForeignKey('ACCOUNT.uid')),
    sa.Column('user_uid', sa.Integer, sa.ForeignKey('USER.uid'))
)