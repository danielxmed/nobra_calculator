"""
Glasgow Alcoholic Hepatitis Score (GAHS) Calculator

The Glasgow Alcoholic Hepatitis Score is a prognostic tool that predicts mortality 
in patients with alcoholic hepatitis. It was developed from a multivariate analysis 
of factors predictive of mortality and has been shown to be more accurate than the 
modified Discriminant Function for predicting 28-day outcomes in alcoholic hepatitis.

References (Vancouver style):
1. Forrest EH, Evans CD, Stewart S, et al. Analysis of factors predictive of mortality 
   in alcoholic hepatitis and derivation and validation of the Glasgow alcoholic hepatitis 
   score. Gut. 2005;54(8):1174-1179. doi: 10.1136/gut.2004.050781.
2. Louvet A, Naveau S, Abdelnour M, et al. The Lille model: a new tool for therapeutic 
   strategy in patients with severe alcoholic hepatitis treated with steroids. Hepatology. 
   2007;45(6):1348-1354. doi: 10.1002/hep.21607.
3. Forrest EH, Morris AJ, Stewart S, et al. The Glasgow alcoholic hepatitis score identifies 
   patients who may benefit from corticosteroids. Gut. 2007;56(12):1743-1746. 
   doi: 10.1136/gut.2006.099226.
"""

from typing import Dict, Any


class GlasgowAlcoholicHepatitisScoreCalculator:
    """Calculator for Glasgow Alcoholic Hepatitis Score (GAHS)"""
    
    def __init__(self):
        # Scoring thresholds for each parameter
        self.AGE_THRESHOLD = 50  # years
        self.WBC_THRESHOLD = 15.0  # ×10⁹/L
        self.UREA_THRESHOLD = 5.0  # mmol/L
        self.PT_RATIO_THRESHOLD_LOW = 1.5  # ratio
        self.PT_RATIO_THRESHOLD_HIGH = 2.0  # ratio
        self.BILIRUBIN_THRESHOLD_LOW = 125.0  # μmol/L
        self.BILIRUBIN_THRESHOLD_HIGH = 250.0  # μmol/L
        
        # Mortality threshold
        self.HIGH_RISK_THRESHOLD = 9  # points
    
    def calculate(self, age: int, white_cell_count: float, urea: float, 
                 prothrombin_time_ratio: float, bilirubin: float) -> Dict[str, Any]:
        """
        Calculates Glasgow Alcoholic Hepatitis Score using clinical parameters
        
        Args:
            age (int): Patient age in years
            white_cell_count (float): White blood cell count (×10⁹/L)
            urea (float): Blood urea nitrogen level (mmol/L)
            prothrombin_time_ratio (float): Prothrombin time ratio or INR
            bilirubin (float): Serum total bilirubin level (μmol/L)
            
        Returns:
            Dict with the score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, white_cell_count, urea, prothrombin_time_ratio, bilirubin)
        
        # Calculate component scores
        age_score = self._calculate_age_score(age)
        wbc_score = self._calculate_wbc_score(white_cell_count)
        urea_score = self._calculate_urea_score(urea)
        pt_score = self._calculate_pt_score(prothrombin_time_ratio)
        bilirubin_score = self._calculate_bilirubin_score(bilirubin)
        
        # Calculate total score
        total_score = age_score + wbc_score + urea_score + pt_score + bilirubin_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, age, white_cell_count, 
                                                urea, prothrombin_time_ratio, bilirubin)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, white_cell_count: float, urea: float, 
                        prothrombin_time_ratio: float, bilirubin: float):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(white_cell_count, (int, float)):
            raise ValueError("White cell count must be a number")
        
        if white_cell_count < 1.0 or white_cell_count > 100.0:
            raise ValueError("White cell count must be between 1.0 and 100.0 ×10⁹/L")
        
        if not isinstance(urea, (int, float)):
            raise ValueError("Urea must be a number")
        
        if urea < 1.0 or urea > 50.0:
            raise ValueError("Urea must be between 1.0 and 50.0 mmol/L")
        
        if not isinstance(prothrombin_time_ratio, (int, float)):
            raise ValueError("Prothrombin time ratio must be a number")
        
        if prothrombin_time_ratio < 0.8 or prothrombin_time_ratio > 10.0:
            raise ValueError("Prothrombin time ratio must be between 0.8 and 10.0")
        
        if not isinstance(bilirubin, (int, float)):
            raise ValueError("Bilirubin must be a number")
        
        if bilirubin < 10.0 or bilirubin > 1000.0:
            raise ValueError("Bilirubin must be between 10.0 and 1000.0 μmol/L")
    
    def _calculate_age_score(self, age: int) -> int:
        """Calculate age component score"""
        if age < self.AGE_THRESHOLD:
            return 1
        else:
            return 2
    
    def _calculate_wbc_score(self, white_cell_count: float) -> int:
        """Calculate white blood cell count component score"""
        if white_cell_count < self.WBC_THRESHOLD:
            return 1
        else:
            return 2
    
    def _calculate_urea_score(self, urea: float) -> int:
        """Calculate urea component score"""
        if urea < self.UREA_THRESHOLD:
            return 1
        else:
            return 2
    
    def _calculate_pt_score(self, prothrombin_time_ratio: float) -> int:
        """Calculate prothrombin time ratio component score"""
        if prothrombin_time_ratio < self.PT_RATIO_THRESHOLD_LOW:
            return 1
        elif prothrombin_time_ratio <= self.PT_RATIO_THRESHOLD_HIGH:
            return 2
        else:
            return 3
    
    def _calculate_bilirubin_score(self, bilirubin: float) -> int:
        """Calculate bilirubin component score"""
        if bilirubin < self.BILIRUBIN_THRESHOLD_LOW:
            return 1
        elif bilirubin <= self.BILIRUBIN_THRESHOLD_HIGH:
            return 2
        else:
            return 3
    
    def _get_interpretation(self, score: int, age: int, white_cell_count: float, 
                          urea: float, prothrombin_time_ratio: float, 
                          bilirubin: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the GAHS score
        
        Args:
            score (int): Calculated GAHS total score
            age, white_cell_count, urea, prothrombin_time_ratio, bilirubin: Input values for context
            
        Returns:
            Dict with interpretation details
        """
        
        # Format values for reporting
        wbc_formatted = f"{white_cell_count:.1f}"
        urea_formatted = f"{urea:.1f}"
        pt_formatted = f"{prothrombin_time_ratio:.2f}"
        bilirubin_formatted = f"{bilirubin:.0f}"
        
        # Build parameter summary
        param_summary = (f"Age: {age} years, WBC: {wbc_formatted} ×10⁹/L, "
                        f"Urea: {urea_formatted} mmol/L, PT ratio: {pt_formatted}, "
                        f"Bilirubin: {bilirubin_formatted} μmol/L")
        
        if score < self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Good prognosis",
                "interpretation": (
                    f"Glasgow Alcoholic Hepatitis Score: {score}/12 points ({param_summary}). "
                    f"GAHS <9 indicates good prognosis with 28-day survival of approximately 87% "
                    f"without specific treatment. Patients in this category typically do not require "
                    f"corticosteroid therapy as there is no demonstrated survival benefit. Focus on "
                    f"supportive care, alcohol cessation counseling, nutritional support, and management "
                    f"of complications. Monitor for disease progression and reassess if clinical "
                    f"deterioration occurs."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Poor prognosis",
                "interpretation": (    
                    f"Glasgow Alcoholic Hepatitis Score: {score}/12 points ({param_summary}). "
                    f"GAHS ≥9 indicates poor prognosis with 28-day survival of approximately 46% "
                    f"without treatment, improving to 78% with corticosteroid therapy. Strong indication "
                    f"for corticosteroid treatment unless contraindicated. Consider prednisolone 40mg "
                    f"daily for 28 days if no contraindications (active infection, renal failure, "
                    f"gastrointestinal bleeding). Provide intensive supportive care, alcohol cessation "
                    f"programs, and consider liver transplant evaluation if appropriate. Monitor closely "
                    f"for treatment response and complications."
                )
            }


def calculate_glasgow_alcoholic_hepatitis_score(age: int, white_cell_count: float, urea: float, 
                                              prothrombin_time_ratio: float, bilirubin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_alcoholic_hepatitis_score pattern
    """
    calculator = GlasgowAlcoholicHepatitisScoreCalculator()
    return calculator.calculate(age, white_cell_count, urea, prothrombin_time_ratio, bilirubin)