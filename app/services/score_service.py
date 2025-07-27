"""
Serviço para gerenciar metadados dos scores médicos
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.models.score_models import ScoreInfo, ScoreMetadataResponse


class ScoreService:
    """Serviço para gerenciar scores médicos"""
    
    def __init__(self, scores_directory: str = "scores"):
        """
        Inicializa o serviço de scores
        
        Args:
            scores_directory (str): Diretório contendo os arquivos JSON dos scores
        """
        self.scores_directory = Path(scores_directory)
        self._scores_cache: Dict[str, Dict[str, Any]] = {}
        self._load_scores()
    
    def _load_scores(self):
        """Carrega todos os scores do diretório"""
        if not self.scores_directory.exists():
            raise FileNotFoundError(f"Diretório de scores não encontrado: {self.scores_directory}")
        
        self._scores_cache = {}
        
        # Procura por arquivos JSON no diretório
        for json_file in self.scores_directory.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    score_data = json.load(f)
                    
                # Valida se o JSON tem os campos obrigatórios
                if not self._validate_score_json(score_data):
                    print(f"Aviso: Score inválido encontrado em {json_file}")
                    continue
                
                score_id = score_data.get("id")
                self._scores_cache[score_id] = score_data
                
            except json.JSONDecodeError as e:
                print(f"Erro ao carregar JSON {json_file}: {e}")
            except Exception as e:
                print(f"Erro inesperado ao carregar {json_file}: {e}")
    
    def _validate_score_json(self, score_data: Dict[str, Any]) -> bool:
        """
        Valida se um JSON de score tem a estrutura mínima necessária
        
        Args:
            score_data (dict): Dados do score carregados do JSON
            
        Returns:
            bool: True se válido, False caso contrário
        """
        required_fields = ["id", "title", "description", "category", "parameters", "result"]
        
        for field in required_fields:
            if field not in score_data:
                return False
        
        # Valida se parameters é uma lista
        if not isinstance(score_data.get("parameters"), list):
            return False
        
        # Valida se result é um dict com campos necessários
        result = score_data.get("result", {})
        if not isinstance(result, dict) or "name" not in result or "unit" not in result:
            return False
        
        return True
    
    def get_available_scores(self) -> List[ScoreInfo]:
        """
        Retorna a lista de scores disponíveis
        
        Returns:
            List[ScoreInfo]: Lista com informações básicas dos scores
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
        Retorna os metadados completos de um score específico
        
        Args:
            score_id (str): ID do score
            
        Returns:
            Optional[ScoreMetadataResponse]: Metadados do score ou None se não encontrado
        """
        if score_id not in self._scores_cache:
            return None
        
        score_data = self._scores_cache[score_id]
        
        try:
            # Converter os dados para o modelo Pydantic
            metadata = ScoreMetadataResponse(**score_data)
            return metadata
        except Exception as e:
            print(f"Erro ao converter metadados do score {score_id}: {e}")
            return None
    
    def score_exists(self, score_id: str) -> bool:
        """
        Verifica se um score existe
        
        Args:
            score_id (str): ID do score
            
        Returns:
            bool: True se o score existe, False caso contrário
        """
        return score_id in self._scores_cache
    
    def get_score_raw_data(self, score_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados brutos de um score
        
        Args:
            score_id (str): ID do score
            
        Returns:
            Optional[Dict]: Dados brutos do score ou None se não encontrado
        """
        return self._scores_cache.get(score_id)
    
    def reload_scores(self):
        """Recarrega todos os scores do diretório"""
        self._load_scores()
    
    def get_scores_by_category(self, category: str) -> List[ScoreInfo]:
        """
        Retorna scores filtrados por categoria
        
        Args:
            category (str): Categoria médica
            
        Returns:
            List[ScoreInfo]: Lista de scores da categoria especificada
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
        Busca scores por texto no título ou descrição
        
        Args:
            query (str): Termo de busca
            
        Returns:
            List[ScoreInfo]: Lista de scores que correspondem à busca
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


# Instância global do serviço
score_service = ScoreService()
