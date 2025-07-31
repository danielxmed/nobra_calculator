"""
Dual Antiplatelet Therapy (DAPT) Score Calculator

Predicts which patients will benefit from prolonged DAPT after coronary stent placement.
Developed from the DAPT Study randomized trial to predict combined ischemic and 
bleeding risk for patients being considered for continued thienopyridine therapy beyond 1 year.

References:
1. Yeh RW, Secemsky EA, Kereiakes DJ, Normand SLT, Gershlick AH, Cohen DJ, et al. 
   Development and Validation of a Prediction Rule for Benefit and Harm of Dual 
   Antiplatelet Therapy Beyond 1 Year After Percutaneous Coronary Intervention. 
   JAMA. 2016;315(16):1735-49.
2. Levine GN, Bates ER, Bittl JA, Brindis RG, Fihn SD, Fleisher LA, et al. 
   2016 ACC/AHA Guideline Focused Update on Duration of Dual Antiplatelet Therapy 
   in Patients With Coronary Artery Disease. Circulation. 2016;134(10):e123-55.
"""

from typing import Dict, Any


class DaptScoreCalculator:
    """Calculator for Dual Antiplatelet Therapy (DAPT) Score"""
    
    def __init__(self):
        # DAPT Score components and point values
        self.AGE_THRESHOLDS = {
            (0, 64): 0,      # <65 years: 0 points
            (65, 74): -1,    # 65-74 years: -1 point
            (75, 120): -2    # ≥75 years: -2 points
        }
        
        # Clinical factors and their point values
        self.DIABETES_POINTS = 1           # Diabetes mellitus: +1 point
        self.SMOKING_POINTS = 1            # Current smoking: +1 point
        self.PRIOR_MI_PCI_POINTS = 1       # Prior MI or PCI: +1 point
        self.SMALL_STENT_POINTS = 1        # Stent diameter <3mm: +1 point
        self.CHF_LOW_EF_POINTS = 2         # CHF or LVEF <30%: +2 points
        self.VEIN_GRAFT_PCI_POINTS = 2     # Vein graft PCI: +2 points
        self.PACLITAXEL_STENT_POINTS = -1  # Paclitaxel-eluting stent: -1 point
        self.MI_PRESENTATION_POINTS = 1    # MI at presentation: +1 point
    
    def calculate(self, age: int, diabetes_mellitus: str, current_smoking: str,
                  prior_mi_or_pci: str, stent_diameter_small: str, chf_or_low_ef: str,
                  vein_graft_pci: str, paclitaxel_eluting_stent: str, 
                  mi_at_presentation: str) -> Dict[str, Any]:
        """
        Calculates the DAPT Score
        
        Args:
            age (int): Patient age in years
            diabetes_mellitus (str): History of diabetes mellitus ("yes"/"no")
            current_smoking (str): Current cigarette smoking ("yes"/"no")
            prior_mi_or_pci (str): Prior MI or PCI ("yes"/"no")
            stent_diameter_small (str): Stent diameter <3 mm ("yes"/"no")
            chf_or_low_ef (str): CHF or LVEF <30% ("yes"/"no")
            vein_graft_pci (str): Saphenous vein graft PCI ("yes"/"no")
            paclitaxel_eluting_stent (str): Paclitaxel-eluting stent ("yes"/"no")
            mi_at_presentation (str): MI at presentation ("yes"/"no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'age': age,
            'diabetes_mellitus': diabetes_mellitus,
            'current_smoking': current_smoking,
            'prior_mi_or_pci': prior_mi_or_pci,
            'stent_diameter_small': stent_diameter_small,
            'chf_or_low_ef': chf_or_low_ef,
            'vein_graft_pci': vein_graft_pci,
            'paclitaxel_eluting_stent': paclitaxel_eluting_stent,
            'mi_at_presentation': mi_at_presentation
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate score components
        age_points = self._calculate_age_points(age)
        clinical_points = self._calculate_clinical_points(parameters)
        
        # Calculate total score
        total_score = age_points + clinical_points
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        # Age validation
        age = parameters['age']
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        # Yes/no parameters validation
        yes_no_params = [
            'diabetes_mellitus', 'current_smoking', 'prior_mi_or_pci',
            'stent_diameter_small', 'chf_or_low_ef', 'vein_graft_pci',
            'paclitaxel_eluting_stent', 'mi_at_presentation'
        ]
        
        for param_name in yes_no_params:
            value = parameters[param_name]
            if not isinstance(value, str) or value.lower() not in ["yes", "no"]:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no'")
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculates points based on age"""
        
        for (min_age, max_age), points in self.AGE_THRESHOLDS.items():
            if min_age <= age <= max_age:
                return points
        
        # Fallback (should not reach here with proper validation)
        return 0
    
    def _calculate_clinical_points(self, parameters: Dict[str, Any]) -> int:
        """Calculates points based on clinical factors"""
        
        points = 0
        
        # Diabetes mellitus
        if parameters['diabetes_mellitus'].lower() == 'yes':
            points += self.DIABETES_POINTS
        
        # Current smoking
        if parameters['current_smoking'].lower() == 'yes':
            points += self.SMOKING_POINTS
        
        # Prior MI or PCI
        if parameters['prior_mi_or_pci'].lower() == 'yes':
            points += self.PRIOR_MI_PCI_POINTS
        
        # Small stent diameter
        if parameters['stent_diameter_small'].lower() == 'yes':
            points += self.SMALL_STENT_POINTS
        
        # CHF or low EF
        if parameters['chf_or_low_ef'].lower() == 'yes':
            points += self.CHF_LOW_EF_POINTS
        
        # Vein graft PCI
        if parameters['vein_graft_pci'].lower() == 'yes':
            points += self.VEIN_GRAFT_PCI_POINTS
        
        # Paclitaxel-eluting stent (negative points)
        if parameters['paclitaxel_eluting_stent'].lower() == 'yes':
            points += self.PACLITAXEL_STENT_POINTS
        
        # MI at presentation
        if parameters['mi_at_presentation'].lower() == 'yes':
            points += self.MI_PRESENTATION_POINTS
        
        return points
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            score (int): Total DAPT score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 2:
            return {
                "stage": "Low Score (<2)",
                "description": "Unfavorable benefit/risk ratio",
                "interpretation": "DAPT score <2 indicates unfavorable benefit/risk ratio for prolonged DAPT. High bleeding risk and low ischemic risk. Consider discontinuing DAPT at 12 months. NNT to prevent ischemic event: 169, NNH to cause bleeding: 69."
            }
        else:  # score >= 2
            return {
                "stage": "High Score (≥2)",
                "description": "Favorable benefit/risk ratio",
                "interpretation": "DAPT score ≥2 indicates favorable benefit/risk ratio for prolonged DAPT. High ischemic risk and low bleeding risk. Consider continuing DAPT beyond 12 months. NNT to prevent ischemic event: 33, NNH to cause bleeding: 263."
            }


def calculate_dapt_score(age: int, diabetes_mellitus: str, current_smoking: str,
                        prior_mi_or_pci: str, stent_diameter_small: str, chf_or_low_ef: str,
                        vein_graft_pci: str, paclitaxel_eluting_stent: str, 
                        mi_at_presentation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dapt_score pattern
    """
    calculator = DaptScoreCalculator()
    return calculator.calculate(
        age, diabetes_mellitus, current_smoking, prior_mi_or_pci,
        stent_diameter_small, chf_or_low_ef, vein_graft_pci,
        paclitaxel_eluting_stent, mi_at_presentation
    )