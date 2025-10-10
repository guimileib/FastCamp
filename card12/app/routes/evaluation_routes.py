"""
Rotas de evaluation sets e métricas
"""

from fastapi import APIRouter, HTTPException, Path, Body
from typing import List, Dict, Any
import uuid
from datetime import datetime

from app.models.evaluation import (
    EvalSetCreate, EvalSet, EvalCase, AddSessionToEvalSet,
    EvalRunRequest, EvalResult, EvalCaseResult
)

router = APIRouter()

eval_sets_storage: Dict[str, EvalSet] = {}
eval_results_storage: Dict[str, EvalResult] = {}


@router.post("/apps/{app_name}/eval_sets/{eval_set_id}", status_code=201)
async def create_eval_set(
    app_name: str,
    eval_set_id: str,
    eval_set_data: EvalSetCreate = Body(...)
):
    
    if eval_set_id in eval_sets_storage:
        raise HTTPException(status_code=400, detail="Evaluation set já existe")
    
    eval_set = EvalSet(
        eval_set_id=eval_set_id,
        app_name=app_name,
        description=eval_set_data.description,
        metadata=eval_set_data.metadata
    )
    
    eval_sets_storage[eval_set_id] = eval_set
    
    return {"message": "Evaluation set criado com sucesso", "eval_set_id": eval_set_id}


@router.get("/apps/{app_name}/eval_sets")
async def list_eval_sets(app_name: str):
    
    app_eval_sets = [
        {
            "eval_set_id": es.eval_set_id,
            "description": es.description,
            "case_count": len(es.cases),
            "created_at": es.created_at,
            "updated_at": es.updated_at
        }
        for es in eval_sets_storage.values()
        if es.app_name == app_name
    ]
    
    return {"eval_sets": app_eval_sets, "total": len(app_eval_sets)}


@router.post("/apps/{app_name}/eval_sets/{eval_set_id}/add_session")
async def add_session_to_eval_set(
    app_name: str,
    eval_set_id: str,
    data: AddSessionToEvalSet = Body(...)
):
    
    eval_set = eval_sets_storage.get(eval_set_id)
    
    if not eval_set:
        raise HTTPException(status_code=404, detail="Evaluation set não encontrado")
    
    case_id = str(uuid.uuid4())
    eval_case = EvalCase(
        case_id=case_id,
        input_data={"session_id": data.session_id},
        expected_output=data.expected_output,
        metadata=data.metadata
    )
    
    eval_set.cases.append(eval_case)
    eval_set.updated_at = datetime.utcnow()
    
    return {
        "message": "Sessão adicionada ao evaluation set",
        "case_id": case_id,
        "eval_set_id": eval_set_id
    }


@router.get("/apps/{app_name}/eval_sets/{eval_set_id}/evals")
async def list_eval_cases(app_name: str, eval_set_id: str):
    """Lista todos os casos de avaliação em um evaluation set"""
    
    eval_set = eval_sets_storage.get(eval_set_id)
    
    if not eval_set:
        raise HTTPException(status_code=404, detail="Evaluation set não encontrado")
    
    return {
        "eval_set_id": eval_set_id,
        "cases": [
            {
                "case_id": case.case_id,
                "created_at": case.created_at,
                "has_expected_output": case.expected_output is not None
            }
            for case in eval_set.cases
        ],
        "total": len(eval_set.cases)
    }


@router.post("/apps/{app_name}/eval_sets/{eval_set_id}/run_eval")
async def run_evaluation(
    app_name: str,
    eval_set_id: str,
    eval_request: EvalRunRequest = Body(...)
):
    """Executa avaliações para casos especificados"""
    
    eval_set = eval_sets_storage.get(eval_set_id)
    
    if not eval_set:
        raise HTTPException(status_code=404, detail="Evaluation set não encontrado")
    
    # Determina quais casos avaliar
    cases_to_eval = eval_set.cases
    if eval_request.case_ids:
        cases_to_eval = [c for c in eval_set.cases if c.case_id in eval_request.case_ids]
    
    # Executa avaliações (simulação)
    case_results = []
    for case in cases_to_eval:
        # Aqui você executaria o agente e aplicaria as métricas
        case_result = EvalCaseResult(
            case_id=case.case_id,
            actual_output={"result": "simulado"},
            metrics={metric.metric_name: 0.85 for metric in eval_request.metrics},
            passed=True
        )
        case_results.append(case_result)
    
    # Cria resultado da avaliação
    eval_result_id = str(uuid.uuid4())
    eval_result = EvalResult(
        eval_result_id=eval_result_id,
        eval_set_id=eval_set_id,
        app_name=app_name,
        case_results=case_results,
        summary={
            "total_cases": len(case_results),
            "passed": len([r for r in case_results if r.passed]),
            "failed": len([r for r in case_results if not r.passed]),
            "average_score": 0.85
        },
        metadata=eval_request.metadata
    )
    
    eval_results_storage[eval_result_id] = eval_result
    
    return {
        "message": "Avaliação executada com sucesso",
        "eval_result_id": eval_result_id,
        "summary": eval_result.summary
    }


@router.get("/apps/{app_name}/eval_results/{eval_result_id}")
async def get_eval_result(app_name: str, eval_result_id: str):
    """Recupera resultados de uma avaliação específica"""
    
    eval_result = eval_results_storage.get(eval_result_id)
    
    if not eval_result:
        raise HTTPException(status_code=404, detail="Resultado de avaliação não encontrado")
    
    return eval_result


@router.get("/apps/{app_name}/eval_results")
async def list_eval_results(app_name: str):
    """Lista todos os resultados de avaliação de uma aplicação"""
    
    app_results = [
        {
            "eval_result_id": er.eval_result_id,
            "eval_set_id": er.eval_set_id,
            "created_at": er.created_at,
            "summary": er.summary
        }
        for er in eval_results_storage.values()
        if er.app_name == app_name
    ]
    
    return {"results": app_results, "total": len(app_results)}
