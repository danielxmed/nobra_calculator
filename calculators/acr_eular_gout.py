"""
ACR/EULAR Gout Classification Criteria Calculator

Implements the 2015 ACR/EULAR classification criteria for gout using a 3-step approach:
1. Entry criterion: ≥1 episode of swelling, pain, or tenderness in peripheral joint/bursa
2. Sufficient criterion: Presence of MSU crystals = definite gout
3. Classification criteria: Scoring system requiring ≥7 points for gout classification

References:
- Neogi T, et al. 2015 Gout classification criteria: an American College of Rheumatology/European League Against Rheumatism collaborative initiative. Ann Rheum Dis. 2015;74(10):1789-98.
- Taylor WJ, et al. Study for Updated Gout Classification Criteria: identification of features to classify gout. Arthritis Care Res (Hoboken). 2015;67(9):1304-15.
"""

from typing import Dict, Any


class AcrEularGoutCalculator:
    """Calculator for ACR/EULAR Gout Classification Criteria"""
    
    def __init__(self):
        # Scoring weights for classification criteria
        self.JOINT_PATTERN_SCORES = {
            "other_joint": 0,     # Joint/bursa other than ankle, midfoot or 1st MTP
            "ankle_midfoot": 1,   # Ankle OR midfoot (as part of mono/oligoarticular episode without 1st MTP)
            "first_mtp": 2        # 1st MTP (as part of mono/oligoarticular episode)
        }
        
        self.EPISODE_CHARACTERISTICS_SCORES = {
            "none": 0,
            "one": 1,
            "two": 2,
            "three": 3
        }
        
        self.TYPICAL_EPISODES_SCORES = {
            "none": 0,
            "one": 1,
            "recurrent": 2
        }
        
        self.TOPHUS_SCORES = {
            "absent": 0,
            "present": 4
        }
        
        self.SERUM_URATE_SCORES = {
            "under_4": -4,      # < 4mg/dL [< 0.24mM]
            "4_to_6": 0,        # ≥ 4 or < 6mg/dL [≥ 0.24 or < 0.36mM]
            "6_to_8": 2,        # ≥ 6 or < 8mg/dL [≥ 0.36 or < 0.48mM]
            "8_to_10": 3,       # ≥ 8 or < 10mg/dL [≥ 0.48 or < 0.60mM]
            "over_10": 4        # ≥ 10mg/dL [≥ 0.60mM]
        }
        
        self.SYNOVIAL_FLUID_SCORES = {
            "negative_msu": -2,
            "not_done": 0
        }
        
        self.IMAGING_URATE_SCORES = {
            "absent": 0,
            "present": 4
        }
        
        self.IMAGING_DAMAGE_SCORES = {
            "absent": 0,
            "present": 4
        }
    
    def calculate(self, entry_criterion: str, msu_crystals_present: str, joint_pattern: str,
                 episode_characteristics: str, typical_episodes: str, tophus_evidence: str,
                 serum_urate: str, synovial_fluid_analysis: str, imaging_urate_deposition: str,
                 imaging_joint_damage: str) -> Dict[str, Any]:
        """
        Calculates ACR/EULAR Gout Classification Criteria result
        
        Args:
            entry_criterion (str): ≥1 episode of swelling, pain, or tenderness in peripheral joint/bursa
            msu_crystals_present (str): Presence of MSU crystals in symptomatic joint/bursa/tophus
            joint_pattern (str): Pattern of joint/bursa involvement during episodes
            episode_characteristics (str): Number of characteristics during episodes
            typical_episodes (str): Number of episodes with typical time-course
            tophus_evidence (str): Evidence of tophus
            serum_urate (str): Serum urate level category
            synovial_fluid_analysis (str): Synovial fluid analysis result
            imaging_urate_deposition (str): Imaging evidence of urate deposition
            imaging_joint_damage (str): Imaging evidence of gout-related joint damage
            
        Returns:
            Dict with classification result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(entry_criterion, msu_crystals_present, joint_pattern,
                            episode_characteristics, typical_episodes, tophus_evidence,
                            serum_urate, synovial_fluid_analysis, imaging_urate_deposition,
                            imaging_joint_damage)
        
        # Step 1: Check entry criterion
        if entry_criterion != "yes":
            return {
                "result": "Entry criterion not met",
                "unit": "classification",
                "interpretation": "Entry criterion not met. Patient must have ≥1 episode of swelling, pain, or tenderness in a peripheral joint or bursa to proceed with gout classification.",
                "stage": "Entry criterion not met",
                "stage_description": "Prerequisites not satisfied"
            }
        
        # Step 2: Check sufficient criterion (MSU crystals)
        if msu_crystals_present == "yes":
            return {
                "result": "Definite gout (MSU crystals present)",
                "unit": "classification",
                "interpretation": "Definite gout. Presence of monosodium urate (MSU) crystals in symptomatic joint, bursa, or tophus is sufficient for gout diagnosis according to ACR/EULAR 2015 criteria.",
                "stage": "Definite gout",
                "stage_description": "MSU crystals present"
            }
        
        # Step 3: Classification criteria scoring
        score = self._calculate_classification_score(joint_pattern, episode_characteristics,
                                                   typical_episodes, tophus_evidence,
                                                   serum_urate, synovial_fluid_analysis,
                                                   imaging_urate_deposition, imaging_joint_damage)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": f"Score {score}/23 points",
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, entry_criterion, msu_crystals_present, joint_pattern,
                        episode_characteristics, typical_episodes, tophus_evidence,
                        serum_urate, synovial_fluid_analysis, imaging_urate_deposition,
                        imaging_joint_damage):
        """Validates input parameters"""
        
        valid_entry = ["yes", "no"]
        valid_msu = ["yes", "no", "not_tested"]
        valid_joint_pattern = ["other_joint", "ankle_midfoot", "first_mtp"]
        valid_characteristics = ["none", "one", "two", "three"]
        valid_episodes = ["none", "one", "recurrent"]
        valid_tophus = ["absent", "present"]
        valid_urate = ["under_4", "4_to_6", "6_to_8", "8_to_10", "over_10"]
        valid_synovial = ["negative_msu", "not_done"]
        valid_imaging = ["absent", "present"]
        
        if entry_criterion not in valid_entry:
            raise ValueError(f"Entry criterion must be one of: {valid_entry}")
        
        if msu_crystals_present not in valid_msu:
            raise ValueError(f"MSU crystals status must be one of: {valid_msu}")
        
        if joint_pattern not in valid_joint_pattern:
            raise ValueError(f"Joint pattern must be one of: {valid_joint_pattern}")
        
        if episode_characteristics not in valid_characteristics:
            raise ValueError(f"Episode characteristics must be one of: {valid_characteristics}")
        
        if typical_episodes not in valid_episodes:
            raise ValueError(f"Typical episodes must be one of: {valid_episodes}")
        
        if tophus_evidence not in valid_tophus:
            raise ValueError(f"Tophus evidence must be one of: {valid_tophus}")
        
        if serum_urate not in valid_urate:
            raise ValueError(f"Serum urate must be one of: {valid_urate}")
        
        if synovial_fluid_analysis not in valid_synovial:
            raise ValueError(f"Synovial fluid analysis must be one of: {valid_synovial}")
        
        if imaging_urate_deposition not in valid_imaging:
            raise ValueError(f"Imaging urate deposition must be one of: {valid_imaging}")
        
        if imaging_joint_damage not in valid_imaging:
            raise ValueError(f"Imaging joint damage must be one of: {valid_imaging}")
    
    def _calculate_classification_score(self, joint_pattern, episode_characteristics,
                                      typical_episodes, tophus_evidence, serum_urate,
                                      synovial_fluid_analysis, imaging_urate_deposition,
                                      imaging_joint_damage):
        """Calculates the classification criteria score"""
        
        score = 0
        
        # Joint pattern (0-2 points)
        score += self.JOINT_PATTERN_SCORES[joint_pattern]
        
        # Episode characteristics (0-3 points)
        score += self.EPISODE_CHARACTERISTICS_SCORES[episode_characteristics]
        
        # Typical episodes (0-2 points)
        score += self.TYPICAL_EPISODES_SCORES[typical_episodes]
        
        # Tophus evidence (0 or 4 points)
        score += self.TOPHUS_SCORES[tophus_evidence]
        
        # Serum urate (-4 to +4 points)
        score += self.SERUM_URATE_SCORES[serum_urate]
        
        # Synovial fluid analysis (-2 or 0 points)
        score += self.SYNOVIAL_FLUID_SCORES[synovial_fluid_analysis]
        
        # Imaging urate deposition (0 or 4 points)
        score += self.IMAGING_URATE_SCORES[imaging_urate_deposition]
        
        # Imaging joint damage (0 or 4 points)
        score += self.IMAGING_DAMAGE_SCORES[imaging_joint_damage]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Classification criteria score
            
        Returns:
            Dict with interpretation
        """
        
        if score >= 7:
            return {
                "stage": "Meets criteria for gout",
                "description": "Meets gout classification criteria",
                "interpretation": f"Score {score}/23 points. Meets ACR/EULAR 2015 classification criteria for gout. Diagnosis consistent with gout. Consider appropriate urate-lowering therapy and management of acute attacks."
            }
        else:
            return {
                "stage": "Does not meet criteria",
                "description": "Does not meet gout classification criteria",
                "interpretation": f"Score {score}/23 points. Does not meet ACR/EULAR 2015 classification criteria for gout (requires ≥7 points). Consider alternative diagnoses such as pseudogout (CPPD crystal arthropathy), septic arthritis, rheumatoid arthritis, or other inflammatory arthropathies."
            }


def calculate_acr_eular_gout(entry_criterion, msu_crystals_present, joint_pattern,
                           episode_characteristics, typical_episodes, tophus_evidence,
                           serum_urate, synovial_fluid_analysis, imaging_urate_deposition,
                           imaging_joint_damage) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_acr_eular_gout pattern
    """
    calculator = AcrEularGoutCalculator()
    return calculator.calculate(entry_criterion, msu_crystals_present, joint_pattern,
                              episode_characteristics, typical_episodes, tophus_evidence,
                              serum_urate, synovial_fluid_analysis, imaging_urate_deposition,
                              imaging_joint_damage)