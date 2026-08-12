# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from horizon.commons.dto import Unset
from horizon.commons.schemas.v1.pagination import PaginateQueryV1

MAX_NAME_LENGTH = 2048
MAX_TYPE_LENGTH = 64


class HWMResponseV1(BaseModel):
    """HWM response."""

    id: int = Field(description="HWM id")
    namespace_id: int = Field(description="Namespace id HWM is bound to")
    name: str = Field(description="HWM name, unique in the namespace")
    description: str = Field(description="HWM description")
    type: str = Field(description="HWM type, any non-empty string")
    value: Any = Field(description="HWM value, any JSON serializable value")
    entity: str | None = Field(default=None, description="Name of entity associated with the HWM. Can be any string")
    expression: str | None = Field(
        default=None,
        description="Expression used to calculate HWM value. Can be any string",
    )
    changed_at: datetime = Field(description="Timestamp of last change of the HWM data")
    changed_by: str | None = Field(default=None, description="Latest user who changed the HWM data")

    model_config = ConfigDict(from_attributes=True)


class HWMListResponseV1(BaseModel):
    hwms: list[HWMResponseV1] = Field(description="List of HWMs")


class HWMPaginateQueryV1(PaginateQueryV1):
    """Query params for HWM pagination request."""

    namespace_id: int = Field(description="Namespace id HWM is bound to")
    name: str | None = Field(default=None, min_length=1, max_length=MAX_NAME_LENGTH, description="Search query")

    # more arguments can be added in future


class HWMCreateRequestV1(BaseModel):
    """Request body for HWM create request."""

    namespace_id: int = Field(description="Namespace id HWM is bound to")
    name: str = Field(min_length=1, max_length=MAX_NAME_LENGTH, description="HWM name, unique in the namespace")
    description: str = Field(default="", description="HWM description")
    type: str = Field(min_length=1, max_length=MAX_TYPE_LENGTH, description="HWM type, any non-empty string")
    value: Any = Field(description="HWM value, any JSON serializable value")
    entity: str | None = Field(default=None, description="Name of entity associated with the HWM. Can be any string")
    expression: str | None = Field(
        default=None,
        description="Expression used to calculate HWM value. Can be any string",
    )


class HWMUpdateRequestV1(BaseModel):
    """Request body for HWM update request.

    If field value is not set, it will not be updated.
    """

    name: str = Field(default=Unset(), min_length=1, max_length=MAX_NAME_LENGTH, description="New HWM name")  # type: ignore[assignment]
    description: str = Field(default=Unset(), description="New HWM description")  # type: ignore[assignment]
    type: str = Field(default=Unset(), min_length=1, max_length=MAX_TYPE_LENGTH, description="New HWM type")  # type: ignore[assignment]
    value: Any = Field(default=Unset(), description="New HWM value")  # type: ignore[assignment]
    entity: str | None = Field(
        default=Unset(), description="New name of entity associated with the HWM. Can be any string"
    )  # type: ignore[assignment]
    expression: str | None = Field(
        default=Unset(), description="New expression used to calculate HWM value. Can be any string"
    )  # type: ignore[assignment]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def _any_field_set(self):
        """Validate that at least one field is set."""
        if not any(not isinstance(v, Unset) for v in self.model_dump(warnings=False).values()):
            msg = "At least one field must be set."
            raise ValueError(msg)
        return self


class HWMBulkCopyRequestV1(BaseModel):
    """Schema for request body of HWM copy operation."""

    source_namespace_id: int = Field(description="Source namespace ID from which HWMs are copied")
    target_namespace_id: int = Field(description="Target namespace ID to which HWMs are copied")
    hwm_ids: list[int] = Field(description="List of HWM IDs to be copied")
    with_history: bool = Field(default=False, description="Whether to copy HWM history")

    @field_validator("hwm_ids", mode="before")
    @classmethod
    def _check_hwm_ids_not_empty(cls, v):
        if not len(v):
            msg = "List should have at least 1 item after validation, not 0"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def _check_namespace_ids(self):
        """Validator to ensure source and target namespace IDs are different."""
        if self.source_namespace_id == self.target_namespace_id:
            msg = "Source and target namespace IDs must not be the same."
            raise ValueError(msg)
        return self


class HWMBulkDeleteRequestV1(BaseModel):
    """Schema for request body of bulk delete HWM operation."""

    namespace_id: int = Field(description="Namespace ID where the HWMs belong")
    hwm_ids: list[int] = Field(description="List of HWM IDs to be copied")

    @field_validator("hwm_ids", mode="before")
    @classmethod
    def _check_hwm_ids_not_empty(cls, v):
        if not len(v):
            msg = "List should have at least 1 item after validation, not 0"
            raise ValueError(msg)
        return v
