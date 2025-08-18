"""create member_bank_accounts table

Revision ID: ba3d8fe753a3
Revises: 51e9d2942d1e
Create Date: 2025-08-18 11:51:42.979783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER


# revision identifiers, used by Alembic.
revision: str = 'ba3d8fe753a3'
down_revision: Union[str, None] = '51e9d2942d1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "member_bank_accounts",
        sa.Column("id", INTEGER(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column("member_id", INTEGER(unsigned=True), sa.ForeignKey("members.id"), nullable=False, index=True),
        sa.Column("bank_holder_name", sa.String(255), nullable=False),
        sa.Column("branch", sa.String(255), nullable=False),
        sa.Column("ifsc_code", sa.String(50), nullable=True),
        sa.Column("swift_code", sa.String(50), nullable=True),
        sa.Column("account_number", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("member_bank_accounts")
