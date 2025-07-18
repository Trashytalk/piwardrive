"""GraphQL API implementation for PiWardrive.

This module provides a GraphQL interface for querying system status and
configuration data. It includes health record queries and configuration
access through a FastAPI-integrated GraphQL endpoint.
"""

from __future__ import annotations

import inspect
from dataclasses import asdict

import graphene
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from graphene import ResolveInfo
from graphene.types.generic import GenericScalar

from .core import config, persistence


class HealthRecordType(graphene.ObjectType):
    """GraphQL type representing a health monitoring record."""

    timestamp = graphene.String()
    cpu_temp = graphene.Float()
    cpu_percent = graphene.Float()
    memory_percent = graphene.Float()
    disk_percent = graphene.Float()


class Query(graphene.ObjectType):
    """Root GraphQL query class providing access to system data."""

    status = graphene.List(HealthRecordType, limit=graphene.Int(default_value=5))
    _config = GenericScalar()

    async def resolve_status(self, info: ResolveInfo, limit: int = 5):
        """Resolve health status records.

        Args:
            info: GraphQL resolve info.
            limit: Maximum number of records to return.

        Returns:
            List of health record objects.
        """
        recs = persistence.load_recent_health(limit)
        if inspect.isawaitable(recs):
            recs = await recs
        return [HealthRecordType(**asdict(r)) for r in recs]

    async def resolve_config(self, info: ResolveInfo):
        """Resolve system configuration.

        Args:
            info: GraphQL resolve info.

        Returns:
            System configuration as a dictionary.
        """
        cfg = config.load_config()
        return asdict(cfg)


schema = graphene.Schema(query=Query)


def add_graphql_route(app: FastAPI, path: str = "/graphql") -> None:
    """Add a GraphQL endpoint to a FastAPI application.

    Args:
        app: The FastAPI application instance.
        path: The URL path for the GraphQL endpoint.
    """

    async def handle(request: Request) -> JSONResponse:
        if request.method == "GET":
            q = request.query_params.get("query") or ""
            variables = None
        else:
            data = await request.json()
            q = data.get("query", "")
            variables = data.get("variables")
        result = await schema.execute_async(q, variable_values=variables)
        status = 200
        if result.errors:
            status = 400
        return JSONResponse(result.to_dict(), status_code=status)

    app.add_api_route(path, handle, methods=["GET", "POST"])
