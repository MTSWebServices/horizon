# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from pydantic import BaseModel, Field


class AuthTokenResponseV1(BaseModel):
    """Authorization response."""

    access_token: str = Field(description="Access token")
    token_type: str = Field(description="Token type")
    expires_at: float = Field(description="Token expiration time, in seconds")
