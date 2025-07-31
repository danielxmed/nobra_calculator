"""
GAP Index for Idiopathic Pulmonary Fibrosis (IPF) Mortality Calculator

Provides mortality risk stratification for IPF patients using Gender, Age, and Physiology.

References:
1. Ley B, Ryerson CJ, Vittinghoff E, et al. A multidimensional index and staging system 
   for idiopathic pulmonary fibrosis. Ann Intern Med. 2012;156(10):684-91. 
   doi: 10.7326/0003-4819-156-10-201205150-00004.
2. Ryerson CJ, Vittinghoff E, Ley B, et al. Predicting survival across chronic interstitial 
   lung disease: the ILD-GAP model. Chest. 2014;145(4):723-8. doi: 10.1378/chest.13-1474.
3. Paterniti MO, Bi Y, Rekić D, et al. Acute Exacerbation and Decline in Forced Vital 
   Capacity Are Associated with Increased Mortality in Idiopathic Pulmonary Fibrosis. 
   Ann Am Thorac Soc. 2017;14(9):1395-1402. doi: 10.1513/AnnalsATS.201606-458OC.

The GAP Index is a validated prognostic tool that stratifies IPF patients into three 
mortality risk categories using four clinical variables.
"""

from typing import Dict, Any, Optional


class GapIndexIpfMortalityCalculator:
    """Calculator for GAP Index IPF Mortality Assessment"""
    
    def __init__(self):
        # GAP scoring system points
        self.GENDER_POINTS = {
            "female": 0,
            "male": 1
        }
        
        self.AGE_POINTS = [
            (60, 0),    # ≤60 years: 0 points
            (65, 1),    # 61-65 years: 1 point
            (float('inf'), 2)  # >65 years: 2 points
        ]
        
        self.FVC_POINTS = [
            (75, 0),    # >75%: 0 points
            (50, 1),    # 50-75%: 1 point
            (0, 2)      # <50%: 2 points
        ]
        
        self.DLCO_POINTS = [
            (55, 0),    # >55%: 0 points
            (36, 1),    # 36-55%: 1 point
            (0, 2),     # ≤35%: 2 points
            # Cannot perform: 3 points (handled separately)
        ]
        
        # GAP staging thresholds
        self.GAP_STAGES = [
            (3, "GAP Stage I", "Low mortality risk"),
            (5, "GAP Stage II", "Intermediate mortality risk"),
            (8, "GAP Stage III", "High mortality risk")
        ]
    
    def calculate(self, gender: str, age: int, fvc_percent_predicted: float, 
                  dlco_percent_predicted: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates GAP Index for IPF mortality prediction
        
        Args:
            gender (str): Patient's gender ('male' or 'female')
            age (int): Patient's age in years
            fvc_percent_predicted (float): FVC as percentage of predicted (%)
            dlco_percent_predicted (Optional[float]): DLCO as percentage of predicted (%), 
                                                     None if cannot perform test
            
        Returns:
            Dict with GAP score, stage, and clinical recommendations
        """
        
        # Validations
        self._validate_inputs(gender, age, fvc_percent_predicted, dlco_percent_predicted)
        
        # Calculate individual component scores
        gender_score = self._calculate_gender_score(gender)
        age_score = self._calculate_age_score(age)
        fvc_score = self._calculate_fvc_score(fvc_percent_predicted)
        dlco_score = self._calculate_dlco_score(dlco_percent_predicted)
        
        # Calculate total GAP score
        gap_score = gender_score + age_score + fvc_score + dlco_score
        
        # Determine GAP stage and interpretation
        interpretation = self._get_interpretation(gap_score)
        
        return {
            "result": gap_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, gender: str, age: int, fvc_percent_predicted: float, 
                        dlco_percent_predicted: Optional[float]):
        """Validates input parameters"""
        
        if gender not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'")
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if not isinstance(fvc_percent_predicted, (int, float)) or fvc_percent_predicted < 10 or fvc_percent_predicted > 150:
            raise ValueError("FVC percent predicted must be between 10 and 150%")
        
        if dlco_percent_predicted is not None:
            if not isinstance(dlco_percent_predicted, (int, float)) or dlco_percent_predicted < 5 or dlco_percent_predicted > 150:
                raise ValueError("DLCO percent predicted must be between 5 and 150% or None if cannot perform")
    
    def _calculate_gender_score(self, gender: str) -> int:
        """Calculates gender component score"""
        return self.GENDER_POINTS[gender]
    
    def _calculate_age_score(self, age: int) -> int:
        """Calculates age component score"""
        for threshold, points in self.AGE_POINTS:
            if age <= threshold:
                return points
        return self.AGE_POINTS[-1][1]  # Fallback to highest score
    
    def _calculate_fvc_score(self, fvc_percent: float) -> int:
        """Calculates FVC component score"""
        for threshold, points in self.FVC_POINTS:
            if fvc_percent > threshold:
                return points
        return self.FVC_POINTS[-1][1]  # Fallback to highest score
    
    def _calculate_dlco_score(self, dlco_percent: Optional[float]) -> int:
        """Calculates DLCO component score"""
        # Cannot perform test = 3 points (most severe)
        if dlco_percent is None:
            return 3
        
        # ≤35%: 2 points
        if dlco_percent <= 35:
            return 2
        
        # 36-55%: 1 point
        if dlco_percent <= 55:
            return 1
        
        # >55%: 0 points
        return 0
    
    def _get_interpretation(self, gap_score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on GAP score
        
        Args:
            gap_score (int): Calculated GAP score (0-8 points)
            
        Returns:
            Dict with interpretation
        """
        
        # Determine GAP stage
        for threshold, stage, description in self.GAP_STAGES:
            if gap_score <= threshold:
                if stage == "GAP Stage I":
                    return {
                        "stage": stage,
                        "description": description,
                        "interpretation": (f"GAP score of {gap_score} indicates {description.lower()}. "
                                        f"Close monitoring every 6 months for evidence of disease progression. "
                                        f"Aggressive management of symptoms and comorbid conditions recommended. "
                                        f"May not require immediate listing for lung transplantation. "
                                        f"Continue antifibrotic therapy if indicated. Focus on maintaining "
                                        f"functional status and quality of life.")
                    }
                elif stage == "GAP Stage II":
                    return {
                        "stage": stage,
                        "description": description,
                        "interpretation": (f"GAP score of {gap_score} indicates {description.lower()}. "
                                        f"Close monitoring every 3-6 months for evidence of disease progression. "
                                        f"Consider lung transplant evaluation if appropriate candidate. "
                                        f"Optimize medical management including antifibrotic therapy. "
                                        f"Pulmonary rehabilitation and oxygen therapy as needed. "
                                        f"Discussion of prognosis and advance care planning recommended.")
                    }
                else:  # GAP Stage III
                    return {
                        "stage": stage,
                        "description": description,
                        "interpretation": (f"GAP score of {gap_score} indicates {description.lower()}. "
                                        f"Frequent monitoring every 3 months or less. Urgent lung transplant "
                                        f"evaluation recommended if appropriate candidate. Palliative care "
                                        f"consultation may be appropriate. Aggressive symptom management including "
                                        f"oxygen therapy, opioids for dyspnea, and pulmonary rehabilitation. "
                                        f"Advance care planning discussions essential.")
                    }
        
        # Fallback (should not reach here with valid input)
        return {
            "stage": "GAP Stage III",
            "description": "High mortality risk",
            "interpretation": f"GAP score of {gap_score} indicates high mortality risk requiring urgent evaluation."
        }


def calculate_gap_index_ipf_mortality(gender: str, age: int, fvc_percent_predicted: float, 
                                     dlco_percent_predicted: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gap_index_ipf_mortality pattern
    """
    calculator = GapIndexIpfMortalityCalculator()
    return calculator.calculate(gender, age, fvc_percent_predicted, dlco_percent_predicted)