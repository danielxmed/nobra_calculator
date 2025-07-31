"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score Calculator

Estimates amount of scarring in the liver based on various lab tests.
Distinguishes between patients with nonalcoholic fatty liver disease 
who have (F3-F4) and do not have (F0-F2) advanced fibrosis.

References:
1. Angulo P, Hui JM, Marchesini G, et al. The NAFLD fibrosis score: 
   a noninvasive system that identifies liver fibrosis in patients with NAFLD. 
   Hepatology. 2007;45(4):846-54.
"""

from typing import Dict, Any


class NafldFibroseScoreCalculator:
    """Calculator for NAFLD Fibrosis Score"""
    
    def __init__(self):
        # Formula constants
        self.INTERCEPT = -1.675
        self.AGE_COEFFICIENT = 0.037
        self.BMI_COEFFICIENT = 0.094
        self.HYPERGLYCEMIA_COEFFICIENT = 1.13
        self.AST_ALT_RATIO_COEFFICIENT = 0.99
        self.PLATELET_COEFFICIENT = -0.013
        self.ALBUMIN_COEFFICIENT = -0.66
        
        # Interpretation thresholds
        self.LOW_CUTOFF = -1.455  # Below this: absence of significant fibrosis
        self.HIGH_CUTOFF = 0.676   # Above this: presence of significant fibrosis
    
    def calculate(self, age: float, bmi: float, hyperglycemia: str, 
                  ast: float, alt: float, platelet_count: float, 
                  albumin: float) -> Dict[str, Any]:
        """
        Calculates the NAFLD Fibrosis Score
        
        Args:
            age (float): Patient age in years
            bmi (float): Body Mass Index in kg/m²
            hyperglycemia (str): Presence of IFG/diabetes ("yes" or "no")
            ast (float): AST level in IU/L
            alt (float): ALT level in IU/L
            platelet_count (float): Platelet count in ×10⁹/L
            albumin (float): Serum albumin in g/dL
            
        Returns:
            Dict with the score result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, bmi, hyperglycemia, ast, alt, 
                            platelet_count, albumin)
        
        # Calculate AST/ALT ratio
        ast_alt_ratio = ast / alt
        
        # Convert hyperglycemia to binary
        hyperglycemia_binary = 1 if hyperglycemia.lower() == "yes" else 0
        
        # Calculate the NAFLD Fibrosis Score
        # Formula: -1.675 + 0.037 × age + 0.094 × BMI + 1.13 × hyperglycemia 
        #          + 0.99 × AST/ALT ratio - 0.013 × platelet - 0.66 × albumin
        score = (
            self.INTERCEPT +
            self.AGE_COEFFICIENT * age +
            self.BMI_COEFFICIENT * bmi +
            self.HYPERGLYCEMIA_COEFFICIENT * hyperglycemia_binary +
            self.AST_ALT_RATIO_COEFFICIENT * ast_alt_ratio +
            self.PLATELET_COEFFICIENT * platelet_count +
            self.ALBUMIN_COEFFICIENT * albumin
        )
        
        # Round to 3 decimal places
        score = round(score, 3)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "ast_alt_ratio": round(ast_alt_ratio, 3)
        }
    
    def _validate_inputs(self, age: float, bmi: float, hyperglycemia: str,
                        ast: float, alt: float, platelet_count: float,
                        albumin: float):
        """Validates input parameters"""
        
        # Age validation
        if not 0 <= age <= 120:
            raise ValueError("Age must be between 0 and 120 years")
        
        # BMI validation
        if not 10 <= bmi <= 70:
            raise ValueError("BMI must be between 10 and 70 kg/m²")
        
        # Hyperglycemia validation
        if hyperglycemia.lower() not in ["yes", "no"]:
            raise ValueError("Hyperglycemia must be 'yes' or 'no'")
        
        # AST validation
        if not 1 <= ast <= 2000:
            raise ValueError("AST must be between 1 and 2000 IU/L")
        
        # ALT validation
        if not 1 <= alt <= 2000:
            raise ValueError("ALT must be between 1 and 2000 IU/L")
        
        # ALT cannot be zero (division by zero)
        if alt == 0:
            raise ValueError("ALT cannot be zero")
        
        # Platelet count validation
        if not 10 <= platelet_count <= 800:
            raise ValueError("Platelet count must be between 10 and 800 ×10⁹/L")
        
        # Albumin validation
        if not 1.0 <= albumin <= 6.0:
            raise ValueError("Albumin must be between 1.0 and 6.0 g/dL")
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (float): Calculated NAFLD Fibrosis Score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.LOW_CUTOFF:
            return {
                "stage": "F0-F2",
                "description": "Absence of significant fibrosis",
                "interpretation": (
                    f"Score of {score} (< -1.455) is a predictor of absence of "
                    "significant fibrosis (F0-F2 fibrosis). Negative predictive value "
                    "of 93% for ruling out advanced fibrosis. These patients have mild "
                    "to moderate fibrosis and are unlikely to have advanced liver disease."
                )
            }
        elif score > self.HIGH_CUTOFF:
            return {
                "stage": "F3-F4",
                "description": "Presence of significant fibrosis",
                "interpretation": (
                    f"Score of {score} (> 0.676) is a predictor of presence of "
                    "significant fibrosis (F3-F4 fibrosis). Positive predictive value "
                    "of 90% for advanced fibrosis. These patients likely have bridging "
                    "fibrosis (F3) or cirrhosis (F4) and should be considered for "
                    "close monitoring and treatment."
                )
            }
        else:
            return {
                "stage": "Indeterminate",
                "description": "Indeterminate zone",
                "interpretation": (
                    f"Score of {score} (between -1.455 and 0.676) falls in the "
                    "indeterminate zone. Approximately 30% of patients fall into this "
                    "range where the score cannot definitively rule in or rule out "
                    "advanced fibrosis. Additional testing such as liver biopsy, "
                    "elastography, or other non-invasive markers may be needed."
                )
            }


def calculate_nafld_fibrosis_score(age: float, bmi: float, hyperglycemia: str,
                                 ast: float, alt: float, platelet_count: float,
                                 albumin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NafldFibroseScoreCalculator()
    return calculator.calculate(age, bmi, hyperglycemia, ast, alt, 
                              platelet_count, albumin)