"""
Service to manage medical score metadata
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.models.score_models import ScoreInfo, ScoreMetadataResponse


class ScoreService:
    """Service to manage medical scores"""
    
    def __init__(self, scores_directory: str = "scores"):
        """
        Initializes the scores service
        
        Args:
            scores_directory (str): Directory containing the score JSON files
        """
        self.scores_directory = Path(scores_directory)
        self._scores_cache: Dict[str, Dict[str, Any]] = {}
        self._load_scores()
    
    def _load_scores(self):
        """Loads all scores from the directory"""
        if not self.scores_directory.exists():
            raise FileNotFoundError(f"Scores directory not found: {self.scores_directory}")
        
        self._scores_cache = {}
        
        # Search for JSON files in the directory
        for json_file in self.scores_directory.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    score_data = json.load(f)
                    
                # Validate if the JSON has the required fields
                if not self._validate_score_json(score_data):
                    print(f"Warning: Invalid score found in {json_file}")
                    continue
                
                score_id = score_data.get("id")
                self._scores_cache[score_id] = score_data
                
            except json.JSONDecodeError as e:
                print(f"Error loading JSON {json_file}: {e}")
            except Exception as e:
                print(f"Unexpected error loading {json_file}: {e}")
    
    def _validate_score_json(self, score_data: Dict[str, Any]) -> bool:
        """
        Validates if a score JSON has the minimum required structure
        
        Args:
            score_data (dict): Score data loaded from JSON
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ["id", "title", "description", "category", "parameters", "result"]
        
        for field in required_fields:
            if field not in score_data:
                return False
        
        # Validate if parameters is a list
        if not isinstance(score_data.get("parameters"), list):
            return False
        
        # Validate if result is a dict with necessary fields
        result = score_data.get("result", {})
        if not isinstance(result, dict) or "name" not in result or "unit" not in result:
            return False
        
        return True
    
    def get_available_scores(self) -> List[ScoreInfo]:
        """
        Returns the list of available scores
        
        Returns:
            List[ScoreInfo]: List with basic score information
        """
        scores = []
        
        for score_id, score_data in self._scores_cache.items():
            score_info = ScoreInfo(
                id=score_data["id"],
                title=score_data["title"],
                description=score_data["description"],
                category=score_data["category"],
                version=score_data.get("version")
            )
            scores.append(score_info)
        
        return scores
    
    def get_score_metadata(self, score_id: str) -> Optional[ScoreMetadataResponse]:
        """
        Returns the complete metadata of a specific score
        
        Args:
            score_id (str): ID of the score
            
        Returns:
            Optional[ScoreMetadataResponse]: Score metadata or None if not found
        """
        if score_id not in self._scores_cache:
            return None
        
        score_data = self._scores_cache[score_id]
        
        try:
            # Convert data to Pydantic model
            metadata = ScoreMetadataResponse(**score_data)
            return metadata
        except Exception as e:
            print(f"Error converting score metadata {score_id}: {e}")
            return None
    
    def score_exists(self, score_id: str) -> bool:
        """
        Checks if a score exists
        
        Args:
            score_id (str): ID of the score
            
        Returns:
            bool: True if the score exists, False otherwise
        """
        return score_id in self._scores_cache
    
    def get_score_raw_data(self, score_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns the raw data of a score
        
        Args:
            score_id (str): ID of the score
            
        Returns:
            Optional[Dict]: Raw score data or None if not found
        """
        return self._scores_cache.get(score_id)
    
    def reload_scores(self):
        """Reloads all scores from the directory"""
        self._load_scores()
    
    def get_scores_by_category(self, category: str) -> List[ScoreInfo]:
        """
        Returns scores filtered by category
        
        Args:
            category (str): Medical category
            
        Returns:
            List[ScoreInfo]: List of scores in the specified category
        """
        scores = []
        
        for score_id, score_data in self._scores_cache.items():
            if score_data.get("category", "").lower() == category.lower():
                score_info = ScoreInfo(
                    id=score_data["id"],
                    title=score_data["title"],
                    description=score_data["description"],
                    category=score_data["category"],
                    version=score_data.get("version")
                )
                scores.append(score_info)
        
        return scores
    
    def search_scores(self, query: str) -> List[ScoreInfo]:
        """
        Searches for scores by text in title or description
        
        Args:
            query (str): Search term
            
        Returns:
            List[ScoreInfo]: List of scores matching the search
        """
        query_lower = query.lower()
        scores = []
        
        for score_id, score_data in self._scores_cache.items():
            title = score_data.get("title", "").lower()
            description = score_data.get("description", "").lower()
            
            if query_lower in title or query_lower in description:
                score_info = ScoreInfo(
                    id=score_data["id"],
                    title=score_data["title"],
                    description=score_data["description"],
                    category=score_data["category"],
                    version=score_data.get("version")
                )
                scores.append(score_info)
        
        return scores


# Global service instance
score_service = ScoreService()
