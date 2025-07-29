"""
Altitude-Adjusted PERC Rule Calculator

Rules out pulmonary embolism if no criteria are present; includes adjustment 
for high altitude (>4000 ft) by removing oxygen saturation criterion.

References:
1. Wolf SJ, et al. Am J Emerg Med. 2008;26(2):181-5.
2. Kline JA, et al. J Thromb Haemost. 2004;2(8):1247-55.
"""

from typing import Dict, Any


class AltitudeAdjustedPercCalculator:
    """Calculator for Altitude-Adjusted PERC Rule"""
    
    def __init__(self):
        # This is a rule-out criteria, so we count positive criteria
        pass
    
    def calculate(self, high_altitude: str, age_50_or_older: str, hr_100_or_greater: str,
                  unilateral_leg_swelling: str, hemoptysis: str, recent_surgery_trauma: str,
                  prior_pe_dvt: str, hormone_use: str) -> Dict[str, Any]:
        """
        Calculates the Altitude-Adjusted PERC Rule
        
        Args:
            high_altitude (str): "yes" if patient lives at >4000 ft altitude
            age_50_or_older (str): "yes" if age ≥50 years
            hr_100_or_greater (str): "yes" if HR ≥100 bpm
            unilateral_leg_swelling (str): "yes" if present
            hemoptysis (str): "yes" if present
            recent_surgery_trauma (str): "yes" if surgery/trauma ≤4 weeks requiring general anesthesia
            prior_pe_dvt (str): "yes" if prior history of PE or DVT
            hormone_use (str): "yes" if on oral contraceptives, HRT, or estrogenic hormones
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(high_altitude, age_50_or_older, hr_100_or_greater,
                            unilateral_leg_swelling, hemoptysis, recent_surgery_trauma,
                            prior_pe_dvt, hormone_use)
        
        # Check if patient is at high altitude (required for this rule)
        if high_altitude != "yes":
            raise ValueError("Altitude-Adjusted PERC Rule is only applicable for patients living at high altitude (>4000 ft)")
        
        # Count positive criteria (excluding high_altitude which is a prerequisite)
        positive_criteria = self._count_positive_criteria(
            age_50_or_older, hr_100_or_greater, unilateral_leg_swelling,
            hemoptysis, recent_surgery_trauma, prior_pe_dvt, hormone_use
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(positive_criteria)
        
        return {
            "result": "PERC Negative" if positive_criteria == 0 else "PERC Positive",
            "unit": "recommendation",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "positive_criteria_count": positive_criteria,
            "perc_satisfied": positive_criteria == 0
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        parameter_names = [
            "high_altitude", "age_50_or_older", "hr_100_or_greater",
            "unilateral_leg_swelling", "hemoptysis", "recent_surgery_trauma",
            "prior_pe_dvt", "hormone_use"
        ]
        
        for i, arg in enumerate(args):
            if arg not in valid_options:
                raise ValueError(f"{parameter_names[i]} must be 'yes' or 'no'")
    
    def _count_positive_criteria(self, age_50_or_older: str, hr_100_or_greater: str,
                               unilateral_leg_swelling: str, hemoptysis: str,
                               recent_surgery_trauma: str, prior_pe_dvt: str,
                               hormone_use: str) -> int:
        """Counts the number of positive PERC criteria"""
        
        criteria = [
            age_50_or_older,
            hr_100_or_greater,
            unilateral_leg_swelling,
            hemoptysis,
            recent_surgery_trauma,
            prior_pe_dvt,
            hormone_use
        ]
        
        return sum(1 for criterion in criteria if criterion == "yes")
    
    def _get_interpretation(self, positive_criteria: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the number of positive criteria
        
        Args:
            positive_criteria (int): Number of positive PERC criteria
            
        Returns:
            Dict with interpretation details
        """
        
        if positive_criteria == 0:
            return {
                "stage": "PERC Negative",
                "description": "No criteria present - PE ruled out",
                "interpretation": "PERC rule criteria satisfied. No need for further workup, as <2% chance of PE. Patient can be safely discharged without additional testing for PE if clinician's pretest probability is <15%."
            }
        else:
            return {
                "stage": "PERC Positive",
                "description": "One or more criteria present",
                "interpretation": f"PERC rule not satisfied ({positive_criteria} criteria present). Further workup for PE is indicated as one or more criteria are present. Consider D-dimer, CT pulmonary angiogram, or other appropriate diagnostic testing based on clinical judgment and pretest probability."
            }


def calculate_altitude_adjusted_perc(high_altitude: str, age_50_or_older: str,
                                   hr_100_or_greater: str, unilateral_leg_swelling: str,
                                   hemoptysis: str, recent_surgery_trauma: str,
                                   prior_pe_dvt: str, hormone_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AltitudeAdjustedPercCalculator()
    return calculator.calculate(high_altitude, age_50_or_older, hr_100_or_greater,
                              unilateral_leg_swelling, hemoptysis, recent_surgery_trauma,
                              prior_pe_dvt, hormone_use)