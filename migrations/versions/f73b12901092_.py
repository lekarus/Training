"""empty message

Revision ID: f73b12901092
Revises: cca51b000ba1
Create Date: 2023-04-25 12:43:38.229651

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f73b12901092'
down_revision = 'cca51b000ba1'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sub_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', postgresql.ENUM('pending', 'successfully', 'failure', name='payment_status_enum'), nullable=True))

    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('api_key', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('link', sa.String(length=128), nullable=True))
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.drop_column('link')
        batch_op.drop_column('api_key')

    with op.batch_alter_table('sub_user', schema=None) as batch_op:
        batch_op.drop_column('payment_status')

    # ### end Alembic commands ###

