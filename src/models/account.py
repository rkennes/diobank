import sqlalchemy as sa
from src.database import metadata

account = sa.Table(
    "account",
    metadata,
    sa.Column("id_account", sa.Integer, primary_key=True, unique=True),
    sa.Column("owner", sa.String, nullable=False),
    sa.Column("balance", sa.Float, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False),
)
