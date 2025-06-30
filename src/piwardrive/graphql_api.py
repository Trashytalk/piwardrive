from __future__ import annotations

import inspect
import json
from dataclasses import asdict

import graphene
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from graphene import ResolveInfo
from graphene.types.generic import GenericScalar

from .core import config, persistence


class HealthRecordType(graphene.ObjectType):
    timestamp = graphene.String()
    cpu_temp = graphene.Float()
    cpu_percent = graphene.Float()
    memory_percent = graphene.Float()
    disk_percent = graphene.Float()


class Query(graphene.ObjectType):
    status = graphene.List(HealthRecordType, limit=graphene.Int(default_value=5))
    config = GenericScalar()

    async def resolve_status(self, info: ResolveInfo, limit: int = 5):
        recs = persistence.load_recent_health(limit)
        if inspect.isawaitable(recs):
            recs = await recs
        return [HealthRecordType(**asdict(r)) for r in recs]

    async def resolve_config(self, info: ResolveInfo):
        cfg = config.load_config()
        return asdict(cfg)


schema = graphene.Schema(query=Query)


def add_graphql_route(app: FastAPI, path: str = "/graphql") -> None:
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
