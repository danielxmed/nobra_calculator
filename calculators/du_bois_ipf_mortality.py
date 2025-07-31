"""
du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality Calculator

Determines 1-year mortality risk in IPF patients using PFT and clinical indicators.
Developed from two clinical trials (n=1,099) to identify independent predictors 
of 1-year mortality in idiopathic pulmonary fibrosis.

References:
1. du Bois RM, Weycker D, Albera C, Bradford WZ, Costabel U, Kartashov A, et al. 
   Ascertainment of individual risk of mortality for patients with idiopathic 
   pulmonary fibrosis. Am J Respir Crit Care Med. 2011;184(4):459-66.
2. Ley B, Ryerson CJ, Vittinghoff E, Ryu JH, Tomassetti S, Lee JS, et al. 
   A multidimensional index and staging system for idiopathic pulmonary fibrosis. 
   Ann Intern Med. 2012;156(10):684-91.
"""

from typing import Dict, Any


class DuBoisIpfMortalityCalculator:
    """Calculator for du Bois Score for IPF Mortality"""
    
    def __init__(self):
        # Scoring system parameters
        self.AGE_THRESHOLDS = {
            (0, 50): 0,      # ≤50 years: 0 points
            (51, 60): 1,     # 51-60 years: 1 point
            (61, 70): 2,     # 61-70 years: 2 points
            (71, 120): 3     # >70 years: 3 points
        }
        
        self.HOSPITALIZATION_POINTS = 2  # Recent respiratory hospitalization: 2 points
        
        self.FVC_THRESHOLDS = {
            65.1: 0,    # >65% predicted: 0 points
            50.1: 1,    # 50-65% predicted: 1 point
            0: 2        # <50% predicted: 2 points
        }
        
        self.FVC_DECLINE_THRESHOLD = -10.0  # >10% decline: 3 points
        self.FVC_DECLINE_POINTS = 3
    
    def calculate(self, age: int, respiratory_hospitalization: str, 
                  fvc_percent_predicted: float, change_fvc_24_weeks: float) -> Dict[str, Any]:
        """
        Calculates the du Bois Score for IPF mortality
        
        Args:
            age (int): Patient age in years
            respiratory_hospitalization (str): History of respiratory hospitalization ("yes"/"no")
            fvc_percent_predicted (float): FVC as percentage of predicted value
            change_fvc_24_weeks (float): Change in FVC over 24 weeks (% predicted)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, respiratory_hospitalization, fvc_percent_predicted, change_fvc_24_weeks)
        
        # Calculate score components
        age_points = self._calculate_age_points(age)
        hospitalization_points = self._calculate_hospitalization_points(respiratory_hospitalization)
        fvc_points = self._calculate_fvc_points(fvc_percent_predicted)
        fvc_change_points = self._calculate_fvc_change_points(change_fvc_24_weeks)
        
        # Calculate total score
        total_score = age_points + hospitalization_points + fvc_points + fvc_change_points
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, respiratory_hospitalization: str, 
                        fvc_percent_predicted: float, change_fvc_24_weeks: float):
        """Validates input parameters"""
        
        # Age validation
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        # Respiratory hospitalization validation
        if not isinstance(respiratory_hospitalization, str) or \
           respiratory_hospitalization.lower() not in ["yes", "no"]:
            raise ValueError("Respiratory hospitalization must be 'yes' or 'no'")
        
        # FVC % predicted validation
        if not isinstance(fvc_percent_predicted, (int, float)) or \
           fvc_percent_predicted < 10.0 or fvc_percent_predicted > 150.0:
            raise ValueError("FVC % predicted must be between 10.0 and 150.0")
        
        # FVC change validation
        if not isinstance(change_fvc_24_weeks, (int, float)) or \
           change_fvc_24_weeks < -50.0 or change_fvc_24_weeks > 50.0:
            raise ValueError("Change in FVC must be between -50.0 and 50.0 % predicted")
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculates points based on age"""
        
        for (min_age, max_age), points in self.AGE_THRESHOLDS.items():
            if min_age <= age <= max_age:
                return points
        
        # Fallback (should not reach here with proper validation)
        return 0
    
    def _calculate_hospitalization_points(self, respiratory_hospitalization: str) -> int:
        """Calculates points based on recent respiratory hospitalization"""
        
        if respiratory_hospitalization.lower() == "yes":
            return self.HOSPITALIZATION_POINTS
        return 0
    
    def _calculate_fvc_points(self, fvc_percent_predicted: float) -> int:
        """Calculates points based on FVC % predicted"""
        
        if fvc_percent_predicted > 65.0:
            return 0  # >65% predicted: 0 points
        elif fvc_percent_predicted >= 50.0:
            return 1  # 50-65% predicted: 1 point
        else:
            return 2  # <50% predicted: 2 points
    
    def _calculate_fvc_change_points(self, change_fvc_24_weeks: float) -> int:
        """Calculates points based on FVC change over 24 weeks"""
        
        # Decline >10% (change < -10.0) gets 3 points
        if change_fvc_24_weeks <= self.FVC_DECLINE_THRESHOLD:
            return self.FVC_DECLINE_POINTS
        return 0
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            score (int): Total du Bois score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Low 1-year mortality risk",
                "interpretation": "Low risk of 1-year mortality in IPF. Continue standard monitoring and treatment. Regular follow-up with pulmonary function tests and clinical assessment recommended."
            }
        elif score <= 8:
            return {
                "stage": "Intermediate Risk", 
                "description": "Intermediate 1-year mortality risk",
                "interpretation": "Intermediate risk of 1-year mortality in IPF. Consider more frequent monitoring, optimization of antifibrotic therapy, and evaluation for lung transplantation if appropriate. Discuss prognosis and advance care planning."
            }
        else:  # score >= 9
            return {
                "stage": "High Risk",
                "description": "High 1-year mortality risk", 
                "interpretation": "High risk of 1-year mortality in IPF. Urgent consideration for lung transplantation evaluation if candidate. Optimize supportive care, consider palliative care consultation, and discuss advance directives. Close monitoring required."
            }


def calculate_du_bois_ipf_mortality(age: int, respiratory_hospitalization: str, 
                                   fvc_percent_predicted: float, change_fvc_24_weeks: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_du_bois_ipf_mortality pattern
    """
    calculator = DuBoisIpfMortalityCalculator()
    return calculator.calculate(age, respiratory_hospitalization, fvc_percent_predicted, change_fvc_24_weeks)