# SPDX-FileCopyrightText: 2025-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
"""Drop user.is_active

Revision ID: 30798436c3fe
Revises: ec64f7b42221
Create Date: 2026-08-11 17:09:35.191305

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "30798436c3fe"
down_revision = "ec64f7b42221"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("user", "is_active")


def downgrade() -> None:
    op.add_column(
        "user",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False, server_default=sa.true()),
    )
