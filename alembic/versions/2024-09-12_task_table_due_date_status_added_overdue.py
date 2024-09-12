"""task table due_date, status added overdue

Revision ID: e96219e2cfbd
Revises: 6f6937b92dfc
Create Date: 2024-09-12 01:51:15.519381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e96219e2cfbd'
down_revision: Union[str, None] = '6f6937b92dfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'due_date')
    # ### end Alembic commands ###
