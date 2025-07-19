import sqlalchemy as sa
from src.database import metadata

transaction = sa.Table(
    "transaction",
    metadata,
    sa.Column("id_transaction", sa.Integer, primary_key=True, unique=True),
    sa.Column("id_account", sa.Integer, sa.ForeignKey("account.id_account"), nullable=False),
    sa.Column("type", sa.String, nullable=False),
    sa.Column("value", sa.Float, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False),
)
