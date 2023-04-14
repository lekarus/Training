"""empty message

Revision ID: 6a8f74bbed3b
Revises: c2f183d22aea
Create Date: 2023-04-14 19:16:50.463699

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a8f74bbed3b'
down_revision = 'c2f183d22aea'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    with op.batch_alter_table('subscription', schema=None) as batch_op:
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

    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('from', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('type', postgresql.ENUM('subscription', 'for_all', 'direct', name='notification_type_enum'), autoincrement=False, nullable=False),
    sa.Column('subscription', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['from'], ['trainer.id'], name='notification_from_fkey'),
    sa.ForeignKeyConstraint(['subscription'], ['subscription.id'], name='notification_subscription_fkey'),
    sa.PrimaryKeyConstraint('id', name='notification_pkey')
    )
    # ### end Alembic commands ###

