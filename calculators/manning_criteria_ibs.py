"""
Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS) Calculator

Determines likelihood of IBS diagnosis based on six clinically significant criteria
related to abdominal pain and stool characteristics. Includes red flag assessment.

References:
1. Manning AP, Thompson WG, Heaton KW, Morris AF. Towards positive diagnosis of the 
   irritable bowel. Br Med J. 1978 Sep 2;2(6138):653-4. doi: 10.1136/bmj.2.6138.653.
2. Thompson WG, Heaton KW, Smyth GT, Smyth C. Irritable bowel syndrome in general 
   practice: prevalence, characteristics, and referral. Gut. 2000 Jan;46(1):78-82. 
   doi: 10.1136/gut.46.1.78.
"""

from typing import Dict, Any


class ManningCriteriaIbsCalculator:
    """Calculator for Manning Criteria for IBS Diagnosis"""
    
    def __init__(self):
        # Diagnostic thresholds
        self.DIAGNOSTIC_THRESHOLD = 3  # Minimum criteria for IBS diagnosis
        self.RED_FLAG_AGE_THRESHOLD = 50  # Age threshold for red flag
        
        # Valid options
        self.VALID_YES_NO_OPTIONS = ["yes", "no"]
    
    def calculate(self, pain_onset_frequent_bowel_movements: str, looser_stools_with_pain_onset: str,
                  pain_relief_with_defecation: str, noticeable_abdominal_bloating: str,
                  incomplete_evacuation_sensation: str, diarrhea_with_mucus: str,
                  patient_age: int, weight_loss: str, blood_in_stools: str,
                  anemia: str, fever: str) -> Dict[str, Any]:
        """
        Calculates Manning Criteria score for IBS diagnosis
        
        Args:
            pain_onset_frequent_bowel_movements (str): Pain onset with frequent BM ("yes"/"no")
            looser_stools_with_pain_onset (str): Looser stools with pain onset ("yes"/"no")
            pain_relief_with_defecation (str): Pain relief with defecation ("yes"/"no")
            noticeable_abdominal_bloating (str): Visible abdominal bloating ("yes"/"no")
            incomplete_evacuation_sensation (str): Incomplete evacuation >25% time ("yes"/"no")
            diarrhea_with_mucus (str): Diarrhea with mucus >25% time ("yes"/"no")
            patient_age (int): Patient age in years
            weight_loss (str): Presence of weight loss ("yes"/"no")
            blood_in_stools (str): Blood in stools ("yes"/"no")
            anemia (str): Presence of anemia ("yes"/"no")
            fever (str): Presence of fever ("yes"/"no")
            
        Returns:
            Dict with the result, red flag assessment, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pain_onset_frequent_bowel_movements, looser_stools_with_pain_onset,
                             pain_relief_with_defecation, noticeable_abdominal_bloating,
                             incomplete_evacuation_sensation, diarrhea_with_mucus,
                             patient_age, weight_loss, blood_in_stools, anemia, fever)
        
        # Calculate Manning criteria score
        criteria_scores = self._calculate_criteria_scores(
            pain_onset_frequent_bowel_movements, looser_stools_with_pain_onset,
            pain_relief_with_defecation, noticeable_abdominal_bloating,
            incomplete_evacuation_sensation, diarrhea_with_mucus
        )
        
        total_criteria = sum(criteria_scores.values())
        
        # Assess red flags
        red_flags = self._assess_red_flags(patient_age, weight_loss, blood_in_stools, anemia, fever)
        has_red_flags = any(red_flags.values())
        
        # Get interpretation
        interpretation_data = self._get_interpretation(total_criteria, has_red_flags)
        
        # Get detailed assessment
        assessment_data = self._get_assessment_data(total_criteria, has_red_flags, red_flags)
        
        return {
            "result": {
                "total_criteria": total_criteria,
                "criteria_scores": criteria_scores,
                "red_flags": red_flags,
                "has_red_flags": has_red_flags,
                "criteria_breakdown": {
                    "pain_onset_frequent_bm": f"Pain onset with frequent BM: {'Yes' if criteria_scores['pain_onset_frequent_bm'] else 'No'}",
                    "looser_stools_with_pain": f"Looser stools with pain: {'Yes' if criteria_scores['looser_stools_with_pain'] else 'No'}",
                    "pain_relief_defecation": f"Pain relief with defecation: {'Yes' if criteria_scores['pain_relief_defecation'] else 'No'}",
                    "abdominal_bloating": f"Abdominal bloating: {'Yes' if criteria_scores['abdominal_bloating'] else 'No'}",
                    "incomplete_evacuation": f"Incomplete evacuation: {'Yes' if criteria_scores['incomplete_evacuation'] else 'No'}",
                    "diarrhea_with_mucus": f"Diarrhea with mucus: {'Yes' if criteria_scores['diarrhea_with_mucus'] else 'No'}"
                },
                "red_flag_breakdown": {
                    "age_over_50": f"Age >50 years: {'Yes' if red_flags['age_over_50'] else 'No'} (Age: {patient_age})",
                    "weight_loss": f"Weight loss: {'Yes' if red_flags['weight_loss'] else 'No'}",
                    "blood_in_stools": f"Blood in stools: {'Yes' if red_flags['blood_in_stools'] else 'No'}",
                    "anemia": f"Anemia: {'Yes' if red_flags['anemia'] else 'No'}",
                    "fever": f"Fever: {'Yes' if red_flags['fever'] else 'No'}"
                },
                "assessment_data": assessment_data
            },
            "unit": "criteria",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, pain_onset_frequent_bowel_movements: str, looser_stools_with_pain_onset: str,
                        pain_relief_with_defecation: str, noticeable_abdominal_bloating: str,
                        incomplete_evacuation_sensation: str, diarrhea_with_mucus: str,
                        patient_age: int, weight_loss: str, blood_in_stools: str,
                        anemia: str, fever: str):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = {
            "pain_onset_frequent_bowel_movements": pain_onset_frequent_bowel_movements,
            "looser_stools_with_pain_onset": looser_stools_with_pain_onset,
            "pain_relief_with_defecation": pain_relief_with_defecation,
            "noticeable_abdominal_bloating": noticeable_abdominal_bloating,
            "incomplete_evacuation_sensation": incomplete_evacuation_sensation,
            "diarrhea_with_mucus": diarrhea_with_mucus,
            "weight_loss": weight_loss,
            "blood_in_stools": blood_in_stools,
            "anemia": anemia,
            "fever": fever
        }
        
        for param_name, param_value in yes_no_params.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in [option.lower() for option in self.VALID_YES_NO_OPTIONS]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate age
        if not isinstance(patient_age, int):
            raise ValueError("Patient age must be an integer")
        
        if patient_age < 10 or patient_age > 100:
            raise ValueError("Patient age must be between 10 and 100 years")
    
    def _calculate_criteria_scores(self, pain_onset_frequent_bowel_movements: str,
                                  looser_stools_with_pain_onset: str, pain_relief_with_defecation: str,
                                  noticeable_abdominal_bloating: str, incomplete_evacuation_sensation: str,
                                  diarrhea_with_mucus: str) -> Dict[str, int]:
        """Calculates individual Manning criteria scores"""
        
        return {
            "pain_onset_frequent_bm": 1 if pain_onset_frequent_bowel_movements.lower() == "yes" else 0,
            "looser_stools_with_pain": 1 if looser_stools_with_pain_onset.lower() == "yes" else 0,
            "pain_relief_defecation": 1 if pain_relief_with_defecation.lower() == "yes" else 0,
            "abdominal_bloating": 1 if noticeable_abdominal_bloating.lower() == "yes" else 0,
            "incomplete_evacuation": 1 if incomplete_evacuation_sensation.lower() == "yes" else 0,
            "diarrhea_with_mucus": 1 if diarrhea_with_mucus.lower() == "yes" else 0
        }
    
    def _assess_red_flags(self, patient_age: int, weight_loss: str, blood_in_stools: str,
                         anemia: str, fever: str) -> Dict[str, bool]:
        """Assesses red flag symptoms that contraindicate IBS diagnosis"""
        
        return {
            "age_over_50": patient_age > self.RED_FLAG_AGE_THRESHOLD,
            "weight_loss": weight_loss.lower() == "yes",
            "blood_in_stools": blood_in_stools.lower() == "yes",
            "anemia": anemia.lower() == "yes",
            "fever": fever.lower() == "yes"
        }
    
    def _get_assessment_data(self, total_criteria: int, has_red_flags: bool,
                           red_flags: Dict[str, bool]) -> Dict[str, str]:
        """
        Returns detailed assessment data based on Manning criteria and red flags
        
        Args:
            total_criteria (int): Total Manning criteria met
            has_red_flags (bool): Whether any red flags are present
            red_flags (Dict[str, bool]): Individual red flag status
            
        Returns:
            Dict with assessment information
        """
        
        # Determine diagnostic likelihood
        if total_criteria >= self.DIAGNOSTIC_THRESHOLD and not has_red_flags:
            diagnostic_likelihood = "IBS diagnosis supported"
            recommendation = "Consider IBS treatment and management"
        elif total_criteria >= self.DIAGNOSTIC_THRESHOLD and has_red_flags:
            diagnostic_likelihood = "Further evaluation required"
            recommendation = "Investigate red flag symptoms before IBS diagnosis"
        else:
            diagnostic_likelihood = "IBS diagnosis not supported"
            recommendation = "Consider alternative diagnoses"
        
        # Identify present red flags
        present_red_flags = [flag for flag, present in red_flags.items() if present]
        red_flag_summary = ", ".join(present_red_flags) if present_red_flags else "None"
        
        return {
            "diagnostic_likelihood": diagnostic_likelihood,
            "recommendation": recommendation,
            "criteria_threshold": f"≥{self.DIAGNOSTIC_THRESHOLD} criteria needed",
            "present_red_flags": red_flag_summary,
            "sensitivity_range": "63-90%",
            "specificity_range": "70-93%",
            "next_steps": "Consider Rome IV criteria and appropriate investigations"
        }
    
    def _get_interpretation(self, total_criteria: int, has_red_flags: bool) -> Dict[str, str]:
        """
        Determines the diagnostic category and interpretation
        
        Args:
            total_criteria (int): Total Manning criteria met
            has_red_flags (bool): Whether any red flags are present
            
        Returns:
            Dict with diagnostic category and clinical interpretation
        """
        
        if total_criteria < self.DIAGNOSTIC_THRESHOLD:  # <3 criteria
            return {
                "stage": "IBS Unlikely",
                "description": "Insufficient criteria for IBS diagnosis",
                "interpretation": (
                    f"Only {total_criteria} of 6 Manning criteria met (minimum 3 required). "
                    "IBS diagnosis is unlikely based on current symptom pattern. Consider "
                    "alternative diagnoses including functional dyspepsia, inflammatory bowel "
                    "disease, celiac disease, gastroparesis, or other organic gastrointestinal "
                    "conditions. Further evaluation may be warranted based on clinical presentation "
                    "including appropriate laboratory studies, imaging, and possibly endoscopic "
                    "evaluation. Rome IV criteria may provide additional diagnostic guidance."
                )
            }
        else:  # ≥3 criteria
            if has_red_flags:
                return {
                    "stage": "Further Evaluation Required",
                    "description": "Sufficient criteria but red flags present",
                    "interpretation": (
                        f"{total_criteria} of 6 Manning criteria met, suggesting possible IBS. "
                        "However, red flag symptoms are present which require investigation before "
                        "establishing IBS diagnosis. Red flags may indicate organic gastrointestinal "
                        "disease requiring specific treatment. Recommended workup may include "
                        "complete blood count, inflammatory markers (ESR, CRP), celiac serology, "
                        "stool studies, and consider colonoscopy or other imaging as clinically "
                        "indicated. IBS diagnosis should only be considered after excluding "
                        "organic pathology."
                    )
                }
            else:
                return {
                    "stage": "IBS Likely",
                    "description": "Sufficient criteria for IBS diagnosis with no red flags",
                    "interpretation": (
                        f"{total_criteria} of 6 Manning criteria met with no red flag symptoms present. "
                        "This supports a diagnosis of irritable bowel syndrome. Consider initiating "
                        "symptomatic treatment including dietary modifications (low FODMAP diet), "
                        "antispasmodics, probiotics, and lifestyle changes. Rome IV criteria provide "
                        "more current diagnostic standards and may be considered for confirmation. "
                        "Reassess if symptoms worsen or new concerning features develop. Patient "
                        "education about chronic nature and symptom management is important."
                    )
                }


def calculate_manning_criteria_ibs(pain_onset_frequent_bowel_movements: str, looser_stools_with_pain_onset: str,
                                  pain_relief_with_defecation: str, noticeable_abdominal_bloating: str,
                                  incomplete_evacuation_sensation: str, diarrhea_with_mucus: str,
                                  patient_age: int, weight_loss: str, blood_in_stools: str,
                                  anemia: str, fever: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ManningCriteriaIbsCalculator()
    return calculator.calculate(pain_onset_frequent_bowel_movements, looser_stools_with_pain_onset,
                               pain_relief_with_defecation, noticeable_abdominal_bloating,
                               incomplete_evacuation_sensation, diarrhea_with_mucus,
                               patient_age, weight_loss, blood_in_stools, anemia, fever)