"""
HEMORR₂HAGES Score for Major Bleeding Risk Calculator

Quantifies hemorrhage risk in elderly patients with atrial fibrillation on anticoagulation.

References:
- Gage BF, et al. Am Heart J. 2006;151(3):713-9.
- Apostolakis S, et al. J Am Coll Cardiol. 2012;60(9):861-7.
"""

from typing import Dict, Any


class Hemorr2hagesCalculator:
    """Calculator for HEMORR₂HAGES Score for Major Bleeding Risk"""
    
    def __init__(self):
        # Scoring weights for each criterion
        self.SCORING_WEIGHTS = {
            "hepatic_renal_disease": {"no": 0, "yes": 1},
            "ethanol_abuse": {"no": 0, "yes": 1},
            "malignancy": {"no": 0, "yes": 1},
            "older_age": {"no": 0, "yes": 1},
            "reduced_platelet": {"no": 0, "yes": 1},
            "rebleeding": {"no": 0, "yes": 2},  # Worth 2 points
            "hypertension": {"no": 0, "yes": 1},
            "anemia": {"no": 0, "yes": 1},
            "genetic_factors": {"no": 0, "yes": 1},
            "excessive_fall_risk": {"no": 0, "yes": 1},
            "stroke": {"no": 0, "yes": 1}
        }
    
    def calculate(self, hepatic_renal_disease: str, ethanol_abuse: str,
                 malignancy: str, older_age: str, reduced_platelet: str,
                 rebleeding: str, hypertension: str, anemia: str,
                 genetic_factors: str, excessive_fall_risk: str,
                 stroke: str) -> Dict[str, Any]:
        """
        Calculates the HEMORR₂HAGES score
        
        Args:
            hepatic_renal_disease: Hepatic or renal disease (no/yes)
            ethanol_abuse: Ethanol (alcohol) abuse (no/yes)
            malignancy: Malignancy history (no/yes)
            older_age: Age >75 years (no/yes)
            reduced_platelet: Reduced platelet count/function (no/yes)
            rebleeding: Prior major bleed (no/yes)
            hypertension: Uncontrolled hypertension (no/yes)
            anemia: Hgb <13 men, <12 women (no/yes)
            genetic_factors: CYP 2C9 polymorphisms (no/yes)
            excessive_fall_risk: Excessive fall risk (no/yes)
            stroke: Stroke history (no/yes)
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            hepatic_renal_disease, ethanol_abuse, malignancy,
            older_age, reduced_platelet, rebleeding,
            hypertension, anemia, genetic_factors,
            excessive_fall_risk, stroke
        )
        
        # Calculate total score
        score = self._calculate_score(
            hepatic_renal_disease, ethanol_abuse, malignancy,
            older_age, reduced_platelet, rebleeding,
            hypertension, anemia, genetic_factors,
            excessive_fall_risk, stroke
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hepatic_renal_disease: str, ethanol_abuse: str,
                        malignancy: str, older_age: str, reduced_platelet: str,
                        rebleeding: str, hypertension: str, anemia: str,
                        genetic_factors: str, excessive_fall_risk: str,
                        stroke: str):
        """Validates input parameters"""
        
        criteria = {
            "hepatic_renal_disease": hepatic_renal_disease,
            "ethanol_abuse": ethanol_abuse,
            "malignancy": malignancy,
            "older_age": older_age,
            "reduced_platelet": reduced_platelet,
            "rebleeding": rebleeding,
            "hypertension": hypertension,
            "anemia": anemia,
            "genetic_factors": genetic_factors,
            "excessive_fall_risk": excessive_fall_risk,
            "stroke": stroke
        }
        
        for criterion, value in criteria.items():
            if value not in ["no", "yes"]:
                raise ValueError(f"{criterion} must be 'no' or 'yes'")
    
    def _calculate_score(self, hepatic_renal_disease: str, ethanol_abuse: str,
                        malignancy: str, older_age: str, reduced_platelet: str,
                        rebleeding: str, hypertension: str, anemia: str,
                        genetic_factors: str, excessive_fall_risk: str,
                        stroke: str) -> int:
        """Calculates the total HEMORR₂HAGES score"""
        
        score = 0
        
        # Sum all component scores
        score += self.SCORING_WEIGHTS["hepatic_renal_disease"][hepatic_renal_disease]
        score += self.SCORING_WEIGHTS["ethanol_abuse"][ethanol_abuse]
        score += self.SCORING_WEIGHTS["malignancy"][malignancy]
        score += self.SCORING_WEIGHTS["older_age"][older_age]
        score += self.SCORING_WEIGHTS["reduced_platelet"][reduced_platelet]
        score += self.SCORING_WEIGHTS["rebleeding"][rebleeding]  # Worth 2 points
        score += self.SCORING_WEIGHTS["hypertension"][hypertension]
        score += self.SCORING_WEIGHTS["anemia"][anemia]
        score += self.SCORING_WEIGHTS["genetic_factors"][genetic_factors]
        score += self.SCORING_WEIGHTS["excessive_fall_risk"][excessive_fall_risk]
        score += self.SCORING_WEIGHTS["stroke"][stroke]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category based on the total score
        
        Args:
            score (int): Total HEMORR₂HAGES score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Score 0-1",
                "interpretation": "Low risk of major bleeding. The benefit of anticoagulation for stroke prevention in AF likely outweighs the bleeding risk in most patients."
            }
        elif score <= 3:
            return {
                "stage": "Intermediate Risk",
                "description": "Score 2-3",
                "interpretation": "Intermediate risk of major bleeding. Careful assessment of individual risk-benefit ratio is recommended. Consider patient preferences and close monitoring if anticoagulation is initiated."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Score ≥4",
                "interpretation": "High risk of major bleeding. The bleeding risk may outweigh the benefit of anticoagulation in many patients. Consider alternative strategies for stroke prevention or more intensive monitoring if anticoagulation is necessary."
            }


def calculate_hemorr2hages(hepatic_renal_disease: str, ethanol_abuse: str,
                          malignancy: str, older_age: str, reduced_platelet: str,
                          rebleeding: str, hypertension: str, anemia: str,
                          genetic_factors: str, excessive_fall_risk: str,
                          stroke: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_hemorr2hages pattern
    """
    calculator = Hemorr2hagesCalculator()
    return calculator.calculate(
        hepatic_renal_disease, ethanol_abuse, malignancy,
        older_age, reduced_platelet, rebleeding,
        hypertension, anemia, genetic_factors,
        excessive_fall_risk, stroke
    )