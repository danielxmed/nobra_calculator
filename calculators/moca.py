"""
Montreal Cognitive Assessment (MoCA) Calculator

Screens for mild cognitive impairment with assessment of multiple cognitive domains
including attention, executive function, memory, language, visuospatial skills,
abstraction, and orientation.

References:
1. Nasreddine ZS, et al. J Am Geriatr Soc. 2005;53(4):695-9.
2. Luis CA, et al. Int J Geriatr Psychiatry. 2009;24(2):197-201.
3. Roalf DR, et al. Alzheimers Dement. 2013;9(5):529-37.
"""

from typing import Dict, Any


class MocaCalculator:
    """Calculator for Montreal Cognitive Assessment (MoCA)"""
    
    def __init__(self):
        # Domain maximum scores
        self.DOMAIN_MAXES = {
            "visuospatial_executive": 5,
            "naming": 3,
            "attention": 6,
            "language": 3,
            "abstraction": 2,
            "delayed_recall": 5,
            "orientation": 6
        }
        
        # Total possible score (excluding memory registration which is not counted)
        self.MAX_SCORE = 30
    
    def calculate(self, visuospatial_executive: int, naming: int, memory_registration: int,
                  attention: int, language: int, abstraction: int, delayed_recall: int,
                  orientation: int, education_level: str) -> Dict[str, Any]:
        """
        Calculates the MoCA score for cognitive assessment
        
        Args:
            visuospatial_executive (int): Visuospatial/Executive score (0-5)
            naming (int): Naming score (0-3)
            memory_registration (int): Memory registration (not counted in total)
            attention (int): Attention score (0-6)
            language (int): Language score (0-3)
            abstraction (int): Abstraction score (0-2)
            delayed_recall (int): Delayed recall score (0-5)
            orientation (int): Orientation score (0-6)
            education_level (str): Education level for adjustment
            
        Returns:
            Dict with MoCA score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(visuospatial_executive, naming, memory_registration,
                             attention, language, abstraction, delayed_recall,
                             orientation, education_level)
        
        # Calculate raw score (excluding memory registration)
        raw_score = (visuospatial_executive + naming + attention + language +
                     abstraction + delayed_recall + orientation)
        
        # Apply education adjustment
        adjusted_score = self._apply_education_adjustment(raw_score, education_level)
        
        # Get interpretation
        interpretation = self._get_interpretation(adjusted_score)
        
        return {
            "result": adjusted_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, visuospatial_executive: int, naming: int, memory_registration: int,
                        attention: int, language: int, abstraction: int, delayed_recall: int,
                        orientation: int, education_level: str):
        """Validates input parameters"""
        
        # Check all scores are integers
        scores = {
            "visuospatial_executive": visuospatial_executive,
            "naming": naming,
            "memory_registration": memory_registration,
            "attention": attention,
            "language": language,
            "abstraction": abstraction,
            "delayed_recall": delayed_recall,
            "orientation": orientation
        }
        
        for domain, score in scores.items():
            if not isinstance(score, int):
                raise ValueError(f"{domain} score must be an integer")
            
            if domain == "memory_registration":
                max_score = 5  # Memory registration has max 5 but not counted in total
            else:
                max_score = self.DOMAIN_MAXES[domain]
            
            if score < 0 or score > max_score:
                raise ValueError(f"{domain} score must be between 0 and {max_score}")
        
        # Validate education level
        if education_level not in ["less_than_12_years", "12_or_more_years"]:
            raise ValueError("Education level must be 'less_than_12_years' or '12_or_more_years'")
    
    def _apply_education_adjustment(self, raw_score: int, education_level: str) -> int:
        """Applies education adjustment to raw score"""
        
        # Add 1 point if education ≤12 years
        if education_level == "less_than_12_years":
            adjusted_score = min(raw_score + 1, self.MAX_SCORE)
        else:
            adjusted_score = raw_score
        
        return adjusted_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on MoCA score
        
        Args:
            score (int): Adjusted MoCA score
            
        Returns:
            Dict with interpretation details
        """
        
        if score >= 26:
            return {
                "stage": "Normal Cognition",
                "description": "Normal cognitive function",
                "interpretation": (f"MoCA Score {score}: Normal cognitive function. This score indicates "
                                f"intact cognitive abilities across all assessed domains including visuospatial/executive "
                                f"function, naming, attention, language, abstraction, memory, and orientation. No cognitive "
                                f"impairment is detected. This score suggests the individual is functioning at an expected "
                                f"cognitive level for their age and education. Regular cognitive health maintenance through "
                                f"mental stimulation, physical exercise, and social engagement is recommended. Routine "
                                f"cognitive screening may be appropriate during regular healthcare visits, especially for "
                                f"individuals with risk factors for cognitive decline such as cardiovascular disease, "
                                f"diabetes, or family history of dementia.")
            }
        elif score >= 18:
            return {
                "stage": "Mild Cognitive Impairment",
                "description": "Possible mild cognitive impairment",
                "interpretation": (f"MoCA Score {score}: Possible mild cognitive impairment (MCI). This score suggests "
                                f"subtle cognitive changes that may affect daily functioning but do not meet criteria for "
                                f"dementia. Further comprehensive neuropsychological evaluation is recommended to confirm "
                                f"the diagnosis and identify specific cognitive domains affected. Consider assessment of "
                                f"activities of daily living, depression screening, and evaluation of potential reversible "
                                f"causes of cognitive impairment such as medication effects, sleep disorders, vitamin "
                                f"deficiencies, or thyroid dysfunction. Regular monitoring is essential as individuals "
                                f"with MCI have increased risk of progression to dementia. Cognitive training, lifestyle "
                                f"modifications including regular exercise, Mediterranean diet, social engagement, and "
                                f"management of cardiovascular risk factors may help slow cognitive decline.")
            }
        elif score >= 10:
            return {
                "stage": "Moderate Cognitive Impairment",
                "description": "Moderate cognitive impairment",
                "interpretation": (f"MoCA Score {score}: Moderate cognitive impairment. This score indicates significant "
                                f"cognitive decline that likely affects multiple domains of cognitive function and impacts "
                                f"daily activities and independence. Comprehensive evaluation is needed including detailed "
                                f"neuropsychological testing, brain imaging (MRI), laboratory studies to exclude reversible "
                                f"causes, and assessment of functional abilities. Consider referral to neurology, geriatrics, "
                                f"or memory disorders clinic for specialized evaluation and management. Assessment of decision-"
                                f"making capacity, safety concerns, and need for supervision or support services is important. "
                                f"Family education about cognitive impairment, safety planning, legal and financial planning, "
                                f"and caregiver support resources should be provided. Treatment may include cholinesterase "
                                f"inhibitors or other medications depending on underlying etiology. Regular monitoring for "
                                f"progression and adjustment of care plan is essential.")
            }
        else:  # score 0-9
            return {
                "stage": "Severe Cognitive Impairment",
                "description": "Severe cognitive impairment",
                "interpretation": (f"MoCA Score {score}: Severe cognitive impairment. This score indicates marked "
                                f"cognitive decline across multiple domains that significantly impairs daily functioning "
                                f"and independence. Immediate comprehensive evaluation is required including neurological "
                                f"assessment, brain imaging, laboratory studies, and functional assessment. Consider urgent "
                                f"referral to neurology or memory disorders specialty clinic. Assessment of safety, "
                                f"decision-making capacity, and need for supervised care or placement is critical. "
                                f"Evaluation for reversible causes of cognitive impairment should be prioritized. "
                                f"Family meeting to discuss diagnosis, prognosis, care planning, safety concerns, and "
                                f"available support services is essential. Consider advanced directives and legal/financial "
                                f"planning while some capacity may remain. Treatment may include medications for underlying "
                                f"dementia if appropriate, management of behavioral symptoms, and comprehensive care "
                                f"coordination. Regular monitoring for complications, caregiver support, and end-of-life "
                                f"planning discussions may be needed.")
            }


def calculate_moca(visuospatial_executive: int, naming: int, memory_registration: int,
                  attention: int, language: int, abstraction: int, delayed_recall: int,
                  orientation: int, education_level: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MocaCalculator()
    return calculator.calculate(visuospatial_executive, naming, memory_registration,
                               attention, language, abstraction, delayed_recall,
                               orientation, education_level)