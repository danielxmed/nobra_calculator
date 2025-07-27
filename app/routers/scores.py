"""
Router para endpoints relacionados aos scores médicos
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.score_models import (
    CKDEpi2021Request,
    CKDEpi2021Response,
    Cha2ds2VascRequest,
    Cha2ds2VascResponse,
    Curb65Request,
    Curb65Response,
    ScoreListResponse,
    ScoreMetadataResponse,
    ErrorResponse
)
from typing import Dict, Any
from app.services.score_service import score_service
from app.services.calculator_service import calculator_service

router = APIRouter(
    prefix="/api",
    tags=["scores"],
    responses={
        404: {"model": ErrorResponse, "description": "Score não encontrado"},
        422: {"model": ErrorResponse, "description": "Parâmetros inválidos"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"}
    }
)


@router.get("/scores", response_model=ScoreListResponse)
async def list_scores(
    category: Optional[str] = Query(None, description="Filtrar por categoria médica"),
    search: Optional[str] = Query(None, description="Buscar por termo no título ou descrição")
):
    """
    Lista todos os scores médicos disponíveis na API
    
    Args:
        category: Opcional - filtrar por categoria médica
        search: Opcional - buscar por termo no título ou descrição
        
    Returns:
        ScoreListResponse: Lista de scores disponíveis
    """
    try:
        if search:
            # Busca por termo
            scores = score_service.search_scores(search)
        elif category:
            # Filtra por categoria
            scores = score_service.get_scores_by_category(category)
        else:
            # Lista todos os scores
            scores = score_service.get_available_scores()
        
        return ScoreListResponse(
            scores=scores,
            total=len(scores)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro ao listar scores",
                "details": {"error": str(e)}
            }
        )


@router.get("/scores/{score_id}", response_model=ScoreMetadataResponse)
async def get_score_metadata(score_id: str):
    """
    Obtém os metadados completos de um score específico
    
    Args:
        score_id: ID do score
        
    Returns:
        ScoreMetadataResponse: Metadados detalhados do score
    """
    try:
        metadata = score_service.get_score_metadata(score_id)
        
        if metadata is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' não encontrado",
                    "details": {"score_id": score_id}
                }
            )
        
        return metadata
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro ao obter metadados do score",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )


@router.post("/ckd_epi_2021", response_model=CKDEpi2021Response)
async def calculate_ckd_epi_2021(request: CKDEpi2021Request):
    """
    Calcula a Taxa de Filtração Glomerular Estimada usando a equação CKD-EPI 2021
    
    Args:
        request: Parâmetros necessários para o cálculo (sexo, idade, creatinina sérica)
        
    Returns:
        CKDEpi2021Response: Resultado do cálculo com interpretação clínica
    """
    try:
        # Converte o request para dicionário
        parameters = {
            "sex": request.sex.value,  # Enum value
            "age": request.age,
            "serum_creatinine": request.serum_creatinine
        }
        
        # Executa o cálculo
        result = calculator_service.calculate_score("ckd_epi_2021", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Erro no cálculo do CKD-EPI 2021",
                    "details": {"parameters": parameters}
                }
            )
        
        return CKDEpi2021Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Parâmetros inválidos para CKD-EPI 2021",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro interno no cálculo",
                "details": {"error": str(e)}
            }
        )


@router.post("/cha2ds2_vasc", response_model=Cha2ds2VascResponse)
async def calculate_cha2ds2_vasc(request: Cha2ds2VascRequest):
    """
    Calcula o CHA₂DS₂-VASc Score para risco de AVC na fibrilação atrial
    
    Args:
        request: Parâmetros necessários para o cálculo
        
    Returns:
        Cha2ds2VascResponse: Resultado com interpretação clínica e recomendação de anticoagulação
    """
    try:
        # Converte request para dicionário
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "congestive_heart_failure": request.congestive_heart_failure,
            "hypertension": request.hypertension,
            "stroke_tia_thromboembolism": request.stroke_tia_thromboembolism,
            "vascular_disease": request.vascular_disease,
            "diabetes": request.diabetes
        }
        
        # Executa o cálculo
        result = calculator_service.calculate_score("cha2ds2_vasc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Erro no cálculo do CHA₂DS₂-VASc",
                    "details": {"parameters": parameters}
                }
            )
        
        return Cha2ds2VascResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Parâmetros inválidos para CHA₂DS₂-VASc",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro interno no cálculo",
                "details": {"error": str(e)}
            }
        )


@router.post("/curb_65", response_model=Curb65Response)
async def calculate_curb_65(request: Curb65Request):
    """
    Calcula o CURB-65 Score para avaliação de gravidade de pneumonia
    
    Args:
        request: Parâmetros necessários para o cálculo
        
    Returns:
        Curb65Response: Resultado com interpretação clínica e recomendação de tratamento
    """
    try:
        # Converte request para dicionário
        parameters = {
            "confusion": request.confusion,
            "urea": request.urea,
            "respiratory_rate": request.respiratory_rate,
            "systolic_bp": request.systolic_bp,
            "diastolic_bp": request.diastolic_bp,
            "age": request.age
        }
        
        # Executa o cálculo
        result = calculator_service.calculate_score("curb_65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Erro no cálculo do CURB-65",
                    "details": {"parameters": parameters}
                }
            )
        
        return Curb65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Parâmetros inválidos para CURB-65",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro interno no cálculo",
                "details": {"error": str(e)}
            }
        )


@router.post("/{score_id}/calculate")
async def calculate_score_generic(score_id: str, parameters: Dict[str, Any]):
    """
    Endpoint genérico para calcular qualquer score disponível
    
    Args:
        score_id: ID do score a ser calculado
        parameters: Dicionário com os parâmetros necessários para o cálculo
        
    Returns:
        Dict: Resultado do cálculo com interpretação
    """
    try:
        # Verifica se o score existe
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' não encontrado",
                    "details": {"score_id": score_id}
                }
            )
        
        # Verifica se a calculadora está disponível
        if not calculator_service.is_calculator_available(score_id):
            raise HTTPException(
                status_code=501,
                detail={
                    "error": "CalculatorNotImplemented",
                    "message": f"Calculadora para '{score_id}' ainda não implementada",
                    "details": {"score_id": score_id}
                }
            )
        
        # Executa o cálculo
        result = calculator_service.calculate_score(score_id, parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": f"Erro no cálculo do {score_id}",
                    "details": {"parameters": parameters}
                }
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": f"Parâmetros inválidos para {score_id}",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro interno no cálculo",
                "details": {"error": str(e)}
            }
        )


@router.get("/categories")
async def list_categories():
    """
    Lista as categorias médicas disponíveis
    
    Returns:
        Dict: Lista de categorias únicas
    """
    try:
        scores = score_service.get_available_scores()
        categories = list(set(score.category for score in scores))
        categories.sort()
        
        return {
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro ao listar categorias",
                "details": {"error": str(e)}
            }
        )


@router.post("/reload")
async def reload_scores():
    """
    Recarrega todos os scores e calculadoras do sistema
    (Útil para desenvolvimento e atualizações)
    
    Returns:
        Dict: Status da operação de reload
    """
    try:
        # Recarrega scores e calculadoras
        score_service.reload_scores()
        calculator_service.reload_calculators()
        
        # Conta quantos scores foram carregados
        scores = score_service.get_available_scores()
        
        return {
            "status": "success",
            "message": "Scores e calculadoras recarregados com sucesso",
            "scores_loaded": len(scores),
            "scores": [score.id for score in scores]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError", 
                "message": "Erro ao recarregar scores",
                "details": {"error": str(e)}
            }
        )


@router.get("/scores/{score_id}/validate")
async def validate_score_calculator(score_id: str):
    """
    Valida se existe uma calculadora disponível para o score
    
    Args:
        score_id: ID do score
        
    Returns:
        Dict: Status da validação
    """
    try:
        # Verifica se o score existe
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' não encontrado",
                    "details": {"score_id": score_id}
                }
            )
        
        # Verifica se a calculadora está disponível
        calculator_available = calculator_service.is_calculator_available(score_id)
        
        return {
            "score_id": score_id,
            "score_exists": True,
            "calculator_available": calculator_available,
            "status": "ready" if calculator_available else "no_calculator"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Erro ao validar score",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )
