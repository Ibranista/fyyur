from alembic import op
import sqlalchemy as sa


revision = "8b2cae42b84d"
down_revision = "30aed9d5b40b"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column("artists", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("venues", sa.Column("created_at", sa.DateTime(), nullable=True))


def downgrade():

    op.drop_column("venues", "created_at")
    op.drop_column("artists", "created_at")
