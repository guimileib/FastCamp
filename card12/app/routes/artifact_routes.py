from fastapi import APIRouter, HTTPException, Path, Body, Query
from typing import Optional

from app.models.artifact import ArtifactCreate, ArtifactResponse, ArtifactList, ArtifactVersion
from app.services.artifact_service import artifact_service

router = APIRouter()


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
    response_model=ArtifactVersion
)
async def get_artifact(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str,
    version_id: Optional[str] = Query(None, description="ID da versão específica")
):
    artifact = artifact_service.get_artifact(session_id, artifact_name, version_id)
    
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact não encontrado")
    
    return artifact


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions/{version_id}",
    response_model=ArtifactVersion
)
async def get_artifact_version(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str,
    version_id: str
):
    artifact = artifact_service.get_artifact(session_id, artifact_name, version_id)
    
    if not artifact:
        raise HTTPException(status_code=404, detail="Versão do artifact não encontrada")
    
    return artifact


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts",
    response_model=ArtifactList
)
async def list_artifacts(
    app_name: str,
    user_id: str,
    session_id: str
):
    artifacts = artifact_service.list_artifacts(session_id)
    
    return ArtifactList(artifacts=artifacts, total=len(artifacts))


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions"
)
async def list_artifact_versions(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str
):
    """Lista todas as versões de um artifact"""
    versions = artifact_service.list_artifact_versions(session_id, artifact_name)
    
    return {"artifact_name": artifact_name, "versions": versions, "total": len(versions)}


@router.delete(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}",
    status_code=204
)
async def delete_artifact(
    app_name: str,
    user_id: str,
    session_id: str,
    artifact_name: str
):
    success = artifact_service.delete_artifact(session_id, artifact_name)
    
    if not success:
        raise HTTPException(status_code=404, detail="Artifact não encontrado")
    
    return None
