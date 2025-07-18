"""Security analysis API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import persistence, service
from piwardrive.database_service import db_service
from piwardrive.models import ErrorResponse, SuspiciousActivity

router = APIRouter(prefix="/security", tags=["security"])


@router.get(
    "/suspicious",
    response_model=list[SuspiciousActivity],
    responses={401: {"model": ErrorResponse}},
)
async def list_suspicious(
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    offset: int = 0,
    _auth: None = Depends(service._check_auth),
) -> list[SuspiciousActivity]:
    """Return suspicious activity rows."""
    query = (
        "SELECT id, scan_session_id, activity_type, severity, description, ",
        "detected_at, latitude, longitude, analyst_notes FROM suspicious_activities",
    )
    params: list[object] = []
    clauses: list[str] = []
    if start:
        clauses.append("detected_at >= ?")
        params.append(start)
    if end:
        clauses.append("detected_at <= ?")
        params.append(end)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY detected_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = await db_service.fetch(query, *params)
    return [SuspiciousActivity(**row) for row in rows]


@router.post(
    "/suspicious",
    response_model=None,
    responses={401: {"model": ErrorResponse}},
)
async def add_suspicious(
    rec: SuspiciousActivity,
    _auth: None = Depends(service._check_auth),
) -> None:
    """Insert a suspicious activity record."""
    await persistence.save_suspicious_activities([rec.model_dump(exclude_unset=True)])
