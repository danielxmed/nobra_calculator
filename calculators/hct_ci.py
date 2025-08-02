"""
Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI) Calculator

Predicts survival after HCT in patients with hematologic malignancies.
Includes optional age adjustment based on Sorror 2014.

References:
- Sorror ML, et al. Blood. 2005;106(8):2912-9.
- Sorror ML, et al. J Clin Oncol. 2014;32(29):3249-56.
"""

from typing import Dict, Any


class HctCiCalculator:
    """Calculator for Hematopoietic Cell Transplantation-specific Comorbidity Index"""
    
    def __init__(self):
        # Comorbidity scoring weights
        self.COMORBIDITY_SCORES = {
            # 1-point comorbidities
            "arrhythmia": {"none": 0, "present": 1},
            "cardiac": {"none": 0, "cad_chf_mi_ef": 1, "valve_disease": 3},
            "inflammatory_bowel": {"none": 0, "present": 1},
            "diabetes": {"none_or_diet": 0, "treated": 1},
            "cerebrovascular": {"none": 0, "present": 1},
            "psychiatric": {"none": 0, "requiring_treatment": 1},
            "hepatic": {"none": 0, "mild": 1, "moderate_severe": 3},
            "obesity": {"no": 0, "yes": 1},
            "infection": {"none": 0, "requiring_treatment": 1},
            # 2-point comorbidities
            "rheumatologic": {"none": 0, "present": 2},
            "peptic_ulcer": {"none_or_no_treatment": 0, "requiring_treatment": 2},
            "renal": {"none_or_mild": 0, "moderate_severe": 2},
            # 2-3 point comorbidity
            "pulmonary": {"none_or_mild": 0, "moderate": 2, "severe": 3},
            # 3-point comorbidity
            "prior_solid_tumor": {"no": 0, "yes": 3}
        }
        
        # Age adjustment threshold (Sorror 2014)
        self.AGE_THRESHOLD = 40
        self.AGE_ADJUSTMENT_POINTS = 1
    
    def calculate(self, arrhythmia: str, cardiac: str, inflammatory_bowel: str,
                 diabetes: str, cerebrovascular: str, psychiatric: str,
                 hepatic: str, obesity: str, infection: str,
                 rheumatologic: str, peptic_ulcer: str, renal: str,
                 pulmonary: str, prior_solid_tumor: str,
                 include_age: str, age: int = None) -> Dict[str, Any]:
        """
        Calculates the HCT-CI score with optional age adjustment
        
        Args:
            arrhythmia: History of arrhythmia (none/present)
            cardiac: Cardiac dysfunction (none/cad_chf_mi_ef/valve_disease)
            inflammatory_bowel: IBD (none/present)
            diabetes: Diabetes status (none_or_diet/treated)
            cerebrovascular: Cerebrovascular disease (none/present)
            psychiatric: Psychiatric disturbance (none/requiring_treatment)
            hepatic: Hepatic dysfunction (none/mild/moderate_severe)
            obesity: BMI > 35 (no/yes)
            infection: Infection requiring treatment after day 0 (none/requiring_treatment)
            rheumatologic: Rheumatologic disease (none/present)
            peptic_ulcer: Peptic ulcer (none_or_no_treatment/requiring_treatment)
            renal: Renal dysfunction (none_or_mild/moderate_severe)
            pulmonary: Pulmonary dysfunction (none_or_mild/moderate/severe)
            prior_solid_tumor: Prior solid tumor (no/yes)
            include_age: Include age adjustment (no/yes)
            age: Patient age in years (required if include_age is yes)
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(arrhythmia, cardiac, inflammatory_bowel, diabetes,
                            cerebrovascular, psychiatric, hepatic, obesity,
                            infection, rheumatologic, peptic_ulcer, renal,
                            pulmonary, prior_solid_tumor, include_age, age)
        
        # Calculate base comorbidity score
        score = self._calculate_comorbidity_score(
            arrhythmia, cardiac, inflammatory_bowel, diabetes,
            cerebrovascular, psychiatric, hepatic, obesity,
            infection, rheumatologic, peptic_ulcer, renal,
            pulmonary, prior_solid_tumor
        )
        
        # Add age adjustment if requested
        if include_age == "yes" and age is not None and age >= self.AGE_THRESHOLD:
            score += self.AGE_ADJUSTMENT_POINTS
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, arrhythmia: str, cardiac: str, inflammatory_bowel: str,
                        diabetes: str, cerebrovascular: str, psychiatric: str,
                        hepatic: str, obesity: str, infection: str,
                        rheumatologic: str, peptic_ulcer: str, renal: str,
                        pulmonary: str, prior_solid_tumor: str,
                        include_age: str, age: int = None):
        """Validates input parameters"""
        
        # Validate comorbidity inputs
        comorbidities = {
            "arrhythmia": arrhythmia,
            "cardiac": cardiac,
            "inflammatory_bowel": inflammatory_bowel,
            "diabetes": diabetes,
            "cerebrovascular": cerebrovascular,
            "psychiatric": psychiatric,
            "hepatic": hepatic,
            "obesity": obesity,
            "infection": infection,
            "rheumatologic": rheumatologic,
            "peptic_ulcer": peptic_ulcer,
            "renal": renal,
            "pulmonary": pulmonary,
            "prior_solid_tumor": prior_solid_tumor
        }
        
        for comorbidity, value in comorbidities.items():
            if value not in self.COMORBIDITY_SCORES[comorbidity]:
                valid_values = list(self.COMORBIDITY_SCORES[comorbidity].keys())
                raise ValueError(f"{comorbidity} must be one of {valid_values}")
        
        # Validate age adjustment inputs
        if include_age not in ["no", "yes"]:
            raise ValueError("include_age must be 'no' or 'yes'")
        
        if include_age == "yes":
            if age is None:
                raise ValueError("Age is required when age adjustment is included")
            if not isinstance(age, (int, float)):
                raise ValueError("Age must be a number")
            if age < 0 or age > 100:
                raise ValueError("Age must be between 0 and 100")
    
    def _calculate_comorbidity_score(self, arrhythmia: str, cardiac: str,
                                    inflammatory_bowel: str, diabetes: str,
                                    cerebrovascular: str, psychiatric: str,
                                    hepatic: str, obesity: str, infection: str,
                                    rheumatologic: str, peptic_ulcer: str,
                                    renal: str, pulmonary: str,
                                    prior_solid_tumor: str) -> int:
        """Calculates the total comorbidity score"""
        
        score = 0
        
        # Sum all comorbidity scores
        score += self.COMORBIDITY_SCORES["arrhythmia"][arrhythmia]
        score += self.COMORBIDITY_SCORES["cardiac"][cardiac]
        score += self.COMORBIDITY_SCORES["inflammatory_bowel"][inflammatory_bowel]
        score += self.COMORBIDITY_SCORES["diabetes"][diabetes]
        score += self.COMORBIDITY_SCORES["cerebrovascular"][cerebrovascular]
        score += self.COMORBIDITY_SCORES["psychiatric"][psychiatric]
        score += self.COMORBIDITY_SCORES["hepatic"][hepatic]
        score += self.COMORBIDITY_SCORES["obesity"][obesity]
        score += self.COMORBIDITY_SCORES["infection"][infection]
        score += self.COMORBIDITY_SCORES["rheumatologic"][rheumatologic]
        score += self.COMORBIDITY_SCORES["peptic_ulcer"][peptic_ulcer]
        score += self.COMORBIDITY_SCORES["renal"][renal]
        score += self.COMORBIDITY_SCORES["pulmonary"][pulmonary]
        score += self.COMORBIDITY_SCORES["prior_solid_tumor"][prior_solid_tumor]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category based on the total score
        
        Args:
            score (int): Total HCT-CI score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Score 0",
                "interpretation": "Low risk group. Non-relapse mortality approximately 14% at 2 years. Good candidate for transplantation."
            }
        elif score <= 2:
            return {
                "stage": "Intermediate Risk",
                "description": "Score 1-2",
                "interpretation": "Intermediate risk group. Non-relapse mortality approximately 21% at 2 years. Consider risk-benefit assessment for transplantation."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Score ≥3",
                "interpretation": "High risk group. Non-relapse mortality approximately 41% at 2 years. Consider alternative therapies or risk-adapted conditioning regimens."
            }


def calculate_hct_ci(arrhythmia: str, cardiac: str, inflammatory_bowel: str,
                    diabetes: str, cerebrovascular: str, psychiatric: str,
                    hepatic: str, obesity: str, infection: str,
                    rheumatologic: str, peptic_ulcer: str, renal: str,
                    pulmonary: str, prior_solid_tumor: str,
                    include_age: str, age: int = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_hct_ci pattern
    """
    calculator = HctCiCalculator()
    return calculator.calculate(
        arrhythmia, cardiac, inflammatory_bowel, diabetes,
        cerebrovascular, psychiatric, hepatic, obesity,
        infection, rheumatologic, peptic_ulcer, renal,
        pulmonary, prior_solid_tumor, include_age, age
    )