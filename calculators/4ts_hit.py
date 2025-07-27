"""
4Ts Score for Heparin-Induced Thrombocytopenia Calculator

Differentiates patients with HIT from those with other causes of thrombocytopenia.
Reference: Lo GK et al., J Thromb Haemost 2006;4(4):759-65
"""

from typing import Dict, Any


class FourTsHitCalculator:
    """Calculator for the 4Ts Score for HIT"""
    
    def calculate(self, thrombocytopenia_severity: str, timing_onset: str,
                 thrombosis_sequelae: str, other_causes: str) -> Dict[str, Any]:
        """
        Calculates the 4Ts Score for HIT
        
        Args:
            thrombocytopenia_severity: Descriptive options for the magnitude of thrombocytopenia
            timing_onset: Descriptive options for the timing of platelet fall  
            thrombosis_sequelae: Descriptive options for the presence of thrombosis/sequelae
            other_causes: Descriptive options for other causes of thrombocytopenia
                
        Returns:
            Dict with result, interpretation, and risk classification
        """
        
        # Validations
        self._validate_inputs(thrombocytopenia_severity, timing_onset,
                            thrombosis_sequelae, other_causes)
        
        # Calculate score
        score = 0
        
        # Thrombocytopenia (0-2 points)
        score += self._score_thrombocytopenia(thrombocytopenia_severity)
        
        # Timing of onset (0-2 points)
        score += self._score_timing(timing_onset)
        
        # Thrombosis/sequelae (0-2 points)
        score += self._score_thrombosis(thrombosis_sequelae)
        
        # Other causes (0-2 points) - note: inverse scoring
        score += self._score_other_causes(other_causes)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "hit_probability": interpretation["hit_probability"]
        }
    
    def _validate_inputs(self, thrombocytopenia_severity: str, timing_onset: str,
                        thrombosis_sequelae: str, other_causes: str):
        """Validates input parameters"""
        
        valid_severity = [
            "fall_greater_50_nadir_greater_20",
            "fall_30_50_or_nadir_10_19", 
            "fall_less_30_or_nadir_less_10"
        ]
        if thrombocytopenia_severity not in valid_severity:
            raise ValueError(f"Thrombocytopenia severity must be one of the valid options")
        
        valid_timing = [
            "onset_5_10_days_or_fall_1_day_heparin_30_days",
            "possible_5_10_days_or_onset_after_10_days_or_heparin_30_100_days",
            "fall_less_4_days_no_recent_exposure"
        ]
        if timing_onset not in valid_timing:
            raise ValueError(f"Timing of onset must be one of the valid options")
        
        valid_thrombosis = [
            "new_thrombosis_or_skin_necrosis_or_systemic_reaction",
            "progressive_thrombosis_or_skin_lesions_or_suspected_thrombosis",
            "no_thrombosis_or_sequelae"
        ]
        if thrombosis_sequelae not in valid_thrombosis:
            raise ValueError(f"Thrombosis/sequelae must be one of the valid options")
        
        valid_other = [
            "no_other_apparent_cause",
            "other_possible_causes", 
            "other_definitive_causes"
        ]
        if other_causes not in valid_other:
            raise ValueError(f"Other causes must be one of the valid options")
    
    def _score_thrombocytopenia(self, severity: str) -> int:
        """Calculates points for thrombocytopenia"""
        mapping = {
            "fall_greater_50_nadir_greater_20": 2,
            "fall_30_50_or_nadir_10_19": 1,
            "fall_less_30_or_nadir_less_10": 0
        }
        return mapping[severity]
    
    def _score_timing(self, timing: str) -> int:
        """Calculates points for timing of onset"""
        mapping = {
            "onset_5_10_days_or_fall_1_day_heparin_30_days": 2,
            "possible_5_10_days_or_onset_after_10_days_or_heparin_30_100_days": 1,
            "fall_less_4_days_no_recent_exposure": 0
        }
        return mapping[timing]
    
    def _score_thrombosis(self, thrombosis: str) -> int:
        """Calculates points for thrombosis/sequelae"""
        mapping = {
            "new_thrombosis_or_skin_necrosis_or_systemic_reaction": 2,
            "progressive_thrombosis_or_skin_lesions_or_suspected_thrombosis": 1,
            "no_thrombosis_or_sequelae": 0
        }
        return mapping[thrombosis]
    
    def _score_other_causes(self, other_causes: str) -> int:
        """Calculates points for other causes (inverse scoring)"""
        mapping = {
            "no_other_apparent_cause": 2,
            "other_possible_causes": 1,
            "other_definitive_causes": 0
        }
        return mapping[other_causes]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score: Calculated score (0-8)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low Probability",
                "description": "Low probability of HIT",
                "interpretation": f"Score of {score} points indicates low probability of HIT (<5%). Negative predictive value of 99.8%. HIT unlikely - consider other causes of thrombocytopenia. May forgo additional HIT testing.",
                "hit_probability": "<5%"
            }
        elif score <= 5:
            return {
                "stage": "Intermediate Probability",
                "description": "Intermediate probability of HIT",
                "interpretation": f"Score of {score} points indicates intermediate probability of HIT (~14%). Further investigation with laboratory tests for HIT (functional or immunoassay) is necessary. Consider discontinuing heparin until results.",
                "hit_probability": "~14%"
            }
        else:  # score >= 6
            return {
                "stage": "High Probability",
                "description": "High probability of HIT",
                "interpretation": f"Score of {score} points indicates high probability of HIT (~64%). Immediately discontinue all heparin. Start non-heparin anticoagulant (argatroban, bivalirudin). Perform confirmatory tests for HIT.",
                "hit_probability": "~64%"
            }


def calculate_4ts_hit(thrombocytopenia_severity: str, timing_onset: str,
                     thrombosis_sequelae: str, other_causes: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FourTsHitCalculator()
    return calculator.calculate(thrombocytopenia_severity, timing_onset,
                              thrombosis_sequelae, other_causes)
