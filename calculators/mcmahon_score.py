"""
McMahon Score for Rhabdomyolysis Calculator

Predicts mortality or acute kidney injury (AKI) requiring renal replacement therapy 
in hospitalized rhabdomyolysis patients.

Reference:
McMahon GM, Zeng X, Waikar SS. A risk prediction score for kidney failure or mortality 
in rhabdomyolysis. JAMA Intern Med. 2013 Oct 28;173(19):1821-8.
"""

from typing import Dict, Any


class McMahonScoreCalculator:
    """Calculator for McMahon Score for Rhabdomyolysis"""
    
    def __init__(self):
        # Age scoring
        self.AGE_SCORES = {
            "<=50": 0,
            "51-70": 1.5,
            "71-80": 2.5,
            ">80": 3
        }
        
        # Sex scoring
        self.SEX_SCORES = {
            "male": 0,
            "female": 1
        }
        
        # Initial creatinine scoring
        self.CREATININE_SCORES = {
            "<1.4": 0,
            "1.4-2.2": 1.5,
            ">2.2": 3
        }
        
        # Initial phosphate scoring
        self.PHOSPHATE_SCORES = {
            "<4.0": 0,
            "4.0-5.4": 1.5,
            ">5.4": 3
        }
        
        # Binary parameter scores
        self.CALCIUM_LOW_SCORE = 2  # If initial calcium <7.5 mg/dL
        self.CPK_HIGH_SCORE = 2     # If initial CPK >40,000 U/L
        self.BICARBONATE_LOW_SCORE = 2  # If initial bicarbonate <19 mEq/L
        
        # Rhabdo cause scoring
        self.RHABDO_CAUSE_SCORES = {
            "known_causes": 0,  # Seizures, syncope, exercise, statins, myositis
            "other_causes": 3
        }
    
    def calculate(self, age: str, sex: str, initial_creatinine: str, 
                  initial_calcium_low: str, initial_cpk_high: str, 
                  rhabdo_cause: str, initial_phosphate: str, 
                  initial_bicarbonate_low: str) -> Dict[str, Any]:
        """
        Calculates the McMahon Score using the provided parameters
        
        Args:
            age: Age category ("<=50", "51-70", "71-80", ">80")
            sex: Biological sex ("male", "female")
            initial_creatinine: Creatinine category ("<1.4", "1.4-2.2", ">2.2")
            initial_calcium_low: "yes" if <7.5 mg/dL, "no" otherwise
            initial_cpk_high: "yes" if >40,000 U/L, "no" otherwise
            rhabdo_cause: "known_causes" or "other_causes"
            initial_phosphate: Phosphate category ("<4.0", "4.0-5.4", ">5.4")
            initial_bicarbonate_low: "yes" if <19 mEq/L, "no" otherwise
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, initial_creatinine, initial_calcium_low, 
                            initial_cpk_high, rhabdo_cause, initial_phosphate, 
                            initial_bicarbonate_low)
        
        # Calculate score
        score = 0
        
        # Add age points
        score += self.AGE_SCORES[age]
        
        # Add sex points
        score += self.SEX_SCORES[sex]
        
        # Add creatinine points
        score += self.CREATININE_SCORES[initial_creatinine]
        
        # Add calcium points
        if initial_calcium_low == "yes":
            score += self.CALCIUM_LOW_SCORE
        
        # Add CPK points
        if initial_cpk_high == "yes":
            score += self.CPK_HIGH_SCORE
        
        # Add rhabdo cause points
        score += self.RHABDO_CAUSE_SCORES[rhabdo_cause]
        
        # Add phosphate points
        score += self.PHOSPHATE_SCORES[initial_phosphate]
        
        # Add bicarbonate points
        if initial_bicarbonate_low == "yes":
            score += self.BICARBONATE_LOW_SCORE
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, sex: str, initial_creatinine: str, 
                        initial_calcium_low: str, initial_cpk_high: str, 
                        rhabdo_cause: str, initial_phosphate: str, 
                        initial_bicarbonate_low: str):
        """Validates input parameters"""
        
        # Validate age
        if age not in self.AGE_SCORES:
            raise ValueError(f"Invalid age category: {age}. Must be one of: {list(self.AGE_SCORES.keys())}")
        
        # Validate sex
        if sex not in self.SEX_SCORES:
            raise ValueError(f"Invalid sex: {sex}. Must be 'male' or 'female'")
        
        # Validate creatinine
        if initial_creatinine not in self.CREATININE_SCORES:
            raise ValueError(f"Invalid creatinine category: {initial_creatinine}. Must be one of: {list(self.CREATININE_SCORES.keys())}")
        
        # Validate binary parameters
        binary_params = {
            "initial_calcium_low": initial_calcium_low,
            "initial_cpk_high": initial_cpk_high,
            "initial_bicarbonate_low": initial_bicarbonate_low
        }
        
        for param_name, param_value in binary_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"Invalid {param_name}: {param_value}. Must be 'yes' or 'no'")
        
        # Validate rhabdo cause
        if rhabdo_cause not in self.RHABDO_CAUSE_SCORES:
            raise ValueError(f"Invalid rhabdo cause: {rhabdo_cause}. Must be 'known_causes' or 'other_causes'")
        
        # Validate phosphate
        if initial_phosphate not in self.PHOSPHATE_SCORES:
            raise ValueError(f"Invalid phosphate category: {initial_phosphate}. Must be one of: {list(self.PHOSPHATE_SCORES.keys())}")
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the calculated score
        
        Args:
            score (float): Calculated McMahon score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 6:
            return {
                "stage": "Low Risk",
                "description": "Low risk for death or AKI requiring RRT",
                "interpretation": "3% risk of death or acute kidney injury requiring renal replacement therapy. Consider standard supportive care with fluid resuscitation and monitoring."
            }
        else:
            return {
                "stage": "Not Low Risk",
                "description": "Not low risk for adverse outcomes",
                "interpretation": "Increased risk of death or acute kidney injury requiring renal replacement therapy. Consider aggressive renal protective therapy including high-volume fluid resuscitation, close monitoring of renal function, and early nephrology consultation."
            }


def calculate_mcmahon_score(age: str, sex: str, initial_creatinine: str, 
                           initial_calcium_low: str, initial_cpk_high: str, 
                           rhabdo_cause: str, initial_phosphate: str, 
                           initial_bicarbonate_low: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_mcmahon_score pattern
    """
    calculator = McMahonScoreCalculator()
    return calculator.calculate(age, sex, initial_creatinine, initial_calcium_low, 
                               initial_cpk_high, rhabdo_cause, initial_phosphate, 
                               initial_bicarbonate_low)