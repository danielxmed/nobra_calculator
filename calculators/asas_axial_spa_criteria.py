"""
ASAS Criteria for Axial Spondyloarthritis (SpA) Calculator

Classifies axial spondyloarthritis according to Assessment of Spondyloarthritis 
International Society (ASAS) criteria. This classification system allows for early 
diagnosis of axial SpA by incorporating both clinical and imaging features.

References (Vancouver style):
1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
   The development of Assessment of SpondyloArthritis international Society 
   classification criteria for axial spondyloarthritis (part II): validation and 
   final selection. Ann Rheum Dis. 2009;68(6):777-83.
2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
   The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
   a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44.
"""

from typing import Dict, Any


class AsasAxialSpaCriteriaCalculator:
    """Calculator for ASAS Criteria for Axial Spondyloarthritis"""
    
    def __init__(self):
        self.spa_features = [
            'inflammatory_back_pain',
            'arthritis',
            'enthesitis',
            'uveitis',
            'dactylitis',
            'psoriasis',
            'crohns_colitis',
            'good_response_nsaids',
            'family_history',
            'elevated_crp'
        ]
    
    def calculate(self,
                 back_pain_duration_months: int,
                 age_at_onset: int,
                 sacroiliitis_imaging: str,
                 hla_b27_positive: str,
                 inflammatory_back_pain: str,
                 arthritis: str,
                 enthesitis: str,
                 uveitis: str,
                 dactylitis: str,
                 psoriasis: str,
                 crohns_colitis: str,
                 good_response_nsaids: str,
                 family_history: str,
                 elevated_crp: str) -> Dict[str, Any]:
        """
        Calculates ASAS classification for axial spondyloarthritis
        
        Args:
            back_pain_duration_months (int): Duration of back pain in months
            age_at_onset (int): Age at onset of back pain
            sacroiliitis_imaging (str): Sacroiliitis on imaging (present/absent)
            hla_b27_positive (str): HLA-B27 positive (yes/no)
            inflammatory_back_pain (str): Inflammatory back pain (yes/no)
            arthritis (str): Past or present active synovitis (yes/no)
            enthesitis (str): Heel enthesitis (yes/no)
            uveitis (str): Past or present anterior uveitis (yes/no)
            dactylitis (str): Past or present dactylitis (yes/no)
            psoriasis (str): Past or present psoriasis (yes/no)
            crohns_colitis (str): Past or present Crohn's/colitis (yes/no)
            good_response_nsaids (str): Good response to NSAIDs (yes/no)
            family_history (str): Family history of SpA diseases (yes/no)
            elevated_crp (str): Elevated CRP (yes/no)
            
        Returns:
            Dict with the classification result and interpretation
        """
        
        # Validations
        self._validate_inputs(
            back_pain_duration_months, age_at_onset, sacroiliitis_imaging,
            hla_b27_positive, inflammatory_back_pain, arthritis, enthesitis,
            uveitis, dactylitis, psoriasis, crohns_colitis, good_response_nsaids,
            family_history, elevated_crp
        )
        
        # Check entry criterion
        entry_criterion_met = self._check_entry_criterion(
            back_pain_duration_months, age_at_onset
        )
        
        if not entry_criterion_met:
            return {
                "result": -1,
                "unit": "",
                "interpretation": "Entry criterion (back pain ≥3 months and age at onset <45 years) not fulfilled. ASAS criteria cannot be applied.",
                "stage": "Entry Criterion Not Met",
                "stage_description": "Entry criterion not fulfilled"
            }
        
        # Count SpA features
        spa_features_present = self._count_spa_features(
            inflammatory_back_pain, arthritis, enthesitis, uveitis,
            dactylitis, psoriasis, crohns_colitis, good_response_nsaids,
            family_history, elevated_crp
        )
        
        # Apply ASAS classification logic
        classification_result = self._apply_classification_logic(
            sacroiliitis_imaging, hla_b27_positive, spa_features_present
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(classification_result)
        
        # Map string result to numeric value for consistency with JSON structure
        result_mapping = {
            "Axial SpA": 1,
            "Not Axial SpA": 0,
            "Entry Criterion Not Met": -1
        }
        
        return {
            "result": result_mapping.get(classification_result, 0),
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, back_pain_duration_months, age_at_onset, 
                        sacroiliitis_imaging, hla_b27_positive, inflammatory_back_pain,
                        arthritis, enthesitis, uveitis, dactylitis, psoriasis,
                        crohns_colitis, good_response_nsaids, family_history, elevated_crp):
        """Validates input parameters"""
        
        if not isinstance(back_pain_duration_months, int):
            raise ValueError("Back pain duration must be an integer")
        
        if back_pain_duration_months < 0 or back_pain_duration_months > 1200:
            raise ValueError("Back pain duration must be between 0 and 1200 months")
        
        if not isinstance(age_at_onset, int):
            raise ValueError("Age at onset must be an integer")
        
        if age_at_onset < 0 or age_at_onset > 100:
            raise ValueError("Age at onset must be between 0 and 100 years")
        
        valid_present_absent = ["present", "absent"]
        if sacroiliitis_imaging not in valid_present_absent:
            raise ValueError("Sacroiliitis imaging must be 'present' or 'absent'")
        
        valid_yes_no = ["yes", "no"]
        yes_no_params = [
            hla_b27_positive, inflammatory_back_pain, arthritis, enthesitis,
            uveitis, dactylitis, psoriasis, crohns_colitis, good_response_nsaids,
            family_history, elevated_crp
        ]
        
        for param in yes_no_params:
            if param not in valid_yes_no:
                raise ValueError("All clinical parameters must be 'yes' or 'no'")
    
    def _check_entry_criterion(self, back_pain_duration_months: int, age_at_onset: int) -> bool:
        """
        Checks if entry criterion is met
        
        Entry criterion: Back pain ≥3 months AND age at onset <45 years
        """
        return back_pain_duration_months >= 3 and age_at_onset < 45
    
    def _count_spa_features(self, inflammatory_back_pain, arthritis, enthesitis,
                           uveitis, dactylitis, psoriasis, crohns_colitis,
                           good_response_nsaids, family_history, elevated_crp) -> int:
        """Counts the number of SpA features present"""
        
        features = [
            inflammatory_back_pain, arthritis, enthesitis, uveitis,
            dactylitis, psoriasis, crohns_colitis, good_response_nsaids,
            family_history, elevated_crp
        ]
        
        return sum(1 for feature in features if feature == "yes")
    
    def _apply_classification_logic(self, sacroiliitis_imaging: str, 
                                   hla_b27_positive: str, spa_features_count: int) -> str:
        """
        Applies ASAS classification logic
        
        Two arms:
        - Imaging arm: Sacroiliitis on imaging + ≥1 SpA feature
        - Clinical arm: HLA-B27 positive + ≥2 SpA features
        """
        
        # Imaging arm
        imaging_arm_positive = (sacroiliitis_imaging == "present" and spa_features_count >= 1)
        
        # Clinical arm
        clinical_arm_positive = (hla_b27_positive == "yes" and spa_features_count >= 2)
        
        # Classification result
        if imaging_arm_positive or clinical_arm_positive:
            return "Axial SpA"
        else:
            return "Not Axial SpA"
    
    def _get_interpretation(self, classification_result: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the classification result
        
        Args:
            classification_result (str): The classification result
            
        Returns:
            Dict with interpretation details
        """
        
        if classification_result == "Axial SpA":
            return {
                "stage": "Axial SpA",
                "description": "Meets ASAS criteria for axial spondyloarthritis",
                "interpretation": "Patient fulfills the ASAS classification criteria for axial spondyloarthritis. Further rheumatological evaluation and appropriate treatment should be considered."
            }
        elif classification_result == "Not Axial SpA":
            return {
                "stage": "Not Axial SpA",
                "description": "Does not meet ASAS criteria",
                "interpretation": "Patient does not fulfill the ASAS classification criteria for axial spondyloarthritis. Consider alternative diagnoses and further evaluation if clinical suspicion remains high."
            }
        else:  # Entry Criterion Not Met
            return {
                "stage": "Entry Criterion Not Met",
                "description": "Entry criterion not fulfilled",
                "interpretation": "Entry criterion (back pain ≥3 months and age at onset <45 years) not fulfilled. ASAS criteria cannot be applied."
            }


def calculate_asas_axial_spa_criteria(back_pain_duration_months: int,
                                     age_at_onset: int,
                                     sacroiliitis_imaging: str,
                                     hla_b27_positive: str,
                                     inflammatory_back_pain: str,
                                     arthritis: str,
                                     enthesitis: str,
                                     uveitis: str,
                                     dactylitis: str,
                                     psoriasis: str,
                                     crohns_colitis: str,
                                     good_response_nsaids: str,
                                     family_history: str,
                                     elevated_crp: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_asas_axial_spa_criteria pattern
    """
    calculator = AsasAxialSpaCriteriaCalculator()
    return calculator.calculate(
        back_pain_duration_months, age_at_onset, sacroiliitis_imaging,
        hla_b27_positive, inflammatory_back_pain, arthritis, enthesitis,
        uveitis, dactylitis, psoriasis, crohns_colitis, good_response_nsaids,
        family_history, elevated_crp
    )
