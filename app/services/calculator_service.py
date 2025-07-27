"""
Service to execute medical score calculations
"""

import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from app.services.score_service import score_service


class CalculatorService:
    """Service to execute score calculations"""
    
    def __init__(self, calculators_directory: str = "calculators"):
        """
        Initializes the calculator service
        
        Args:
            calculators_directory (str): Directory containing the calculation modules
        """
        self.calculators_directory = Path(calculators_directory)
        self._calculator_cache: Dict[str, Any] = {}
        
        # Add the calculators directory to Python's path
        if str(self.calculators_directory.absolute()) not in sys.path:
            sys.path.insert(0, str(self.calculators_directory.absolute().parent))
    
    def _load_calculator(self, score_id: str) -> Optional[Any]:
        """
        Dynamically loads a score's calculation module
        
        Args:
            score_id (str): ID of the score
            
        Returns:
            Optional[Any]: Calculation function or None if not found
        """
        if score_id in self._calculator_cache:
            return self._calculator_cache[score_id]
        
        try:
            # Try to import the calculator module
            module_name = f"calculators.{score_id}"
            calculator_module = importlib.import_module(module_name)
            
            # Look for the calculation function (convention: calculate_<score_id>)
            function_name = f"calculate_{score_id}"
            
            if hasattr(calculator_module, function_name):
                calculator_function = getattr(calculator_module, function_name)
                self._calculator_cache[score_id] = calculator_function
                return calculator_function
            
            # If the function with the standard pattern is not found, look for other conventions
            # Look for a Calculator class
            if hasattr(calculator_module, f"{score_id.replace('_', '').title()}Calculator"):
                calculator_class_name = f"{score_id.replace('_', '').title()}Calculator"
                calculator_class = getattr(calculator_module, calculator_class_name)
                calculator_instance = calculator_class()
                
                if hasattr(calculator_instance, 'calculate'):
                    calculator_function = calculator_instance.calculate
                    self._calculator_cache[score_id] = calculator_function
                    return calculator_function
            
            print(f"Calculation function not found for {score_id}")
            return None
            
        except ImportError as e:
            print(f"Error importing calculator for {score_id}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error loading calculator {score_id}: {e}")
            return None
    
    def calculate_score(self, score_id: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes a score's calculation with the provided parameters
        
        Args:
            score_id (str): ID of the score
            parameters (dict): Parameters required for calculation
            
        Returns:
            Optional[Dict]: Calculation result or None in case of error
        """
        # Check if the score exists
        if not score_service.score_exists(score_id):
            raise ValueError(f"Score '{score_id}' not found")
        
        # Load the calculator
        calculator_function = self._load_calculator(score_id)
        if calculator_function is None:
            raise ValueError(f"Calculator for '{score_id}' not found")
        
        try:
            # Execute the calculation
            result = calculator_function(**parameters)
            return result
            
        except TypeError as e:
            # Parameter error (missing or invalid arguments)
            raise ValueError(f"Invalid parameters for {score_id}: {e}")
        except Exception as e:
            # Other calculation errors
            raise ValueError(f"Error calculating {score_id}: {e}")
    
    def validate_parameters(self, score_id: str, parameters: Dict[str, Any]) -> bool:
        """
        Validates if the provided parameters are sufficient for the calculation
        
        Args:
            score_id (str): ID of the score
            parameters (dict): Parameters to validate
            
        Returns:
            bool: True if parameters are valid, False otherwise
        """
        # Get score metadata
        metadata = score_service.get_score_metadata(score_id)
        if metadata is None:
            return False
        
        # Check if all required parameters are present
        for param in metadata.parameters:
            if param.required and param.name not in parameters:
                return False
        
        return True
    
    def get_missing_parameters(self, score_id: str, parameters: Dict[str, Any]) -> list:
        """
        Returns the list of missing required parameters
        
        Args:
            score_id (str): ID of the score
            parameters (dict): Provided parameters
            
        Returns:
            list: List of missing parameters
        """
        missing = []
        
        # Get score metadata
        metadata = score_service.get_score_metadata(score_id)
        if metadata is None:
            return missing
        
        # Check which required parameters are missing
        for param in metadata.parameters:
            if param.required and param.name not in parameters:
                missing.append(param.name)
        
        return missing
    
    def reload_calculators(self):
        """Clears the calculator cache forcing reload"""
        self._calculator_cache.clear()
        
        # Remove calculator modules from Python's cache
        modules_to_remove = []
        for module_name in sys.modules:
            if module_name.startswith("calculators."):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            del sys.modules[module_name]
    
    def is_calculator_available(self, score_id: str) -> bool:
        """
        Checks if a calculator is available for the score
        
        Args:
            score_id (str): ID of the score
            
        Returns:
            bool: True if the calculator is available, False otherwise
        """
        calculator_function = self._load_calculator(score_id)
        return calculator_function is not None


# Global service instance
calculator_service = CalculatorService()
