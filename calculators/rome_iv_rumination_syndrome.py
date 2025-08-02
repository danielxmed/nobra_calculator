"""
Rome IV Diagnostic Criteria for Rumination Syndrome Calculator

Rome IV diagnostic assessment for rumination syndrome, a functional gastroduodenal 
disorder characterized by effortless regurgitation of recently ingested food followed 
by remastication and reswallowing or expulsion. This calculator implements the 
official Rome IV criteria requiring fulfillment of all diagnostic criteria for 
≥3 months with onset ≥6 months ago.

References (Vancouver style):
1. Stanghellini V, Chan FK, Hasler WL, Malagelada JR, Suzuki H, Tack J, Talley NJ. 
   Gastroduodenal disorders. Gastroenterology. 2016 May;150(6):1380-1392. 
   doi: 10.1053/j.gastro.2016.02.011.
2. Rome Foundation. Rome IV Diagnostic Criteria for Functional Gastrointestinal 
   Disorders. 4th ed. Raleigh, NC: Rome Foundation; 2016.
3. Barba E, Burri E, Accarino A, Cisternas D, Quiroga S, Monclus E, Navazo I, 
   Malagelada JR. Abdominothoracic mechanisms of functional abdominal distention 
   and correction by biofeedback. Gastroenterology. 2015 Apr;148(4):732-9. 
   doi: 10.1053/j.gastro.2014.12.006.
4. Kessing BF, Bredenoord AJ, Smout AJ. Objective manometric criteria for the 
   rumination syndrome. Am J Gastroenterol. 2014 Jan;109(1):52-9. 
   doi: 10.1038/ajg.2013.428.
"""

from typing import Dict, Any


class RomeIvRuminationSyndromeCalculator:
    """Calculator for Rome IV Diagnostic Criteria for Rumination Syndrome"""
    
    def __init__(self):
        # Rome IV diagnostic criteria constants
        self.POSITIVE_CRITERIA_REQUIRED = 2
        self.EXCLUSION_CRITERIA_REQUIRED = 7
        self.TOTAL_CRITERIA_REQUIRED = 9
    
    def calculate(
        self,
        persistent_recurrent_regurgitation: str,
        regurgitation_not_preceded_by_retching: str,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_heartburn_reflux: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_dysphagia: str,
        exclusion_persistent_vomiting: str
    ) -> Dict[str, Any]:
        """
        Applies Rome IV diagnostic criteria for rumination syndrome
        
        Rome IV criteria require ALL of the following for ≥3 months (onset ≥6 months ago):
        
        Positive Criteria (both must be met):
        1. Persistent/recurrent regurgitation of recently ingested food with remastication/reswallowing
        2. Regurgitation not preceded by retching (effortless regurgitation)
        
        Exclusion Criteria (all must be absent):
        3. No gastrointestinal bleeding
        4. No unexplained iron deficiency anemia
        5. No significant heartburn or esophageal reflux symptoms
        6. No unintentional weight loss
        7. No palpable abdominal mass or lymphadenopathy
        8. No dysphagia
        9. No persistent vomiting episodes
        
        Args:
            persistent_recurrent_regurgitation (str): Persistent regurgitation with remastication ("yes"/"no")
            regurgitation_not_preceded_by_retching (str): Effortless regurgitation ("yes"/"no")
            exclusion_gi_bleeding (str): No GI bleeding ("yes"/"no")
            exclusion_iron_deficiency_anemia (str): No iron deficiency anemia ("yes"/"no")
            exclusion_heartburn_reflux (str): No heartburn/reflux ("yes"/"no")
            exclusion_weight_loss (str): No weight loss ("yes"/"no")
            exclusion_abdominal_mass_lymphadenopathy (str): No masses/lymphadenopathy ("yes"/"no")
            exclusion_dysphagia (str): No dysphagia ("yes"/"no")
            exclusion_persistent_vomiting (str): No persistent vomiting ("yes"/"no")
            
        Returns:
            Dict with diagnostic result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            persistent_recurrent_regurgitation,
            regurgitation_not_preceded_by_retching,
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_heartburn_reflux,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_dysphagia,
            exclusion_persistent_vomiting
        )
        
        # Count criteria met
        positive_criteria_met = self._count_positive_criteria(
            persistent_recurrent_regurgitation,
            regurgitation_not_preceded_by_retching
        )
        
        exclusion_criteria_met = self._count_exclusion_criteria(
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_heartburn_reflux,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_dysphagia,
            exclusion_persistent_vomiting
        )
        
        # Determine diagnostic outcome
        diagnosis_met = self._evaluate_diagnosis(positive_criteria_met, exclusion_criteria_met)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_met, positive_criteria_met, exclusion_criteria_met)
        
        return {
            "result": "Positive" if diagnosis_met else "Negative",
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self,
        persistent_recurrent_regurgitation: str,
        regurgitation_not_preceded_by_retching: str,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_heartburn_reflux: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_dysphagia: str,
        exclusion_persistent_vomiting: str
    ):
        """Validates all input parameters"""
        
        parameters = [
            ("persistent_recurrent_regurgitation", persistent_recurrent_regurgitation),
            ("regurgitation_not_preceded_by_retching", regurgitation_not_preceded_by_retching),
            ("exclusion_gi_bleeding", exclusion_gi_bleeding),
            ("exclusion_iron_deficiency_anemia", exclusion_iron_deficiency_anemia),
            ("exclusion_heartburn_reflux", exclusion_heartburn_reflux),
            ("exclusion_weight_loss", exclusion_weight_loss),
            ("exclusion_abdominal_mass_lymphadenopathy", exclusion_abdominal_mass_lymphadenopathy),
            ("exclusion_dysphagia", exclusion_dysphagia),
            ("exclusion_persistent_vomiting", exclusion_persistent_vomiting)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string ('yes' or 'no')")
            
            if param_value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got: {param_value}")
    
    def _count_positive_criteria(
        self,
        persistent_recurrent_regurgitation: str,
        regurgitation_not_preceded_by_retching: str
    ) -> int:
        """
        Counts positive criteria met (both must be present for diagnosis)
        
        Returns:
            int: Number of positive criteria met (0-2)
        """
        criteria_met = 0
        
        # Criterion 1: Persistent/recurrent regurgitation with remastication
        if persistent_recurrent_regurgitation.lower() == "yes":
            criteria_met += 1
        
        # Criterion 2: Effortless regurgitation (not preceded by retching)
        if regurgitation_not_preceded_by_retching.lower() == "yes":
            criteria_met += 1
        
        return criteria_met
    
    def _count_exclusion_criteria(
        self,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_heartburn_reflux: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_dysphagia: str,
        exclusion_persistent_vomiting: str
    ) -> int:
        """
        Counts exclusion criteria met (all must be absent for diagnosis)
        
        Returns:
            int: Number of exclusion criteria met (0-7)
        """
        criteria_met = 0
        
        # All exclusion criteria must be "yes" (meaning the concerning feature is absent)
        exclusion_parameters = [
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_heartburn_reflux,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_dysphagia,
            exclusion_persistent_vomiting
        ]
        
        for exclusion in exclusion_parameters:
            if exclusion.lower() == "yes":
                criteria_met += 1
        
        return criteria_met
    
    def _evaluate_diagnosis(self, positive_criteria_met: int, exclusion_criteria_met: int) -> bool:
        """
        Evaluates whether Rome IV diagnostic criteria are fulfilled
        
        Args:
            positive_criteria_met (int): Number of positive criteria met
            exclusion_criteria_met (int): Number of exclusion criteria met
            
        Returns:
            bool: True if all criteria met, False otherwise
        """
        return (positive_criteria_met == self.POSITIVE_CRITERIA_REQUIRED and 
                exclusion_criteria_met == self.EXCLUSION_CRITERIA_REQUIRED)
    
    def _get_interpretation(
        self, 
        diagnosis_met: bool, 
        positive_criteria_met: int, 
        exclusion_criteria_met: int
    ) -> Dict[str, str]:
        """
        Provides clinical interpretation based on diagnostic outcome
        
        Args:
            diagnosis_met (bool): Whether all criteria are fulfilled
            positive_criteria_met (int): Number of positive criteria met
            exclusion_criteria_met (int): Number of exclusion criteria met
            
        Returns:
            Dict with clinical interpretation
        """
        
        if diagnosis_met:
            return {
                "stage": "Criteria Met",
                "description": "Meets Rome IV criteria",
                "interpretation": (
                    "Patient fulfills Rome IV diagnostic criteria for rumination syndrome. "
                    "Diagnosis is established when all criteria are met including persistent "
                    "regurgitation of recently ingested food with remastication and reswallowing, "
                    "effortless regurgitation without retching, and exclusion of organic causes. "
                    "Treatment focuses on behavioral interventions including diaphragmatic breathing "
                    "training, habit reversal therapy, and biofeedback. Dietary modifications and "
                    "psychological support may be beneficial."
                )
            }
        else:
            # Determine specific reason for non-fulfillment
            if positive_criteria_met < self.POSITIVE_CRITERIA_REQUIRED:
                missing_positive = self.POSITIVE_CRITERIA_REQUIRED - positive_criteria_met
                interpretation_detail = (
                    f"Patient does not fulfill Rome IV diagnostic criteria for rumination syndrome. "
                    f"{missing_positive} essential positive criteria not met. "
                )
            else:
                missing_exclusions = self.EXCLUSION_CRITERIA_REQUIRED - exclusion_criteria_met
                interpretation_detail = (
                    f"Patient does not fulfill Rome IV diagnostic criteria for rumination syndrome. "
                    f"{missing_exclusions} exclusion criteria not satisfied (alarm symptoms present). "
                )
            
            return {
                "stage": "Criteria Not Met",
                "description": "Does not meet Rome IV criteria",
                "interpretation": (
                    f"{interpretation_detail}"
                    "Consider alternative diagnoses including GERD with regurgitation, gastroparesis, "
                    "eating disorders, or organic gastrointestinal pathology. Further evaluation may "
                    "be needed including upper endoscopy, gastric emptying studies, and psychological "
                    "assessment as clinically indicated."
                )
            }


def calculate_rome_iv_rumination_syndrome(
    persistent_recurrent_regurgitation: str,
    regurgitation_not_preceded_by_retching: str,
    exclusion_gi_bleeding: str,
    exclusion_iron_deficiency_anemia: str,
    exclusion_heartburn_reflux: str,
    exclusion_weight_loss: str,
    exclusion_abdominal_mass_lymphadenopathy: str,
    exclusion_dysphagia: str,
    exclusion_persistent_vomiting: str
) -> Dict[str, Any]:
    """
    Convenience function for Rome IV Rumination Syndrome diagnostic assessment
    
    Applies the official Rome IV diagnostic criteria for rumination syndrome to determine
    if a patient meets the validated criteria for this functional gastroduodenal disorder.
    
    Args:
        persistent_recurrent_regurgitation (str): Persistent regurgitation pattern ("yes"/"no")
        regurgitation_not_preceded_by_retching (str): Effortless regurgitation ("yes"/"no")
        exclusion_gi_bleeding (str): Absence of GI bleeding ("yes"/"no")
        exclusion_iron_deficiency_anemia (str): Absence of iron deficiency anemia ("yes"/"no")
        exclusion_heartburn_reflux (str): Absence of heartburn/reflux ("yes"/"no")
        exclusion_weight_loss (str): Absence of weight loss ("yes"/"no")
        exclusion_abdominal_mass_lymphadenopathy (str): Absence of masses/lymphadenopathy ("yes"/"no")
        exclusion_dysphagia (str): Absence of dysphagia ("yes"/"no")
        exclusion_persistent_vomiting (str): Absence of persistent vomiting ("yes"/"no")
        
    Returns:
        Dict[str, Any]: Diagnostic result with clinical interpretation and management recommendations
    """
    calculator = RomeIvRuminationSyndromeCalculator()
    return calculator.calculate(
        persistent_recurrent_regurgitation,
        regurgitation_not_preceded_by_retching,
        exclusion_gi_bleeding,
        exclusion_iron_deficiency_anemia,
        exclusion_heartburn_reflux,
        exclusion_weight_loss,
        exclusion_abdominal_mass_lymphadenopathy,
        exclusion_dysphagia,
        exclusion_persistent_vomiting
    )