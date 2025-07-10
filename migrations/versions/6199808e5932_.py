"""empty message

Revision ID: 6199808e5932
Revises: 
Create Date: 2019-03-26 10:27:46.536745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6199808e5932"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "release",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(length=10), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "release_file",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=100), nullable=True),
        sa.Column("release_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["release_id"], ["release.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("release_file")
    op.drop_table("release")
    op.drop_table("project")
