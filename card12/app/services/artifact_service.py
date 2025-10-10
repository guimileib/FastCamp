from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
from loguru import logger

from app.models.artifact import Artifact, ArtifactVersion, ArtifactResponse

class ArtifactService:    
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
    
    def _get_artifact_key(self, session_id: str, artifact_name: str) -> str:
        return f"{session_id}:{artifact_name}"
    
    def create_or_update_artifact(
        self,
        session_id: str,
        user_id: str,
        app_name: str,
        artifact_name: str,
        content: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> Artifact:
        key = self._get_artifact_key(session_id, artifact_name)
        version_id = str(uuid.uuid4())
        
        version = ArtifactVersion(
            version_id=version_id,
            artifact_name=artifact_name,
            session_id=session_id,
            content=content,
            metadata=metadata
        )
        
        if key in self.artifacts:
            artifact = self.artifacts[key]
            artifact.versions.append(version)
            artifact.current_version = version_id
            artifact.updated_at = datetime.utcnow()
            logger.info(f"Artifact atualizado: {artifact_name} (versão {version_id})")
        else:
            artifact = Artifact(
                artifact_name=artifact_name,
                session_id=session_id,
                user_id=user_id,
                app_name=app_name,
                current_version=version_id,
                versions=[version],
                metadata=metadata
            )
            self.artifacts[key] = artifact
            logger.info(f"Artifact criado: {artifact_name}")
        
        return artifact
    
    def get_artifact(
        self,
        session_id: str,
        artifact_name: str,
        version_id: Optional[str] = None
    ) -> Optional[ArtifactVersion]:
        key = self._get_artifact_key(session_id, artifact_name)
        artifact = self.artifacts.get(key)
        
        if not artifact:
            return None
        
        if version_id:
            for version in artifact.versions:
                if version.version_id == version_id:
                    return version
            return None
        else:
            for version in artifact.versions:
                if version.version_id == artifact.current_version:
                    return version
            return artifact.versions[-1] if artifact.versions else None
    
    def list_artifacts(self, session_id: str) -> List[str]:
        artifacts = [
            artifact.artifact_name
            for artifact in self.artifacts.values()
            if artifact.session_id == session_id
        ]
        return artifacts
    
    def list_artifact_versions(
        self,
        session_id: str,
        artifact_name: str
    ) -> List[str]:
        key = self._get_artifact_key(session_id, artifact_name)
        artifact = self.artifacts.get(key)
        
        if not artifact:
            return []
        
        return [v.version_id for v in artifact.versions]
    
    def delete_artifact(
        self,
        session_id: str,
        artifact_name: str
    ) -> bool:
        key = self._get_artifact_key(session_id, artifact_name)
        
        if key in self.artifacts:
            del self.artifacts[key]
            logger.info(f"Artifact deletado: {artifact_name} da sessão {session_id}")
            return True
        
        return False
    
    def get_artifact_info(
        self,
        session_id: str,
        artifact_name: str
    ) -> Optional[ArtifactResponse]:
        key = self._get_artifact_key(session_id, artifact_name)
        artifact = self.artifacts.get(key)
        
        if not artifact:
            return None
        
        return ArtifactResponse(
            artifact_name=artifact.artifact_name,
            current_version=artifact.current_version,
            created_at=artifact.created_at,
            updated_at=artifact.updated_at,
            version_count=len(artifact.versions),
            metadata=artifact.metadata
        )

artifact_service = ArtifactService()
