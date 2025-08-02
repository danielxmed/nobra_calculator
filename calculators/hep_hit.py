"""
HIT Expert Probability (HEP) Score for Heparin-Induced Thrombocytopenia Calculator

Pre-test clinical scoring model for HIT based on broad expert opinion.

References:
- Cuker A, et al. J Thromb Haemost. 2010;8(12):2642-50.
- Joseph J, et al. Blood Adv. 2018;2(22):3155-3162.
"""

from typing import Dict, Any


class HepHitCalculator:
    """Calculator for HIT Expert Probability (HEP) Score"""
    
    def __init__(self):
        # Point values for each feature
        self.magnitude_points = {
            "less_than_30": -1,
            "30_to_50": 1,
            "greater_than_50": 3
        }
        
        self.timing_points = {
            "less_than_4_days": -1,
            "4_days": 2,
            "5_to_10_days": 3,
            "11_to_14_days": 2,
            "greater_than_14_days": -1
        }
        
        self.nadir_points = {
            "20_or_less": -2,
            "greater_than_20": 2
        }
        
        self.thrombosis_points = {
            "new_vte_ate": 3,
            "progression_vte_ate": 2,
            "none": 0
        }
        
        self.skin_necrosis_points = {
            "yes": 3,
            "no": 0
        }
        
        self.systemic_reaction_points = {
            "yes": 2,
            "no": 0
        }
        
        self.bleeding_points = {
            "yes": -1,
            "no": 0
        }
        
        self.other_causes_points = {
            "definite": -3,
            "possible": -1,
            "none": 0
        }
    
    def calculate(self, magnitude_fall: str, timing_platelet_fall: str,
                  nadir_platelet_count: str, thrombosis: str,
                  skin_necrosis: str, acute_systemic_reaction: str,
                  bleeding: str, other_causes_thrombocytopenia: str) -> Dict[str, Any]:
        """
        Calculates the HEP score for HIT probability
        
        Args:
            magnitude_fall (str): Magnitude of platelet count fall
            timing_platelet_fall (str): Timing of platelet count fall
            nadir_platelet_count (str): Nadir platelet count
            thrombosis (str): Presence of thrombosis
            skin_necrosis (str): Skin necrosis at injection sites
            acute_systemic_reaction (str): Acute systemic reaction after IV heparin
            bleeding (str): Presence of bleeding
            other_causes_thrombocytopenia (str): Other causes of thrombocytopenia
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(magnitude_fall, timing_platelet_fall,
                            nadir_platelet_count, thrombosis,
                            skin_necrosis, acute_systemic_reaction,
                            bleeding, other_causes_thrombocytopenia)
        
        # Calculate total score
        total_score = 0
        
        # Add points for each feature
        total_score += self.magnitude_points[magnitude_fall]
        total_score += self.timing_points[timing_platelet_fall]
        total_score += self.nadir_points[nadir_platelet_count]
        total_score += self.thrombosis_points[thrombosis]
        total_score += self.skin_necrosis_points[skin_necrosis]
        total_score += self.systemic_reaction_points[acute_systemic_reaction]
        total_score += self.bleeding_points[bleeding]
        total_score += self.other_causes_points[other_causes_thrombocytopenia]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, magnitude_fall: str, timing_platelet_fall: str,
                        nadir_platelet_count: str, thrombosis: str,
                        skin_necrosis: str, acute_systemic_reaction: str,
                        bleeding: str, other_causes_thrombocytopenia: str):
        """Validates input parameters"""
        
        if magnitude_fall not in self.magnitude_points:
            raise ValueError(f"Invalid magnitude_fall: {magnitude_fall}")
        
        if timing_platelet_fall not in self.timing_points:
            raise ValueError(f"Invalid timing_platelet_fall: {timing_platelet_fall}")
        
        if nadir_platelet_count not in self.nadir_points:
            raise ValueError(f"Invalid nadir_platelet_count: {nadir_platelet_count}")
        
        if thrombosis not in self.thrombosis_points:
            raise ValueError(f"Invalid thrombosis: {thrombosis}")
        
        if skin_necrosis not in self.skin_necrosis_points:
            raise ValueError(f"Invalid skin_necrosis: {skin_necrosis}")
        
        if acute_systemic_reaction not in self.systemic_reaction_points:
            raise ValueError(f"Invalid acute_systemic_reaction: {acute_systemic_reaction}")
        
        if bleeding not in self.bleeding_points:
            raise ValueError(f"Invalid bleeding: {bleeding}")
        
        if other_causes_thrombocytopenia not in self.other_causes_points:
            raise ValueError(f"Invalid other_causes_thrombocytopenia: {other_causes_thrombocytopenia}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated HEP score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 2:
            return {
                "stage": "Low Probability",
                "description": "Score <2",
                "interpretation": "Low probability of HIT. The HEP score has 100% sensitivity at "
                                "cutoff of 2, effectively ruling out HIT in low-risk patients. "
                                "Consider alternative causes of thrombocytopenia."
            }
        elif score < 5:
            return {
                "stage": "Intermediate Probability",
                "description": "Score 2-4",
                "interpretation": "Intermediate probability of HIT. Further testing recommended "
                                "including HIT antibody testing. Continue clinical monitoring."
            }
        else:
            return {
                "stage": "High Probability",
                "description": "Score ≥5",
                "interpretation": "High probability of HIT. At cutoff of 5, the HEP score has "
                                "86% sensitivity and 88% specificity. Consider immediate cessation "
                                "of heparin and initiation of alternative anticoagulation while "
                                "awaiting confirmatory testing."
            }


def calculate_hep_hit(magnitude_fall: str, timing_platelet_fall: str,
                      nadir_platelet_count: str, thrombosis: str,
                      skin_necrosis: str, acute_systemic_reaction: str,
                      bleeding: str, other_causes_thrombocytopenia: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HepHitCalculator()
    return calculator.calculate(magnitude_fall, timing_platelet_fall,
                              nadir_platelet_count, thrombosis,
                              skin_necrosis, acute_systemic_reaction,
                              bleeding, other_causes_thrombocytopenia)