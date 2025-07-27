"""
Serviço para executar cálculos dos scores médicos
"""

import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from app.services.score_service import score_service


class CalculatorService:
    """Serviço para executar cálculos dos scores"""
    
    def __init__(self, calculators_directory: str = "calculators"):
        """
        Inicializa o serviço de calculadora
        
        Args:
            calculators_directory (str): Diretório contendo os módulos de cálculo
        """
        self.calculators_directory = Path(calculators_directory)
        self._calculator_cache: Dict[str, Any] = {}
        
        # Adiciona o diretório de calculadoras ao path do Python
        if str(self.calculators_directory.absolute()) not in sys.path:
            sys.path.insert(0, str(self.calculators_directory.absolute().parent))
    
    def _load_calculator(self, score_id: str) -> Optional[Any]:
        """
        Carrega dinamicamente o módulo de cálculo de um score
        
        Args:
            score_id (str): ID do score
            
        Returns:
            Optional[Any]: Função de cálculo ou None se não encontrada
        """
        if score_id in self._calculator_cache:
            return self._calculator_cache[score_id]
        
        try:
            # Tenta importar o módulo do calculador
            module_name = f"calculators.{score_id}"
            calculator_module = importlib.import_module(module_name)
            
            # Procura pela função de cálculo (convenção: calculate_<score_id>)
            function_name = f"calculate_{score_id}"
            
            if hasattr(calculator_module, function_name):
                calculator_function = getattr(calculator_module, function_name)
                self._calculator_cache[score_id] = calculator_function
                return calculator_function
            
            # Se não encontrar a função com o padrão, procura por outras convenções
            # Procura por uma classe Calculator
            if hasattr(calculator_module, f"{score_id.replace('_', '').title()}Calculator"):
                calculator_class_name = f"{score_id.replace('_', '').title()}Calculator"
                calculator_class = getattr(calculator_module, calculator_class_name)
                calculator_instance = calculator_class()
                
                if hasattr(calculator_instance, 'calculate'):
                    calculator_function = calculator_instance.calculate
                    self._calculator_cache[score_id] = calculator_function
                    return calculator_function
            
            print(f"Função de cálculo não encontrada para {score_id}")
            return None
            
        except ImportError as e:
            print(f"Erro ao importar calculadora para {score_id}: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao carregar calculadora {score_id}: {e}")
            return None
    
    def calculate_score(self, score_id: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executa o cálculo de um score com os parâmetros fornecidos
        
        Args:
            score_id (str): ID do score
            parameters (dict): Parâmetros necessários para o cálculo
            
        Returns:
            Optional[Dict]: Resultado do cálculo ou None em caso de erro
        """
        # Verifica se o score existe
        if not score_service.score_exists(score_id):
            raise ValueError(f"Score '{score_id}' não encontrado")
        
        # Carrega a calculadora
        calculator_function = self._load_calculator(score_id)
        if calculator_function is None:
            raise ValueError(f"Calculadora para '{score_id}' não encontrada")
        
        try:
            # Executa o cálculo
            result = calculator_function(**parameters)
            return result
            
        except TypeError as e:
            # Erro de parâmetros (argumentos faltando ou inválidos)
            raise ValueError(f"Parâmetros inválidos para {score_id}: {e}")
        except Exception as e:
            # Outros erros de cálculo
            raise ValueError(f"Erro no cálculo de {score_id}: {e}")
    
    def validate_parameters(self, score_id: str, parameters: Dict[str, Any]) -> bool:
        """
        Valida se os parâmetros fornecidos são suficientes para o cálculo
        
        Args:
            score_id (str): ID do score
            parameters (dict): Parâmetros para validar
            
        Returns:
            bool: True se os parâmetros são válidos, False caso contrário
        """
        # Obtém os metadados do score
        metadata = score_service.get_score_metadata(score_id)
        if metadata is None:
            return False
        
        # Verifica se todos os parâmetros obrigatórios estão presentes
        for param in metadata.parameters:
            if param.required and param.name not in parameters:
                return False
        
        return True
    
    def get_missing_parameters(self, score_id: str, parameters: Dict[str, Any]) -> list:
        """
        Retorna a lista de parâmetros obrigatórios que estão faltando
        
        Args:
            score_id (str): ID do score
            parameters (dict): Parâmetros fornecidos
            
        Returns:
            list: Lista de parâmetros faltando
        """
        missing = []
        
        # Obtém os metadados do score
        metadata = score_service.get_score_metadata(score_id)
        if metadata is None:
            return missing
        
        # Verifica quais parâmetros obrigatórios estão faltando
        for param in metadata.parameters:
            if param.required and param.name not in parameters:
                missing.append(param.name)
        
        return missing
    
    def reload_calculators(self):
        """Limpa o cache de calculadoras forçando o recarregamento"""
        self._calculator_cache.clear()
        
        # Remove módulos de calculadoras do cache do Python
        modules_to_remove = []
        for module_name in sys.modules:
            if module_name.startswith("calculators."):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            del sys.modules[module_name]
    
    def is_calculator_available(self, score_id: str) -> bool:
        """
        Verifica se existe uma calculadora disponível para o score
        
        Args:
            score_id (str): ID do score
            
        Returns:
            bool: True se a calculadora está disponível, False caso contrário
        """
        calculator_function = self._load_calculator(score_id)
        return calculator_function is not None


# Instância global do serviço
calculator_service = CalculatorService()
