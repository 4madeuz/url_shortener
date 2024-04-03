"""Initial migration

Revision ID: 0cff8991adb5
Revises: 
Create Date: 2024-04-02 14:36:58.587595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cff8991adb5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('original_url', sa.String(), nullable=True),
    sa.Column('short_url', sa.String(), nullable=True),
    sa.Column('timestamps', sa.ARRAY(sa.DateTime()), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###