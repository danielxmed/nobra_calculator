"""
Main API routes for frontend integration
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.score_service import score_service
from app.services.calculator_service import calculator_service

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

@router.get("/scores")
async def list_scores(
    category: Optional[str] = Query(None, description="Filter by medical specialty"),
    search: Optional[str] = Query(None, description="Search scores by keywords")
):
    """
    List all available medical scores and calculators
    
    Args:
        category: Filter by medical specialty (optional)
        search: Search by keywords (optional)
    
    Returns:
        Dict: List of available scores with metadata
    """
    try:
        if search:
            scores = score_service.search_scores(search)
        elif category:
            scores = score_service.get_scores_by_category(category)
        else:
            scores = score_service.get_available_scores()
        
        return {
            "scores": [
                {
                    "id": score.id,
                    "title": score.title,
                    "description": score.description,
                    "category": score.category,
                    "version": score.version
                } for score in scores
            ],
            "total": len(scores)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing scores",
                "details": {"error": str(e)}
            }
        )

@router.get("/scores/{score_id}")
async def get_score_metadata(score_id: str):
    """
    Get comprehensive metadata for a specific medical score
    
    Args:
        score_id: ID of the score
        
    Returns:
        Dict: Complete score metadata including parameters and interpretation
    """
    try:
        metadata = score_service.get_score_metadata(score_id)
        
        if metadata is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
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
                "message": "Error getting score metadata",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )

@router.post("/reload")
async def reload_scores():
    """
    Reload all scores and calculators in the system
    
    Returns:
        Dict: Status of the reload operation
    """
    try:
        # Reload scores and calculators
        score_service.reload_scores()
        calculator_service.reload_calculators()
        
        # Count how many scores were loaded
        scores = score_service.get_available_scores()
        
        return {
            "status": "success",
            "message": "Scores and calculators reloaded successfully",
            "scores_loaded": len(scores),
            "scores": [score.id for score in scores]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError", 
                "message": "Error reloading scores",
                "details": {"error": str(e)}
            }
        )

@router.get("/categories")
async def list_categories():
    """
    List all available medical categories
    
    Returns:
        Dict: List of unique categories
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
                "message": "Error listing categories",
                "details": {"error": str(e)}
            }
        )