"""
BARD Score for NAFLD Fibrosis Calculator

Predicts risk of advanced fibrosis in patients with non-alcoholic fatty liver disease.

References:
1. Harrison SA, et al. Development and validation of a simple NAFLD clinical 
   scoring system for identifying patients without advanced disease. 
   Gut. 2008 Oct;57(10):1441-7.
"""

from typing import Dict, Any


class BardScoreCalculator:
    """Calculator for BARD Score for NAFLD Fibrosis"""
    
    def __init__(self):
        # Score thresholds
        self.BMI_CUTOFF = 28.0
        self.AST_ALT_RATIO_CUTOFF = 0.8
        
        # Point allocations
        self.BMI_POINTS = 1
        self.AST_ALT_RATIO_POINTS = 2
        self.DIABETES_POINTS = 1
    
    def calculate(self, bmi: float, ast: float, alt: float, diabetes: str) -> Dict[str, Any]:
        """
        Calculates BARD score based on BMI, AST/ALT ratio, and diabetes status
        
        Args:
            bmi (float): Body Mass Index in kg/m²
            ast (float): Aspartate aminotransferase in U/L
            alt (float): Alanine aminotransferase in U/L
            diabetes (str): Presence of diabetes ("yes" or "no")
            
        Returns:
            Dict with BARD score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bmi, ast, alt, diabetes)
        
        # Calculate AST/ALT ratio
        ast_alt_ratio = self._calculate_ast_alt_ratio(ast, alt)
        
        # Calculate BARD score
        score = 0
        
        # BMI ≥28: 1 point
        if bmi >= self.BMI_CUTOFF:
            score += self.BMI_POINTS
        
        # AST/ALT ratio ≥0.8: 2 points
        if ast_alt_ratio >= self.AST_ALT_RATIO_CUTOFF:
            score += self.AST_ALT_RATIO_POINTS
        
        # Diabetes: 1 point
        if diabetes.lower() == "yes":
            score += self.DIABETES_POINTS
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bmi: float, ast: float, alt: float, diabetes: str):
        """Validates input parameters"""
        
        if not isinstance(bmi, (int, float)) or bmi < 10 or bmi > 70:
            raise ValueError("BMI must be between 10 and 70 kg/m²")
        
        if not isinstance(ast, (int, float)) or ast <= 0:
            raise ValueError("AST must be a positive number")
        
        if not isinstance(alt, (int, float)) or alt <= 0:
            raise ValueError("ALT must be a positive number")
        
        if diabetes.lower() not in ["yes", "no"]:
            raise ValueError("Diabetes must be 'yes' or 'no'")
    
    def _calculate_ast_alt_ratio(self, ast: float, alt: float) -> float:
        """
        Calculates AST/ALT ratio
        
        Args:
            ast (float): AST value
            alt (float): ALT value
            
        Returns:
            float: AST/ALT ratio
        """
        if alt == 0:
            raise ValueError("ALT cannot be zero")
        
        return ast / alt
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines risk category based on BARD score
        
        Args:
            score (int): BARD score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Low risk of advanced fibrosis",
                "interpretation": "Score 0-1 indicates low risk of advanced fibrosis (F3-F4). " +
                                "Negative predictive value 96%. Consider routine monitoring " +
                                "without immediate need for liver biopsy."
            }
        else:  # score 2-4
            return {
                "stage": "High Risk",
                "description": "High risk of advanced fibrosis",
                "interpretation": "Score 2-4 indicates high risk of advanced fibrosis (F3-F4). " +
                                "Odds ratio 17 (95% CI 9.2-31.9) for advanced fibrosis. " +
                                "Consider liver biopsy or non-invasive imaging (e.g., FibroScan) " +
                                "for further evaluation."
            }


def calculate_bard_score(bmi: float, ast: float, alt: float, diabetes: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BardScoreCalculator()
    return calculator.calculate(bmi, ast, alt, diabetes)