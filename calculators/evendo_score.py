"""
EVendo Score for Esophageal Varices Calculator

Predicts presence and size of esophageal varices prior to screening endoscopy in patients 
with cirrhosis. Uses readily available laboratory values and clinical findings to help 
identify patients who may safely defer endoscopic screening.

References:
- Dong TS, Kalani A, Aby ES, Le L, Luu K, Hauer M, et al. Machine Learning-based Development 
  and Validation of a Scoring System for Screening High-Risk Esophageal Varices. 
  Clin Gastroenterol Hepatol. 2019;17(10):1894-1901.
- Hassan M, Hasan MW, Giordano A, Masud F, Bartoli A, Ahmad N. Validation of the EVendo 
  score for the prediction of varices in cirrhotic patients. World J Hepatol. 2022;14(2):460-474.
"""

from typing import Dict, Any


class EvendoScoreCalculator:
    """Calculator for EVendo Score for Esophageal Varices"""
    
    def __init__(self):
        # Formula constants from original EVendo Score development
        self.INR_COEFFICIENT = 8.5
        self.AST_DENOMINATOR = 35
        self.PLATELET_DENOMINATOR = 150
        self.BUN_DENOMINATOR = 20
        self.HEMOGLOBIN_DENOMINATOR = 15
        self.ASCITES_BONUS = 1
        self.RISK_THRESHOLD = 3.90
    
    def calculate(self, inr: float, ast_u_l: float, platelet_count: float, 
                  bun_mg_dl: float, hemoglobin_g_dl: float, ascites_present: str) -> Dict[str, Any]:
        """
        Calculates the EVendo Score using laboratory values and clinical findings
        
        Args:
            inr (float): International Normalized Ratio (0.5-10.0)
            ast_u_l (float): Aspartate aminotransferase level in U/L (5-500)
            platelet_count (float): Platelet count in ×10³/µL (10-1000)
            bun_mg_dl (float): Blood urea nitrogen in mg/dL (2-100)
            hemoglobin_g_dl (float): Hemoglobin level in g/dL (4.0-20.0)
            ascites_present (str): Presence of ascites ("yes" or "no")
            
        Returns:
            Dict with the EVendo Score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(inr, ast_u_l, platelet_count, bun_mg_dl, hemoglobin_g_dl, ascites_present)
        
        # Calculate EVendo Score
        evendo_score = self._calculate_score(inr, ast_u_l, platelet_count, bun_mg_dl, hemoglobin_g_dl, ascites_present)
        
        # Get risk classification and interpretation
        interpretation = self._get_interpretation(evendo_score)
        
        return {
            "result": evendo_score,
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "probability_varices": interpretation["probability_varices"],
            "recommendation": interpretation["recommendation"]
        }
    
    def _validate_inputs(self, inr: float, ast_u_l: float, platelet_count: float, 
                        bun_mg_dl: float, hemoglobin_g_dl: float, ascites_present: str):
        """Validates input parameters"""
        
        if not isinstance(inr, (int, float)):
            raise ValueError("INR must be a number")
        
        if not isinstance(ast_u_l, (int, float)):
            raise ValueError("AST must be a number")
        
        if not isinstance(platelet_count, (int, float)):
            raise ValueError("Platelet count must be a number")
        
        if not isinstance(bun_mg_dl, (int, float)):
            raise ValueError("BUN must be a number")
        
        if not isinstance(hemoglobin_g_dl, (int, float)):
            raise ValueError("Hemoglobin must be a number")
        
        if ascites_present not in ["yes", "no"]:
            raise ValueError("Ascites presence must be 'yes' or 'no'")
        
        if inr < 0.5 or inr > 10.0:
            raise ValueError("INR must be between 0.5 and 10.0")
        
        if ast_u_l < 5 or ast_u_l > 500:
            raise ValueError("AST must be between 5 and 500 U/L")
        
        if platelet_count < 10 or platelet_count > 1000:
            raise ValueError("Platelet count must be between 10 and 1000 ×10³/µL")
        
        if bun_mg_dl < 2 or bun_mg_dl > 100:
            raise ValueError("BUN must be between 2 and 100 mg/dL")
        
        if hemoglobin_g_dl < 4.0 or hemoglobin_g_dl > 20.0:
            raise ValueError("Hemoglobin must be between 4.0 and 20.0 g/dL")
    
    def _calculate_score(self, inr: float, ast_u_l: float, platelet_count: float, 
                        bun_mg_dl: float, hemoglobin_g_dl: float, ascites_present: str) -> float:
        """
        Calculates the EVendo Score using the formula:
        A = (8.5 × INR) + (AST / 35)
        B = (Platelet count / 150) + (BUN / 20) + (Hemoglobin / 15)
        EVendo Score = (A / B) + 1 (if ascites present)
        """
        
        # Calculate component A
        a_component = (self.INR_COEFFICIENT * inr) + (ast_u_l / self.AST_DENOMINATOR)
        
        # Calculate component B
        b_component = ((platelet_count / self.PLATELET_DENOMINATOR) + 
                      (bun_mg_dl / self.BUN_DENOMINATOR) + 
                      (hemoglobin_g_dl / self.HEMOGLOBIN_DENOMINATOR))
        
        # Check for division by zero (should not occur with valid inputs)
        if b_component == 0:
            raise ValueError("Invalid calculation: denominator component is zero")
        
        # Calculate base score
        base_score = a_component / b_component
        
        # Add ascites bonus if present
        ascites_bonus = self.ASCITES_BONUS if ascites_present == "yes" else 0
        
        evendo_score = base_score + ascites_bonus
        
        return round(evendo_score, 2)
    
    def _get_interpretation(self, score: float) -> Dict[str, Any]:
        """
        Determines the risk classification and clinical interpretation based on EVendo Score
        
        Args:
            score (float): Calculated EVendo Score
            
        Returns:
            Dict with risk classification and clinical interpretation
        """
        
        if score <= self.RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low probability of esophageal varices",
                "interpretation": f"EVendo Score: {score} (≤3.90 = Low Risk). Screening endoscopy may be safely deferred. Probability of esophageal varices <5%. This score has 95.1% sensitivity and 95.8% negative predictive value for detecting varices needing treatment. Consider routine clinical follow-up with repeat assessment in 1-2 years or if clinical status changes.",
                "probability_varices": "<5%",
                "recommendation": "Expectant management - screening endoscopy may be deferred"
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High probability of esophageal varices",
                "interpretation": f"EVendo Score: {score} (>3.90 = High Risk). Endoscopic screening recommended. Probability of esophageal varices ≥5%. Upper endoscopy should be performed to evaluate for the presence and size of varices and determine need for primary prophylaxis. Consider urgent endoscopy if high clinical suspicion for large varices or bleeding risk.",
                "probability_varices": "≥5%",
                "recommendation": "Endoscopic screening recommended"
            }


def calculate_evendo_score(inr: float, ast_u_l: float, platelet_count: float, 
                          bun_mg_dl: float, hemoglobin_g_dl: float, ascites_present: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_evendo_score pattern
    """
    calculator = EvendoScoreCalculator()
    return calculator.calculate(inr, ast_u_l, platelet_count, bun_mg_dl, hemoglobin_g_dl, ascites_present)