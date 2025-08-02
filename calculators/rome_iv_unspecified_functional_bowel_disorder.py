"""
Rome IV Diagnostic Criteria for Unspecified Functional Bowel Disorder Calculator

Rome IV diagnostic assessment for unspecified functional bowel disorder, a catch-all 
diagnosis for functional bowel symptoms that do not meet specific criteria for other 
functional bowel disorders. This calculator implements the official Rome IV criteria 
requiring bowel symptoms not attributable to organic etiology that persist for ≥3 months 
with onset ≥6 months prior to diagnosis, while excluding other functional disorders.

References (Vancouver style):
1. Lacy BE, Mearin F, Chang L, Chey WD, Lembo AJ, Simren M, Spiller R. Bowel disorders. 
   Gastroenterology. 2016 May;150(6):1393-1407.e5. doi: 10.1053/j.gastro.2016.02.031.
2. Rome Foundation. Rome IV Diagnostic Criteria for Functional Gastrointestinal 
   Disorders. 4th ed. Raleigh, NC: Rome Foundation; 2016.
3. Palsson OS, Whitehead WE, van Tilburg MA, Chang L, Chey W, Crowell MD, Keefer L, 
   Lembo AJ, Parkman HP, Rao SS, Sperber A, Spiegel B, Tack J, Vanner S, Walker LS, 
   Whorwell P, Yang M. Rome IV diagnostic questionnaires and tables for investigators 
   and clinicians. Gastroenterology. 2016 May;150(6):1481-1491. 
   doi: 10.1053/j.gastro.2016.02.014.
"""

from typing import Dict, Any


class RomeIvUnspecifiedFunctionalBowelDisorderCalculator:
    """Calculator for Rome IV Diagnostic Criteria for Unspecified Functional Bowel Disorder"""
    
    def __init__(self):
        # Rome IV diagnostic criteria constants
        self.INCLUSION_CRITERIA_REQUIRED = 2  # Temporal + Non-organic
        self.EXCLUSION_CRITERIA_REQUIRED = 4  # Exclude other functional disorders
        self.ALARM_SYMPTOMS_EXCLUDED = 7  # All alarm symptoms must be absent
        self.TOTAL_CRITERIA_REQUIRED = 13
    
    def calculate(
        self,
        bowel_symptoms_duration: str,
        symptoms_not_organic: str,
        exclusion_ibs_criteria: str,
        exclusion_functional_constipation: str,
        exclusion_functional_diarrhea: str,
        exclusion_functional_bloating: str,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_family_history_colon_cancer: str,
        exclusion_age_over_50_without_screening: str,
        exclusion_sudden_bowel_habit_change: str
    ) -> Dict[str, Any]:
        """
        Applies Rome IV diagnostic criteria for unspecified functional bowel disorder
        
        Rome IV criteria require ALL of the following for ≥3 months (onset ≥6 months ago):
        
        Inclusion Criteria (both must be met):
        1. Bowel symptoms present for ≥3 months with onset ≥6 months prior to diagnosis
        2. Bowel symptoms not attributable to organic etiology
        
        Exclusion of Other Functional Disorders (all must be excluded):
        3. Does not meet criteria for IBS
        4. Does not meet criteria for functional constipation
        5. Does not meet criteria for functional diarrhea
        6. Does not meet criteria for functional abdominal bloating/distension
        
        Exclusion of Alarm Symptoms (all must be absent):
        7. No gastrointestinal bleeding
        8. No unexplained iron deficiency anemia
        9. No unintentional weight loss
        10. No palpable abdominal mass or lymphadenopathy
        11. No family history of colon cancer without screening
        12. No symptom onset after age 50 without screening
        13. No sudden change in bowel habits
        
        Args:
            bowel_symptoms_duration (str): Temporal criteria met ("yes"/"no")
            symptoms_not_organic (str): Non-organic etiology ("yes"/"no")
            exclusion_ibs_criteria (str): Does not meet IBS criteria ("yes"/"no")
            exclusion_functional_constipation (str): Does not meet constipation criteria ("yes"/"no")
            exclusion_functional_diarrhea (str): Does not meet diarrhea criteria ("yes"/"no")
            exclusion_functional_bloating (str): Does not meet bloating criteria ("yes"/"no")
            exclusion_gi_bleeding (str): No GI bleeding ("yes"/"no")
            exclusion_iron_deficiency_anemia (str): No iron deficiency anemia ("yes"/"no")
            exclusion_weight_loss (str): No weight loss ("yes"/"no")
            exclusion_abdominal_mass_lymphadenopathy (str): No masses/lymphadenopathy ("yes"/"no")
            exclusion_family_history_colon_cancer (str): No family history without screening ("yes"/"no")
            exclusion_age_over_50_without_screening (str): No onset >50 without screening ("yes"/"no")
            exclusion_sudden_bowel_habit_change (str): No sudden bowel changes ("yes"/"no")
            
        Returns:
            Dict with diagnostic result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            bowel_symptoms_duration,
            symptoms_not_organic,
            exclusion_ibs_criteria,
            exclusion_functional_constipation,
            exclusion_functional_diarrhea,
            exclusion_functional_bloating,
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_family_history_colon_cancer,
            exclusion_age_over_50_without_screening,
            exclusion_sudden_bowel_habit_change
        )
        
        # Count criteria met
        inclusion_criteria_met = self._count_inclusion_criteria(
            bowel_symptoms_duration,
            symptoms_not_organic
        )
        
        functional_disorder_exclusions_met = self._count_functional_disorder_exclusions(
            exclusion_ibs_criteria,
            exclusion_functional_constipation,
            exclusion_functional_diarrhea,
            exclusion_functional_bloating
        )
        
        alarm_symptom_exclusions_met = self._count_alarm_symptom_exclusions(
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_family_history_colon_cancer,
            exclusion_age_over_50_without_screening,
            exclusion_sudden_bowel_habit_change
        )
        
        # Determine diagnostic outcome
        diagnosis_met = self._evaluate_diagnosis(
            inclusion_criteria_met,
            functional_disorder_exclusions_met,
            alarm_symptom_exclusions_met
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(
            diagnosis_met,
            inclusion_criteria_met,
            functional_disorder_exclusions_met,
            alarm_symptom_exclusions_met
        )
        
        return {
            "result": "Positive" if diagnosis_met else "Negative",
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self,
        bowel_symptoms_duration: str,
        symptoms_not_organic: str,
        exclusion_ibs_criteria: str,
        exclusion_functional_constipation: str,
        exclusion_functional_diarrhea: str,
        exclusion_functional_bloating: str,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_family_history_colon_cancer: str,
        exclusion_age_over_50_without_screening: str,
        exclusion_sudden_bowel_habit_change: str
    ):
        """Validates all input parameters"""
        
        parameters = [
            ("bowel_symptoms_duration", bowel_symptoms_duration),
            ("symptoms_not_organic", symptoms_not_organic),
            ("exclusion_ibs_criteria", exclusion_ibs_criteria),
            ("exclusion_functional_constipation", exclusion_functional_constipation),
            ("exclusion_functional_diarrhea", exclusion_functional_diarrhea),
            ("exclusion_functional_bloating", exclusion_functional_bloating),
            ("exclusion_gi_bleeding", exclusion_gi_bleeding),
            ("exclusion_iron_deficiency_anemia", exclusion_iron_deficiency_anemia),
            ("exclusion_weight_loss", exclusion_weight_loss),
            ("exclusion_abdominal_mass_lymphadenopathy", exclusion_abdominal_mass_lymphadenopathy),
            ("exclusion_family_history_colon_cancer", exclusion_family_history_colon_cancer),
            ("exclusion_age_over_50_without_screening", exclusion_age_over_50_without_screening),
            ("exclusion_sudden_bowel_habit_change", exclusion_sudden_bowel_habit_change)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string ('yes' or 'no')")
            
            if param_value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got: {param_value}")
    
    def _count_inclusion_criteria(
        self,
        bowel_symptoms_duration: str,
        symptoms_not_organic: str
    ) -> int:
        """
        Counts inclusion criteria met (both must be present for diagnosis)
        
        Returns:
            int: Number of inclusion criteria met (0-2)
        """
        criteria_met = 0
        
        # Criterion 1: Temporal requirements
        if bowel_symptoms_duration.lower() == "yes":
            criteria_met += 1
        
        # Criterion 2: Non-organic etiology
        if symptoms_not_organic.lower() == "yes":
            criteria_met += 1
        
        return criteria_met
    
    def _count_functional_disorder_exclusions(
        self,
        exclusion_ibs_criteria: str,
        exclusion_functional_constipation: str,
        exclusion_functional_diarrhea: str,
        exclusion_functional_bloating: str
    ) -> int:
        """
        Counts functional disorder exclusions met (all must be excluded for diagnosis)
        
        Returns:
            int: Number of functional disorder exclusions met (0-4)
        """
        criteria_met = 0
        
        functional_exclusions = [
            exclusion_ibs_criteria,
            exclusion_functional_constipation,
            exclusion_functional_diarrhea,
            exclusion_functional_bloating
        ]
        
        for exclusion in functional_exclusions:
            if exclusion.lower() == "yes":
                criteria_met += 1
        
        return criteria_met
    
    def _count_alarm_symptom_exclusions(
        self,
        exclusion_gi_bleeding: str,
        exclusion_iron_deficiency_anemia: str,
        exclusion_weight_loss: str,
        exclusion_abdominal_mass_lymphadenopathy: str,
        exclusion_family_history_colon_cancer: str,
        exclusion_age_over_50_without_screening: str,
        exclusion_sudden_bowel_habit_change: str
    ) -> int:
        """
        Counts alarm symptom exclusions met (all must be absent for diagnosis)
        
        Returns:
            int: Number of alarm symptom exclusions met (0-7)
        """
        criteria_met = 0
        
        alarm_exclusions = [
            exclusion_gi_bleeding,
            exclusion_iron_deficiency_anemia,
            exclusion_weight_loss,
            exclusion_abdominal_mass_lymphadenopathy,
            exclusion_family_history_colon_cancer,
            exclusion_age_over_50_without_screening,
            exclusion_sudden_bowel_habit_change
        ]
        
        for exclusion in alarm_exclusions:
            if exclusion.lower() == "yes":
                criteria_met += 1
        
        return criteria_met
    
    def _evaluate_diagnosis(
        self,
        inclusion_criteria_met: int,
        functional_disorder_exclusions_met: int,
        alarm_symptom_exclusions_met: int
    ) -> bool:
        """
        Evaluates whether Rome IV diagnostic criteria are fulfilled
        
        Args:
            inclusion_criteria_met (int): Number of inclusion criteria met
            functional_disorder_exclusions_met (int): Number of functional disorder exclusions met
            alarm_symptom_exclusions_met (int): Number of alarm symptom exclusions met
            
        Returns:
            bool: True if all criteria met, False otherwise
        """
        return (inclusion_criteria_met == self.INCLUSION_CRITERIA_REQUIRED and 
                functional_disorder_exclusions_met == self.EXCLUSION_CRITERIA_REQUIRED and
                alarm_symptom_exclusions_met == self.ALARM_SYMPTOMS_EXCLUDED)
    
    def _get_interpretation(
        self, 
        diagnosis_met: bool,
        inclusion_criteria_met: int,
        functional_disorder_exclusions_met: int,
        alarm_symptom_exclusions_met: int
    ) -> Dict[str, str]:
        """
        Provides clinical interpretation based on diagnostic outcome
        
        Args:
            diagnosis_met (bool): Whether all criteria are fulfilled
            inclusion_criteria_met (int): Number of inclusion criteria met
            functional_disorder_exclusions_met (int): Number of functional disorder exclusions met
            alarm_symptom_exclusions_met (int): Number of alarm symptom exclusions met
            
        Returns:
            Dict with clinical interpretation
        """
        
        if diagnosis_met:
            return {
                "stage": "Criteria Met",
                "description": "Meets Rome IV criteria",
                "interpretation": (
                    "Patient fulfills Rome IV diagnostic criteria for unspecified functional bowel disorder. "
                    "This diagnosis applies to bowel symptoms not attributable to organic etiology that do not "
                    "meet criteria for IBS, functional constipation, functional diarrhea, or functional abdominal "
                    "bloating/distension disorders. Management should be guided by individual patient symptoms and "
                    "severity. No specific standardized treatment exists, but symptom-directed therapy may include "
                    "dietary modifications, probiotics, antispasmodics, or other supportive measures as clinically indicated."
                )
            }
        else:
            # Determine specific reason for non-fulfillment
            if inclusion_criteria_met < self.INCLUSION_CRITERIA_REQUIRED:
                if inclusion_criteria_met == 0:
                    interpretation_detail = (
                        "Patient does not fulfill Rome IV diagnostic criteria for unspecified functional bowel disorder. "
                        "Neither temporal criteria nor functional etiology established. "
                    )
                else:
                    interpretation_detail = (
                        "Patient does not fulfill Rome IV diagnostic criteria for unspecified functional bowel disorder. "
                        "One inclusion criterion not met (either temporal requirements or functional etiology). "
                    )
            elif functional_disorder_exclusions_met < self.EXCLUSION_CRITERIA_REQUIRED:
                missing_exclusions = self.EXCLUSION_CRITERIA_REQUIRED - functional_disorder_exclusions_met
                interpretation_detail = (
                    f"Patient does not fulfill Rome IV diagnostic criteria for unspecified functional bowel disorder. "
                    f"Patient meets criteria for a more specific functional bowel disorder. "
                )
            else:
                missing_alarm_exclusions = self.ALARM_SYMPTOMS_EXCLUDED - alarm_symptom_exclusions_met
                interpretation_detail = (
                    f"Patient does not fulfill Rome IV diagnostic criteria for unspecified functional bowel disorder. "
                    f"{missing_alarm_exclusions} alarm symptoms present requiring evaluation. "
                )
            
            return {
                "stage": "Criteria Not Met",
                "description": "Does not meet Rome IV criteria",
                "interpretation": (
                    f"{interpretation_detail}"
                    "Consider appropriate evaluation based on specific criteria not met. "
                    "If alarm symptoms are present, further investigation including imaging, endoscopy, "
                    "and laboratory studies may be indicated."
                )
            }


def calculate_rome_iv_unspecified_functional_bowel_disorder(
    bowel_symptoms_duration: str,
    symptoms_not_organic: str,
    exclusion_ibs_criteria: str,
    exclusion_functional_constipation: str,
    exclusion_functional_diarrhea: str,
    exclusion_functional_bloating: str,
    exclusion_gi_bleeding: str,
    exclusion_iron_deficiency_anemia: str,
    exclusion_weight_loss: str,
    exclusion_abdominal_mass_lymphadenopathy: str,
    exclusion_family_history_colon_cancer: str,
    exclusion_age_over_50_without_screening: str,
    exclusion_sudden_bowel_habit_change: str
) -> Dict[str, Any]:
    """
    Convenience function for Rome IV Unspecified Functional Bowel Disorder diagnostic assessment
    
    Applies the official Rome IV diagnostic criteria for unspecified functional bowel disorder
    to determine if a patient meets the validated criteria for this catch-all functional disorder.
    
    Args:
        bowel_symptoms_duration (str): Temporal criteria (≥3 months, onset ≥6 months ago) ("yes"/"no")
        symptoms_not_organic (str): Non-organic etiology ("yes"/"no")
        exclusion_ibs_criteria (str): Does not meet IBS criteria ("yes"/"no")
        exclusion_functional_constipation (str): Does not meet constipation criteria ("yes"/"no")
        exclusion_functional_diarrhea (str): Does not meet diarrhea criteria ("yes"/"no")
        exclusion_functional_bloating (str): Does not meet bloating criteria ("yes"/"no")
        exclusion_gi_bleeding (str): Absence of GI bleeding ("yes"/"no")
        exclusion_iron_deficiency_anemia (str): Absence of iron deficiency anemia ("yes"/"no")
        exclusion_weight_loss (str): Absence of weight loss ("yes"/"no")
        exclusion_abdominal_mass_lymphadenopathy (str): Absence of masses/lymphadenopathy ("yes"/"no")
        exclusion_family_history_colon_cancer (str): No family history without screening ("yes"/"no")
        exclusion_age_over_50_without_screening (str): No onset >50 without screening ("yes"/"no")
        exclusion_sudden_bowel_habit_change (str): No sudden bowel changes ("yes"/"no")
        
    Returns:
        Dict[str, Any]: Diagnostic result with clinical interpretation and management recommendations
    """
    calculator = RomeIvUnspecifiedFunctionalBowelDisorderCalculator()
    return calculator.calculate(
        bowel_symptoms_duration,
        symptoms_not_organic,
        exclusion_ibs_criteria,
        exclusion_functional_constipation,
        exclusion_functional_diarrhea,
        exclusion_functional_bloating,
        exclusion_gi_bleeding,
        exclusion_iron_deficiency_anemia,
        exclusion_weight_loss,
        exclusion_abdominal_mass_lymphadenopathy,
        exclusion_family_history_colon_cancer,
        exclusion_age_over_50_without_screening,
        exclusion_sudden_bowel_habit_change
    )