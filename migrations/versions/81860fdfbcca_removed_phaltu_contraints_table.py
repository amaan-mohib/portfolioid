"""removed phaltu contraints table

Revision ID: 81860fdfbcca
Revises: f197765e8709
Create Date: 2020-05-16 13:03:17.394900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81860fdfbcca'
down_revision = 'f197765e8709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_social_links_fb', table_name='social_links')
    op.create_index(op.f('ix_social_links_fb'), 'social_links', ['fb'], unique=False)
    op.drop_index('ix_social_links_github', table_name='social_links')
    op.create_index(op.f('ix_social_links_github'), 'social_links', ['github'], unique=False)
    op.drop_index('ix_social_links_insta', table_name='social_links')
    op.create_index(op.f('ix_social_links_insta'), 'social_links', ['insta'], unique=False)
    op.drop_index('ix_social_links_linkedIn', table_name='social_links')
    op.create_index(op.f('ix_social_links_linkedIn'), 'social_links', ['linkedIn'], unique=False)
    op.drop_index('ix_social_links_twitter', table_name='social_links')
    op.create_index(op.f('ix_social_links_twitter'), 'social_links', ['twitter'], unique=False)
    op.drop_index('ix_social_links_yt', table_name='social_links')
    op.create_index(op.f('ix_social_links_yt'), 'social_links', ['yt'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_social_links_yt'), table_name='social_links')
    op.create_index('ix_social_links_yt', 'social_links', ['yt'], unique=1)
    op.drop_index(op.f('ix_social_links_twitter'), table_name='social_links')
    op.create_index('ix_social_links_twitter', 'social_links', ['twitter'], unique=1)
    op.drop_index(op.f('ix_social_links_linkedIn'), table_name='social_links')
    op.create_index('ix_social_links_linkedIn', 'social_links', ['linkedIn'], unique=1)
    op.drop_index(op.f('ix_social_links_insta'), table_name='social_links')
    op.create_index('ix_social_links_insta', 'social_links', ['insta'], unique=1)
    op.drop_index(op.f('ix_social_links_github'), table_name='social_links')
    op.create_index('ix_social_links_github', 'social_links', ['github'], unique=1)
    op.drop_index(op.f('ix_social_links_fb'), table_name='social_links')
    op.create_index('ix_social_links_fb', 'social_links', ['fb'], unique=1)
    # ### end Alembic commands ###
