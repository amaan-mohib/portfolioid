"""renew table

Revision ID: f197765e8709
Revises: 
Create Date: 2020-05-14 21:51:10.929373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f197765e8709'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('thumb', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_templates_name'), 'portfolio_templates', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('admin_role', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('img', sa.String(length=128), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('temp', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_first_name'), 'profile', ['first_name'], unique=False)
    op.create_index(op.f('ix_profile_timestamp'), 'profile', ['timestamp'], unique=False)
    op.create_table('social_links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fb', sa.String(length=128), nullable=True),
    sa.Column('insta', sa.String(length=128), nullable=True),
    sa.Column('linkedIn', sa.String(length=128), nullable=True),
    sa.Column('github', sa.String(length=128), nullable=True),
    sa.Column('twitter', sa.String(length=128), nullable=True),
    sa.Column('yt', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_social_links_fb'), 'social_links', ['fb'], unique=True)
    op.create_index(op.f('ix_social_links_github'), 'social_links', ['github'], unique=True)
    op.create_index(op.f('ix_social_links_insta'), 'social_links', ['insta'], unique=True)
    op.create_index(op.f('ix_social_links_linkedIn'), 'social_links', ['linkedIn'], unique=True)
    op.create_index(op.f('ix_social_links_twitter'), 'social_links', ['twitter'], unique=True)
    op.create_index(op.f('ix_social_links_yt'), 'social_links', ['yt'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_social_links_yt'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_twitter'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_linkedIn'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_insta'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_github'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_fb'), table_name='social_links')
    op.drop_table('social_links')
    op.drop_index(op.f('ix_profile_timestamp'), table_name='profile')
    op.drop_index(op.f('ix_profile_first_name'), table_name='profile')
    op.drop_table('profile')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_portfolio_templates_name'), table_name='portfolio_templates')
    op.drop_table('portfolio_templates')
    # ### end Alembic commands ###
