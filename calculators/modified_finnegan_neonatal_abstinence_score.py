"""
Modified Finnegan Neonatal Abstinence Score (NAS) Calculator

Stratifies severity of opioid withdrawal in neonates and guides pharmacologic 
treatment decisions. The modified version is the most widely used tool for 
neonatal abstinence syndrome assessment.

References:
1. Finnegan LP, et al. Addict Dis. 1975;2(1-2):141-58.
2. Jansson LM, et al. J Opioid Manag. 2009;5(1):47-55.
3. Hudak ML, et al. Pediatrics. 2012;129(2):e540-60.
"""

from typing import Dict, Any


class ModifiedFinneganNeonatalAbstinenceScoreCalculator:
    """Calculator for Modified Finnegan Neonatal Abstinence Score (NAS)"""
    
    def __init__(self):
        # Scoring for each parameter
        self.CRY_SCORES = {
            "normal": 0,
            "excessive_high_pitched_under_5min": 2,
            "continuous_high_pitched_over_5min": 3
        }
        
        self.SLEEP_SCORES = {
            "normal": 0,
            "sleeps_under_3hrs": 1,
            "sleeps_under_2hrs": 2,
            "sleeps_under_1hr": 3
        }
        
        self.MORO_REFLEX_SCORES = {
            "normal": 0,
            "hyperactive": 2,
            "markedly_hyperactive": 3
        }
        
        self.TREMOR_SCORES = {
            "none": 0,
            "mild_when_disturbed": 1,
            "moderate_severe_when_disturbed": 2,
            "mild_when_undisturbed": 3,
            "moderate_severe_when_undisturbed": 4
        }
        
        self.HYPERTHERMIA_SCORES = {
            "normal": 0,
            "mild_99_to_100_9F": 1,
            "severe_over_100_9F": 2
        }
        
        self.RESPIRATORY_RATE_SCORES = {
            "normal": 0,
            "over_60_no_retractions": 1,
            "over_60_with_retractions": 2
        }
        
        # Binary parameters (yes/no) with their point values
        self.BINARY_SCORES = {
            "increased_muscle_tone": 1,
            "excoriation": 1,
            "myoclonic_jerks": 3,
            "generalized_convulsions": 5,
            "sweating": 1,
            "frequent_yawning": 1,
            "mottling": 1,
            "nasal_flaring": 2,
            "sneezing": 1,
            "nasal_stuffiness": 1,
            "excessive_sucking": 1,
            "poor_feeding": 2,
            "regurgitation": 2,
            "projectile_vomiting": 3,
            "loose_stools": 2,
            "watery_stools": 3
        }
    
    def calculate(self, cry: str, sleep: str, moro_reflex: str, tremors: str,
                  increased_muscle_tone: str, excoriation: str, myoclonic_jerks: str,
                  generalized_convulsions: str, sweating: str, hyperthermia: str,
                  frequent_yawning: str, mottling: str, nasal_flaring: str,
                  respiratory_rate: str, sneezing: str, nasal_stuffiness: str,
                  excessive_sucking: str, poor_feeding: str, regurgitation: str,
                  projectile_vomiting: str, loose_stools: str, watery_stools: str) -> Dict[str, Any]:
        """
        Calculates the Modified Finnegan Neonatal Abstinence Score (NAS)
        
        Args:
            All NAS assessment parameters covering CNS, metabolic, respiratory, and GI domains
            
        Returns:
            Dict with NAS score and treatment recommendations
        """
        
        # Validate inputs
        self._validate_inputs(cry, sleep, moro_reflex, tremors, increased_muscle_tone,
                            excoriation, myoclonic_jerks, generalized_convulsions,
                            sweating, hyperthermia, frequent_yawning, mottling,
                            nasal_flaring, respiratory_rate, sneezing, nasal_stuffiness,
                            excessive_sucking, poor_feeding, regurgitation,
                            projectile_vomiting, loose_stools, watery_stools)
        
        # Calculate component scores
        total_score = 0
        
        # Multi-level scoring parameters
        total_score += self.CRY_SCORES[cry]
        total_score += self.SLEEP_SCORES[sleep]
        total_score += self.MORO_REFLEX_SCORES[moro_reflex]
        total_score += self.TREMOR_SCORES[tremors]
        total_score += self.HYPERTHERMIA_SCORES[hyperthermia]
        total_score += self.RESPIRATORY_RATE_SCORES[respiratory_rate]
        
        # Binary scoring parameters
        binary_params = {
            "increased_muscle_tone": increased_muscle_tone,
            "excoriation": excoriation,
            "myoclonic_jerks": myoclonic_jerks,
            "generalized_convulsions": generalized_convulsions,
            "sweating": sweating,
            "frequent_yawning": frequent_yawning,
            "mottling": mottling,
            "nasal_flaring": nasal_flaring,
            "sneezing": sneezing,
            "nasal_stuffiness": nasal_stuffiness,
            "excessive_sucking": excessive_sucking,
            "poor_feeding": poor_feeding,
            "regurgitation": regurgitation,
            "projectile_vomiting": projectile_vomiting,
            "loose_stools": loose_stools,
            "watery_stools": watery_stools
        }
        
        for param_name, param_value in binary_params.items():
            if param_value == "yes":
                total_score += self.BINARY_SCORES[param_name]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, cry: str, sleep: str, moro_reflex: str, tremors: str,
                        increased_muscle_tone: str, excoriation: str, myoclonic_jerks: str,
                        generalized_convulsions: str, sweating: str, hyperthermia: str,
                        frequent_yawning: str, mottling: str, nasal_flaring: str,
                        respiratory_rate: str, sneezing: str, nasal_stuffiness: str,
                        excessive_sucking: str, poor_feeding: str, regurgitation: str,
                        projectile_vomiting: str, loose_stools: str, watery_stools: str):
        """Validates input parameters"""
        
        # Validate multi-level parameters
        if cry not in self.CRY_SCORES:
            raise ValueError(f"cry must be one of: {', '.join(self.CRY_SCORES.keys())}")
        if sleep not in self.SLEEP_SCORES:
            raise ValueError(f"sleep must be one of: {', '.join(self.SLEEP_SCORES.keys())}")
        if moro_reflex not in self.MORO_REFLEX_SCORES:
            raise ValueError(f"moro_reflex must be one of: {', '.join(self.MORO_REFLEX_SCORES.keys())}")
        if tremors not in self.TREMOR_SCORES:
            raise ValueError(f"tremors must be one of: {', '.join(self.TREMOR_SCORES.keys())}")
        if hyperthermia not in self.HYPERTHERMIA_SCORES:
            raise ValueError(f"hyperthermia must be one of: {', '.join(self.HYPERTHERMIA_SCORES.keys())}")
        if respiratory_rate not in self.RESPIRATORY_RATE_SCORES:
            raise ValueError(f"respiratory_rate must be one of: {', '.join(self.RESPIRATORY_RATE_SCORES.keys())}")
        
        # Validate binary parameters
        binary_params = [
            increased_muscle_tone, excoriation, myoclonic_jerks, generalized_convulsions,
            sweating, frequent_yawning, mottling, nasal_flaring, sneezing, nasal_stuffiness,
            excessive_sucking, poor_feeding, regurgitation, projectile_vomiting,
            loose_stools, watery_stools
        ]
        
        binary_param_names = [
            "increased_muscle_tone", "excoriation", "myoclonic_jerks", "generalized_convulsions",
            "sweating", "frequent_yawning", "mottling", "nasal_flaring", "sneezing", "nasal_stuffiness",
            "excessive_sucking", "poor_feeding", "regurgitation", "projectile_vomiting",
            "loose_stools", "watery_stools"
        ]
        
        for i, param in enumerate(binary_params):
            if param not in ["yes", "no"]:
                raise ValueError(f"{binary_param_names[i]} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on NAS score
        
        Args:
            score: Total NAS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 7:
            return {
                "stage": "No Treatment",
                "description": "Mild or no withdrawal symptoms",
                "interpretation": (f"NAS score of {score} indicates mild or no withdrawal symptoms. "
                                "Continue supportive care including swaddling, minimal stimulation, "
                                "frequent small feeds, and quiet environment. Monitor every 3-4 hours. "
                                "No pharmacologic treatment indicated at this time.")
            }
        elif score <= 11:
            return {
                "stage": "Monitor Closely",
                "description": "Moderate withdrawal symptoms",
                "interpretation": (f"NAS score of {score} indicates moderate withdrawal symptoms. "
                                "Increase monitoring frequency and optimize non-pharmacologic interventions. "
                                "Consider pharmacologic treatment if three consecutive scores ≥8. "
                                "Continue supportive care and reassess frequently.")
            }
        else:  # score >= 12
            return {
                "stage": "Treat",
                "description": "Severe withdrawal symptoms",
                "interpretation": (f"NAS score of {score} indicates severe withdrawal symptoms requiring "
                                "immediate pharmacologic treatment. Two consecutive scores ≥12 indicate "
                                "need for medication (typically morphine or methadone). Continue supportive "
                                "care and monitor response to treatment. Goal is to stabilize infant to "
                                "allow feeding, sleeping, and appropriate weight gain.")
            }


def calculate_modified_finnegan_neonatal_abstinence_score(
    cry: str, sleep: str, moro_reflex: str, tremors: str,
    increased_muscle_tone: str, excoriation: str, myoclonic_jerks: str,
    generalized_convulsions: str, sweating: str, hyperthermia: str,
    frequent_yawning: str, mottling: str, nasal_flaring: str,
    respiratory_rate: str, sneezing: str, nasal_stuffiness: str,
    excessive_sucking: str, poor_feeding: str, regurgitation: str,
    projectile_vomiting: str, loose_stools: str, watery_stools: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedFinneganNeonatalAbstinenceScoreCalculator()
    return calculator.calculate(cry, sleep, moro_reflex, tremors,
                              increased_muscle_tone, excoriation, myoclonic_jerks,
                              generalized_convulsions, sweating, hyperthermia,
                              frequent_yawning, mottling, nasal_flaring,
                              respiratory_rate, sneezing, nasal_stuffiness,
                              excessive_sucking, poor_feeding, regurgitation,
                              projectile_vomiting, loose_stools, watery_stools)