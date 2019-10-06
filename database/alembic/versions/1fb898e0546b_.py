"""empty message

Revision ID: 1fb898e0546b
Revises: 5b5b56d946c3
Create Date: 2019-10-06 18:50:55.389555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb898e0546b'
down_revision = '5b5b56d946c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.create_table('files',
                    sa.Column('id', sa.String(length=40), nullable=False),
                    sa.Column('filename', sa.String(length=50), nullable=True),
                    sa.Column('content_type', sa.String(length=50), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###