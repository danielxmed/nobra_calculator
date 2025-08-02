"""
Rome IV Diagnostic Criteria for Proctalgia Fugax Calculator

Applies the official Rome IV diagnostic criteria for proctalgia fugax, a functional 
anorectal pain disorder. Proctalgia fugax is characterized by sudden, severe, episodic 
rectal pain unrelated to defecation, lasting seconds to 30 minutes, with complete 
pain-free intervals between episodes.

References:
1. Lacy BE, Mearin F, Chang L, Chey WD, Lembo AJ, Simren M, Spiller R. Bowel Disorders. 
   Gastroenterology. 2016 May;150(6):1393-1407.e5. doi: 10.1053/j.gastro.2016.02.031.
2. Rome Foundation. Rome IV Diagnostic Criteria for Functional Gastrointestinal Disorders. 
   4th ed. Raleigh, NC: Rome Foundation; 2016.
3. Bharucha AE, Wald A, Enck P, Rao S. Functional anorectal disorders. Gastroenterology. 
   2006 Apr;130(5):1510-8. doi: 10.1053/j.gastro.2005.11.064.
"""

from typing import Dict, Any


class RomeIvProctalgieFugaxCalculator:
    """Calculator for Rome IV Diagnostic Criteria for Proctalgia Fugax"""
    
    def __init__(self):
        # All criteria must be met for positive diagnosis
        self.REQUIRED_CRITERIA_COUNT = 8
    
    def calculate(self, recurrent_rectal_pain_unrelated_defecation: str, 
                 episode_duration_seconds_to_30_minutes: str,
                 no_anorectal_pain_between_episodes: str,
                 exclusion_inflammatory_causes: str,
                 exclusion_structural_anorectal_lesions: str,
                 exclusion_prostatitis: str,
                 exclusion_coccygodynia: str,
                 exclusion_pelvic_floor_alterations: str) -> Dict[str, Any]:
        """
        Applies Rome IV diagnostic criteria for proctalgia fugax
        
        Args:
            recurrent_rectal_pain_unrelated_defecation (str): Recurrent episodes of pain 
                localized to the rectum and unrelated to defecation ("yes"/"no")
            episode_duration_seconds_to_30_minutes (str): Episodes lasting from seconds 
                to minutes, with maximum duration of 30 minutes ("yes"/"no")
            no_anorectal_pain_between_episodes (str): No anorectal pain between episodes ("yes"/"no")
            exclusion_inflammatory_causes (str): Exclusion of inflammatory bowel disease ("yes"/"no")
            exclusion_structural_anorectal_lesions (str): Exclusion of structural anorectal 
                lesions (abscess, fissure, thrombosed hemorrhoids) ("yes"/"no")
            exclusion_prostatitis (str): Exclusion of prostatitis ("yes"/"no")
            exclusion_coccygodynia (str): Exclusion of coccygodynia ("yes"/"no")
            exclusion_pelvic_floor_alterations (str): Exclusion of major structural 
                alterations of the pelvic floor ("yes"/"no")
            
        Returns:
            Dict with Rome IV proctalgia fugax diagnostic assessment
        """
        
        # Validate inputs
        self._validate_inputs(recurrent_rectal_pain_unrelated_defecation, 
                             episode_duration_seconds_to_30_minutes,
                             no_anorectal_pain_between_episodes,
                             exclusion_inflammatory_causes,
                             exclusion_structural_anorectal_lesions,
                             exclusion_prostatitis,
                             exclusion_coccygodynia,
                             exclusion_pelvic_floor_alterations)
        
        # Count criteria met
        criteria_met = self._count_criteria_met(recurrent_rectal_pain_unrelated_defecation,
                                               episode_duration_seconds_to_30_minutes,
                                               no_anorectal_pain_between_episodes,
                                               exclusion_inflammatory_causes,
                                               exclusion_structural_anorectal_lesions,
                                               exclusion_prostatitis,
                                               exclusion_coccygodynia,
                                               exclusion_pelvic_floor_alterations)
        
        # Determine diagnosis
        diagnosis_met = criteria_met == self.REQUIRED_CRITERIA_COUNT
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_met, criteria_met)
        
        return {
            "result": "Criteria Met" if diagnosis_met else "Criteria Not Met",
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, recurrent_rectal_pain_unrelated_defecation: str, 
                        episode_duration_seconds_to_30_minutes: str,
                        no_anorectal_pain_between_episodes: str,
                        exclusion_inflammatory_causes: str,
                        exclusion_structural_anorectal_lesions: str,
                        exclusion_prostatitis: str,
                        exclusion_coccygodynia: str,
                        exclusion_pelvic_floor_alterations: str):
        """Validates input parameters"""
        
        # List of all parameters with their names for validation
        parameters = [
            (recurrent_rectal_pain_unrelated_defecation, "recurrent_rectal_pain_unrelated_defecation"),
            (episode_duration_seconds_to_30_minutes, "episode_duration_seconds_to_30_minutes"),
            (no_anorectal_pain_between_episodes, "no_anorectal_pain_between_episodes"),
            (exclusion_inflammatory_causes, "exclusion_inflammatory_causes"),
            (exclusion_structural_anorectal_lesions, "exclusion_structural_anorectal_lesions"),
            (exclusion_prostatitis, "exclusion_prostatitis"),
            (exclusion_coccygodynia, "exclusion_coccygodynia"),
            (exclusion_pelvic_floor_alterations, "exclusion_pelvic_floor_alterations")
        ]
        
        for param, name in parameters:
            if not isinstance(param, str) or param.lower() not in ["yes", "no"]:
                raise ValueError(f"{name} must be either 'yes' or 'no'")
    
    def _count_criteria_met(self, recurrent_rectal_pain_unrelated_defecation: str,
                           episode_duration_seconds_to_30_minutes: str,
                           no_anorectal_pain_between_episodes: str,
                           exclusion_inflammatory_causes: str,
                           exclusion_structural_anorectal_lesions: str,
                           exclusion_prostatitis: str,
                           exclusion_coccygodynia: str,
                           exclusion_pelvic_floor_alterations: str) -> int:
        """Counts how many Rome IV criteria are met"""
        
        criteria_met = 0
        
        # Criterion 1: Recurrent episodes of pain localized to the rectum and unrelated to defecation
        if recurrent_rectal_pain_unrelated_defecation.lower() == "yes":
            criteria_met += 1
        
        # Criterion 2: Episodes lasting from seconds to minutes, with maximum duration of 30 minutes
        if episode_duration_seconds_to_30_minutes.lower() == "yes":
            criteria_met += 1
        
        # Criterion 3: No anorectal pain between episodes
        if no_anorectal_pain_between_episodes.lower() == "yes":
            criteria_met += 1
        
        # Criterion 4: Exclusion of inflammatory bowel disease
        if exclusion_inflammatory_causes.lower() == "yes":
            criteria_met += 1
        
        # Criterion 5: Exclusion of structural anorectal lesions
        if exclusion_structural_anorectal_lesions.lower() == "yes":
            criteria_met += 1
        
        # Criterion 6: Exclusion of prostatitis
        if exclusion_prostatitis.lower() == "yes":
            criteria_met += 1
        
        # Criterion 7: Exclusion of coccygodynia
        if exclusion_coccygodynia.lower() == "yes":
            criteria_met += 1
        
        # Criterion 8: Exclusion of major structural alterations of the pelvic floor
        if exclusion_pelvic_floor_alterations.lower() == "yes":
            criteria_met += 1
        
        return criteria_met
    
    def _get_interpretation(self, diagnosis_met: bool, criteria_met: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on Rome IV criteria fulfillment
        
        Args:
            diagnosis_met (bool): Whether all criteria are met
            criteria_met (int): Number of criteria fulfilled
            
        Returns:
            Dict with clinical interpretation
        """
        
        if diagnosis_met:
            return {
                "stage": "Criteria Met",
                "description": "Meets Rome IV criteria",
                "interpretation": "Patient fulfills Rome IV diagnostic criteria for proctalgia fugax. Diagnosis is established when all essential criteria are met, including recurrent episodes of rectal pain lasting seconds to 30 minutes, pain-free intervals between episodes, and exclusion of organic causes. Treatment focuses on reassurance, patient education about the benign nature of the condition, stress management techniques, and symptomatic relief during acute episodes. Consider triggers such as stress, anxiety, or sexual activity. Prognosis is generally excellent with episodes typically occurring less than 5 times per year."
            }
        else:
            return {
                "stage": "Criteria Not Met",
                "description": "Does not meet Rome IV criteria",
                "interpretation": f"Patient does not fulfill Rome IV diagnostic criteria for proctalgia fugax ({criteria_met}/{self.REQUIRED_CRITERIA_COUNT} criteria met). One or more essential criteria are not satisfied. Consider alternative diagnoses including levator ani syndrome (chronic pain with puborectalis muscle tenderness on digital rectal examination), unspecified functional anorectal pain (episodes lasting longer than 30 minutes), or organic causes of anorectal pain. Further evaluation may be needed to identify underlying structural pathology, inflammatory conditions, or alternative functional disorders. Complete history, physical examination, and appropriate diagnostic studies should be performed to exclude organic causes."
            }


def calculate_rome_iv_proctalgia_fugax(recurrent_rectal_pain_unrelated_defecation: str,
                                      episode_duration_seconds_to_30_minutes: str,
                                      no_anorectal_pain_between_episodes: str,
                                      exclusion_inflammatory_causes: str,
                                      exclusion_structural_anorectal_lesions: str,
                                      exclusion_prostatitis: str,
                                      exclusion_coccygodynia: str,
                                      exclusion_pelvic_floor_alterations: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = RomeIvProctalgieFugaxCalculator()
    return calculator.calculate(recurrent_rectal_pain_unrelated_defecation,
                               episode_duration_seconds_to_30_minutes,
                               no_anorectal_pain_between_episodes,
                               exclusion_inflammatory_causes,
                               exclusion_structural_anorectal_lesions,
                               exclusion_prostatitis,
                               exclusion_coccygodynia,
                               exclusion_pelvic_floor_alterations)