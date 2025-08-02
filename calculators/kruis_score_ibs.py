"""
Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS) Calculator

Clinical scoring system to differentiate IBS from organic gastrointestinal disease 
using weighted symptoms and laboratory parameters. Developed by Kruis et al. (1984) 
as one of the first validated scoring systems for IBS diagnosis.

References:
1. Kruis W, Thieme C, Weinzierl M, Schüssler P, Holl J, Paulus W. A diagnostic score 
   for the irritable bowel syndrome. Its value in the exclusion of organic disease. 
   Gastroenterology. 1984 Jul;87(1):1-7.
2. Frigerio G, Beretta A, Orsenigo G, Tadeo G, Imperiali G, Minoli G. Irritable bowel 
   syndrome. Still a diagnosis of exclusion? Dig Dis Sci. 1992 Jan;37(1):164-7.
"""

from typing import Dict, Any


class KruisScoreIbsCalculator:
    """Calculator for Kruis Score for IBS Diagnosis"""
    
    def __init__(self):
        """Initialize scoring parameters based on original Kruis criteria"""
        # Positive symptom scores
        self.symptom_scores = {
            "symptoms_present": 34,           # Abdominal pain, flatulence, or bowel irregularity
            "duration_over_2_years": 16,      # Symptom duration > 2 years
            "pain_description": 23,           # Pain described as burning, cutting, very strong
            "alternating_bowel_habits": 14    # Alternating constipation and diarrhea
        }
        
        # Negative red flag scores
        self.red_flag_scores = {
            "abnormal_physical_findings": -47,  # Abnormal physical examination
            "esr_over_10": -13,                # ESR > 10 mm/hr
            "wbc_over_10000": -50,             # WBC > 10,000/μL
            "low_hemoglobin": -98,             # Hemoglobin low (F<12, M<14 g/dL)
            "history_blood_in_stool": -98      # History of blood in stool
        }
        
        # Diagnostic threshold
        self.diagnostic_threshold = 44
    
    def calculate(self, symptoms_present: str, duration_over_2_years: str,
                 pain_description: str, alternating_bowel_habits: str,
                 abnormal_physical_findings: str, esr_over_10: str,
                 wbc_over_10000: str, low_hemoglobin: str,
                 history_blood_in_stool: str) -> Dict[str, Any]:
        """
        Calculates Kruis Score for IBS diagnosis
        
        Args:
            symptoms_present (str): Abdominal pain, flatulence, or bowel irregularity ("yes" or "no")
            duration_over_2_years (str): Symptom duration >2 years ("yes" or "no")
            pain_description (str): Severe pain description ("yes" or "no")
            alternating_bowel_habits (str): Alternating constipation/diarrhea ("yes" or "no")
            abnormal_physical_findings (str): Abnormal exam findings ("yes" or "no")
            esr_over_10 (str): ESR >10 mm/hr ("yes" or "no")
            wbc_over_10000 (str): WBC >10,000/μL ("yes" or "no")
            low_hemoglobin (str): Low hemoglobin ("yes" or "no")
            history_blood_in_stool (str): History of blood in stool ("yes" or "no")
            
        Returns:
            Dict with score calculation and IBS diagnosis assessment
        """
        
        # Validate inputs
        self._validate_inputs(symptoms_present, duration_over_2_years, pain_description,
                            alternating_bowel_habits, abnormal_physical_findings,
                            esr_over_10, wbc_over_10000, low_hemoglobin, history_blood_in_stool)
        
        # Calculate score components
        symptom_score = self._calculate_symptom_score(
            symptoms_present, duration_over_2_years, pain_description, alternating_bowel_habits
        )
        
        red_flag_score = self._calculate_red_flag_score(
            abnormal_physical_findings, esr_over_10, wbc_over_10000, 
            low_hemoglobin, history_blood_in_stool
        )
        
        total_score = symptom_score + red_flag_score
        
        # Determine diagnosis
        diagnosis_result = self._get_diagnosis(total_score)
        
        # Check for red flags
        red_flags_present = self._check_red_flags(
            abnormal_physical_findings, esr_over_10, wbc_over_10000,
            low_hemoglobin, history_blood_in_stool
        )
        
        # Create detailed result
        result = {
            "total_score": total_score,
            "symptom_score": symptom_score,
            "red_flag_score": red_flag_score,
            "individual_scores": {
                "symptoms_present": self.symptom_scores["symptoms_present"] if symptoms_present == "yes" else 0,
                "duration_over_2_years": self.symptom_scores["duration_over_2_years"] if duration_over_2_years == "yes" else 0,
                "pain_description": self.symptom_scores["pain_description"] if pain_description == "yes" else 0,
                "alternating_bowel_habits": self.symptom_scores["alternating_bowel_habits"] if alternating_bowel_habits == "yes" else 0,
                "abnormal_physical_findings": self.red_flag_scores["abnormal_physical_findings"] if abnormal_physical_findings == "yes" else 0,
                "esr_over_10": self.red_flag_scores["esr_over_10"] if esr_over_10 == "yes" else 0,
                "wbc_over_10000": self.red_flag_scores["wbc_over_10000"] if wbc_over_10000 == "yes" else 0,
                "low_hemoglobin": self.red_flag_scores["low_hemoglobin"] if low_hemoglobin == "yes" else 0,
                "history_blood_in_stool": self.red_flag_scores["history_blood_in_stool"] if history_blood_in_stool == "yes" else 0
            },
            "red_flags_present": red_flags_present,
            "diagnostic_threshold": self.diagnostic_threshold,
            "meets_threshold": total_score >= self.diagnostic_threshold
        }
        
        # Generate interpretation
        interpretation = self._generate_interpretation(total_score, red_flags_present, diagnosis_result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation,
            "stage": diagnosis_result["stage"],
            "stage_description": diagnosis_result["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        parameter_names = [
            "symptoms_present", "duration_over_2_years", "pain_description",
            "alternating_bowel_habits", "abnormal_physical_findings", 
            "esr_over_10", "wbc_over_10000", "low_hemoglobin", "history_blood_in_stool"
        ]
        
        for i, value in enumerate(args):
            if value not in valid_options:
                raise ValueError(f"{parameter_names[i]} must be 'yes' or 'no'")
    
    def _calculate_symptom_score(self, symptoms_present: str, duration_over_2_years: str,
                                pain_description: str, alternating_bowel_habits: str) -> int:
        """Calculates positive symptom score"""
        
        score = 0
        
        if symptoms_present == "yes":
            score += self.symptom_scores["symptoms_present"]
        if duration_over_2_years == "yes":
            score += self.symptom_scores["duration_over_2_years"]
        if pain_description == "yes":
            score += self.symptom_scores["pain_description"]
        if alternating_bowel_habits == "yes":
            score += self.symptom_scores["alternating_bowel_habits"]
            
        return score
    
    def _calculate_red_flag_score(self, abnormal_physical_findings: str, esr_over_10: str,
                                 wbc_over_10000: str, low_hemoglobin: str,
                                 history_blood_in_stool: str) -> int:
        """Calculates negative red flag score"""
        
        score = 0
        
        if abnormal_physical_findings == "yes":
            score += self.red_flag_scores["abnormal_physical_findings"]
        if esr_over_10 == "yes":
            score += self.red_flag_scores["esr_over_10"]
        if wbc_over_10000 == "yes":
            score += self.red_flag_scores["wbc_over_10000"]
        if low_hemoglobin == "yes":
            score += self.red_flag_scores["low_hemoglobin"]
        if history_blood_in_stool == "yes":
            score += self.red_flag_scores["history_blood_in_stool"]
            
        return score
    
    def _check_red_flags(self, abnormal_physical_findings: str, esr_over_10: str,
                        wbc_over_10000: str, low_hemoglobin: str,
                        history_blood_in_stool: str) -> list:
        """Identifies which red flags are present"""
        
        red_flags = []
        
        if abnormal_physical_findings == "yes":
            red_flags.append("abnormal_physical_findings")
        if esr_over_10 == "yes":
            red_flags.append("elevated_esr")
        if wbc_over_10000 == "yes":
            red_flags.append("elevated_wbc")
        if low_hemoglobin == "yes":
            red_flags.append("anemia")
        if history_blood_in_stool == "yes":
            red_flags.append("blood_in_stool")
            
        return red_flags
    
    def _get_diagnosis(self, total_score: int) -> Dict[str, str]:
        """
        Determines diagnosis based on total score
        
        Args:
            total_score (int): Calculated Kruis score
            
        Returns:
            Dict with stage and description
        """
        
        if total_score >= self.diagnostic_threshold:
            return {
                "stage": "Positive for IBS",
                "description": f"Score ≥ {self.diagnostic_threshold} points"
            }
        else:
            return {
                "stage": "Negative for IBS",
                "description": f"Score < {self.diagnostic_threshold} points"
            }
    
    def _generate_interpretation(self, total_score: int, red_flags_present: list,
                               diagnosis_result: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            total_score (int): Calculated score
            red_flags_present (list): List of present red flags
            diagnosis_result (Dict): Diagnosis result
            
        Returns:
            str: Detailed clinical interpretation with recommendations
        """
        
        # Base interpretation
        if total_score >= self.diagnostic_threshold:
            interpretation = (
                f"Score of {total_score} points indicates IBS diagnosis is likely. "
                f"Patient meets Kruis criteria threshold (≥{self.diagnostic_threshold} points) "
                f"for irritable bowel syndrome. "
            )
        else:
            interpretation = (
                f"Score of {total_score} points suggests IBS diagnosis is unlikely. "
                f"Patient does not meet Kruis criteria threshold (≥{self.diagnostic_threshold} points). "
                f"Consider further evaluation for organic gastrointestinal disease. "
            )
        
        # Red flag assessment
        if red_flags_present:
            red_flag_descriptions = {
                "abnormal_physical_findings": "abnormal physical examination findings",
                "elevated_esr": "elevated ESR (>10 mm/hr)",
                "elevated_wbc": "elevated WBC count (>10,000/μL)",
                "anemia": "anemia (low hemoglobin)",
                "blood_in_stool": "history of blood in stool"
            }
            
            flag_list = [red_flag_descriptions.get(flag, flag) for flag in red_flags_present]
            interpretation += (
                f"IMPORTANT: Red flags present ({', '.join(flag_list)}). "
                f"Organic pathology must be excluded through appropriate investigation "
                f"before diagnosing IBS. Consider colonoscopy, CT scan, or other imaging "
                f"as clinically indicated. "
            )
        else:
            interpretation += (
                f"No red flags identified, which supports the diagnostic assessment. "
            )
        
        # Clinical guidance
        if total_score >= self.diagnostic_threshold and not red_flags_present:
            interpretation += (
                f"With positive Kruis criteria and absence of red flags, IBS diagnosis "
                f"can be made with confidence (81% sensitivity, 91% specificity). "
                f"Consider initiating IBS management including dietary modifications, "
                f"symptom-targeted therapies, and patient education. "
            )
        elif total_score >= self.diagnostic_threshold and red_flags_present:
            interpretation += (
                f"Despite positive Kruis score, presence of red flags mandates "
                f"exclusion of organic disease before IBS diagnosis. "
            )
        else:
            interpretation += (
                f"Consider alternative diagnoses including inflammatory bowel disease, "
                f"celiac disease, microscopic colitis, or other organic conditions. "
                f"Clinical correlation and further investigation are recommended. "
            )
        
        # Historical context
        interpretation += (
            f"Note: The Kruis Score (1984) was one of the first validated IBS diagnostic "
            f"tools but has largely been superseded by Rome criteria in clinical practice."
        )
        
        return interpretation


def calculate_kruis_score_ibs(symptoms_present, duration_over_2_years, pain_description,
                             alternating_bowel_habits, abnormal_physical_findings,
                             esr_over_10, wbc_over_10000, low_hemoglobin,
                             history_blood_in_stool) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = KruisScoreIbsCalculator()
    return calculator.calculate(symptoms_present, duration_over_2_years, pain_description,
                              alternating_bowel_habits, abnormal_physical_findings,
                              esr_over_10, wbc_over_10000, low_hemoglobin,
                              history_blood_in_stool)