"""
AST to Platelet Ratio Index (APRI) Calculator

Determines the likelihood of liver fibrosis and cirrhosis in patients with hepatitis C
using AST levels and platelet count.

Formula: APRI = [(AST ÷ AST Upper Limit Normal) × 100] ÷ Platelet Count

References:
- Lin ZH, Xin YN, Dong QJ, et al. Performance of the aspartate aminotransferase-to-platelet 
  ratio index for the staging of hepatitis C-related fibrosis: an updated meta-analysis. 
  Hepatology. 2011;53(3):726-36.
"""

from typing import Dict, Any


class ApriCalculator:
    """Calculator for AST to Platelet Ratio Index (APRI)"""
    
    def __init__(self):
        # Standard interpretation thresholds
        self.LOW_RISK_THRESHOLD = 0.5
        self.MODERATE_RISK_THRESHOLD = 0.7
        self.HIGH_RISK_THRESHOLD = 1.0
        self.VERY_HIGH_RISK_THRESHOLD = 1.5
        self.EXTREMELY_HIGH_RISK_THRESHOLD = 2.0
    
    def calculate(self, ast_level: float, ast_upper_limit_normal: float, platelet_count: float) -> Dict[str, Any]:
        """
        Calculates the APRI score using the provided parameters
        
        Args:
            ast_level (float): Aspartate aminotransferase (AST) level in IU/L
            ast_upper_limit_normal (float): Upper limit of normal for AST (typically 40 IU/L)
            platelet_count (float): Platelet count in ×10⁹/L
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(ast_level, ast_upper_limit_normal, platelet_count)
        
        # Calculation logic
        result = self._calculate_formula(ast_level, ast_upper_limit_normal, platelet_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "ratio",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ast_level: float, ast_upper_limit_normal: float, platelet_count: float):
        """Validates input parameters"""
        
        # AST level validation
        if not isinstance(ast_level, (int, float)):
            raise ValueError("AST level must be a number")
        
        if ast_level < 1 or ast_level > 2000:
            raise ValueError("AST level must be between 1 and 2000 IU/L")
        
        # AST upper limit normal validation
        if not isinstance(ast_upper_limit_normal, (int, float)):
            raise ValueError("AST upper limit normal must be a number")
        
        if ast_upper_limit_normal < 10 or ast_upper_limit_normal > 100:
            raise ValueError("AST upper limit normal must be between 10 and 100 IU/L")
        
        # Platelet count validation
        if not isinstance(platelet_count, (int, float)):
            raise ValueError("Platelet count must be a number")
        
        if platelet_count < 10 or platelet_count > 1000:
            raise ValueError("Platelet count must be between 10 and 1000 ×10⁹/L")
        
        # Additional logical validation
        if platelet_count == 0:
            raise ValueError("Platelet count cannot be zero (division by zero)")
    
    def _calculate_formula(self, ast_level: float, ast_upper_limit_normal: float, platelet_count: float) -> float:
        """Implements the APRI formula"""
        
        # APRI = [(AST ÷ AST Upper Limit Normal) × 100] ÷ Platelet Count
        ast_ratio = ast_level / ast_upper_limit_normal
        ast_ratio_percent = ast_ratio * 100
        apri_score = ast_ratio_percent / platelet_count
        
        # Round to 2 decimal places for clinical relevance
        return round(apri_score, 2)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the APRI score
        
        Args:
            result (float): Calculated APRI score
            
        Returns:
            Dict with interpretation details
        """
        
        if result <= self.LOW_RISK_THRESHOLD:  # ≤0.5
            return {
                "stage": "Low Risk",
                "description": "Minimal or no fibrosis",
                "interpretation": "APRI score ≤0.5 suggests minimal or no liver fibrosis. High negative predictive value for ruling out significant fibrosis and cirrhosis."
            }
        elif result <= self.MODERATE_RISK_THRESHOLD:  # 0.5-0.7
            return {
                "stage": "Low-Moderate Risk",
                "description": "Possible mild fibrosis",
                "interpretation": "APRI score 0.5-0.7 suggests possible mild fibrosis. Additional testing may be needed for definitive assessment."
            }
        elif result <= self.HIGH_RISK_THRESHOLD:  # 0.7-1.0
            return {
                "stage": "Moderate Risk",
                "description": "Significant fibrosis likely",
                "interpretation": "APRI score 0.7-1.0 suggests significant hepatic fibrosis with 77% sensitivity and 72% specificity. Consider further evaluation."
            }
        elif result <= self.VERY_HIGH_RISK_THRESHOLD:  # 1.0-1.5
            return {
                "stage": "High Risk",
                "description": "Cirrhosis likely",
                "interpretation": "APRI score 1.0-1.5 suggests cirrhosis with 76% sensitivity and 72% specificity. Further evaluation recommended."
            }
        elif result <= self.EXTREMELY_HIGH_RISK_THRESHOLD:  # 1.5-2.0
            return {
                "stage": "Very High Risk",
                "description": "Cirrhosis very likely",
                "interpretation": "APRI score 1.5-2.0 indicates high probability of cirrhosis. High positive predictive value for ruling in cirrhosis."
            }
        else:  # >2.0
            return {
                "stage": "Extremely High Risk",
                "description": "Cirrhosis highly likely",
                "interpretation": "APRI score ≥2.0 indicates very high probability of cirrhosis with 91% specificity but 46% sensitivity. Strong positive predictor of cirrhosis."
            }


def calculate_apri(ast_level: float, ast_upper_limit_normal: float, platelet_count: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_apri pattern
    """
    calculator = ApriCalculator()
    return calculator.calculate(ast_level, ast_upper_limit_normal, platelet_count)