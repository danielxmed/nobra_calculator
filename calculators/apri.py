"""
AST to Platelet Ratio Index (APRI) Calculator

Determines the likelihood of hepatic fibrosis and cirrhosis in patients with hepatitis C 
using readily available laboratory values (AST and platelet count).

References:
1. Wai CT, Greenson JK, Fontana RJ, et al. A simple noninvasive index can predict both 
   significant fibrosis and cirrhosis in patients with chronic hepatitis C. Hepatology. 
   2003;38(2):518-26.
2. Shaheen AA, Myers RP. Diagnostic accuracy of the aspartate aminotransferase-to-platelet 
   ratio index for the prediction of hepatitis C-related fibrosis: a systematic review. 
   Hepatology. 2007;46(3):912-21.
"""

from typing import Dict, Any


class ApriCalculator:
    """Calculator for AST to Platelet Ratio Index (APRI)"""
    
    def __init__(self):
        # Reference cutoff values for interpretation
        self.CUTOFF_EXCLUDE_FIBROSIS = 0.3
        self.CUTOFF_EXCLUDE_CIRRHOSIS = 0.5
        self.CUTOFF_SIGNIFICANT_FIBROSIS = 1.5
        self.CUTOFF_CIRRHOSIS = 2.0
    
    def calculate(self, ast: float, ast_upper_limit: float, platelet_count: float) -> Dict[str, Any]:
        """
        Calculates the APRI score using the provided laboratory parameters
        
        Args:
            ast (float): Serum aspartate aminotransferase (AST) level in U/L
            ast_upper_limit (float): Upper limit of normal for AST in U/L 
                                   (typically 40 U/L for males, 32 U/L for females)
            platelet_count (float): Platelet count in × 10³/µL
            
        Returns:
            Dict with the APRI score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(ast, ast_upper_limit, platelet_count)
        
        # Calculate APRI score
        apri_score = self._calculate_apri(ast, ast_upper_limit, platelet_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(apri_score)
        
        return {
            "result": apri_score,
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ast: float, ast_upper_limit: float, platelet_count: float):
        """Validates input parameters"""
        
        if not isinstance(ast, (int, float)) or ast <= 0:
            raise ValueError("AST must be a positive number")
        
        if ast < 1 or ast > 2000:
            raise ValueError("AST value must be between 1 and 2000 U/L")
        
        if not isinstance(ast_upper_limit, (int, float)) or ast_upper_limit <= 0:
            raise ValueError("AST upper limit must be a positive number")
        
        if ast_upper_limit < 10 or ast_upper_limit > 100:
            raise ValueError("AST upper limit must be between 10 and 100 U/L")
        
        if not isinstance(platelet_count, (int, float)) or platelet_count <= 0:
            raise ValueError("Platelet count must be a positive number")
        
        if platelet_count < 10 or platelet_count > 1000:
            raise ValueError("Platelet count must be between 10 and 1000 × 10³/µL")
    
    def _calculate_apri(self, ast: float, ast_upper_limit: float, platelet_count: float) -> float:
        """
        Implements the APRI formula
        
        APRI = [(AST/AST upper limit of normal) × 100] / Platelet count (×10³/µL)
        """
        
        # Calculate AST ratio (normalized to upper limit of normal)
        ast_ratio = ast / ast_upper_limit
        
        # Calculate APRI score
        apri_score = (ast_ratio * 100) / platelet_count
        
        # Round to 3 decimal places for clinical relevance
        return round(apri_score, 3)
    
    def _get_interpretation(self, apri_score: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the APRI score
        
        Args:
            apri_score (float): Calculated APRI value
            
        Returns:
            Dict with clinical interpretation
        """
        
        if apri_score <= self.CUTOFF_EXCLUDE_FIBROSIS:
            return {
                "stage": "Low Risk",
                "description": "Rules out significant fibrosis",
                "interpretation": "APRI ≤0.3 has high negative predictive value for excluding significant liver fibrosis (METAVIR F2-F4). Significant fibrosis is unlikely."
            }
        elif apri_score <= self.CUTOFF_EXCLUDE_CIRRHOSIS:
            return {
                "stage": "Low-Intermediate Risk",
                "description": "Low probability of cirrhosis",
                "interpretation": "APRI 0.3-0.5 suggests low probability of advanced fibrosis. Values ≤0.5 have good negative predictive value for ruling out cirrhosis."
            }
        elif apri_score < self.CUTOFF_SIGNIFICANT_FIBROSIS:
            return {
                "stage": "Intermediate Risk",
                "description": "Indeterminate risk",
                "interpretation": "APRI 0.5-1.5 represents intermediate risk. Additional assessment with other non-invasive markers or liver biopsy may be needed for accurate staging."
            }
        elif apri_score < self.CUTOFF_CIRRHOSIS:
            return {
                "stage": "High Risk",
                "description": "Suggests significant fibrosis",
                "interpretation": "APRI ≥1.5 has good positive predictive value for significant fibrosis (METAVIR F3-F4). Consider hepatology referral and surveillance for complications."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Suggests cirrhosis",
                "interpretation": "APRI ≥2.0 strongly suggests cirrhosis (METAVIR F4). Requires hepatology evaluation, surveillance for hepatocellular carcinoma, and assessment for portal hypertension complications."
            }


def calculate_apri(ast: float, ast_upper_limit: float, platelet_count: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_apri pattern
    """
    calculator = ApriCalculator()
    return calculator.calculate(ast, ast_upper_limit, platelet_count)
