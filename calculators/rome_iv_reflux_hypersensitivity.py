"""
Rome IV Diagnostic Criteria for Reflux Hypersensitivity Calculator

Applies the official Rome IV diagnostic criteria for reflux hypersensitivity, a functional 
esophageal disorder characterized by retrosternal symptoms triggered by normal amounts of 
gastroesophageal reflux. This condition is distinguished from GERD by normal acid exposure 
time but positive symptom-reflux association on ambulatory pH monitoring.

References:
1. Aziz Q, Fass R, Gyawali CP, Miwa H, Pandolfino JE, Zerbib F. Esophageal disorders. 
   Gastroenterology. 2016 May;150(6):1368-1379. doi: 10.1053/j.gastro.2016.02.012.
2. Rome Foundation. Rome IV Diagnostic Criteria for Functional Gastrointestinal Disorders. 
   4th ed. Raleigh, NC: Rome Foundation; 2016.
3. Patel A, Gyawali CP. Reflux hypersensitivity: Current concepts and future directions. 
   Current Gastroenterology Reports. 2015 May;17(5):20. doi: 10.1007/s11894-015-0441-x.
"""

from typing import Dict, Any


class RomeIvRefluxHypersensitivityCalculator:
    """Calculator for Rome IV Diagnostic Criteria for Reflux Hypersensitivity"""
    
    def __init__(self):
        # All criteria must be met for positive diagnosis
        self.REQUIRED_CRITERIA_COUNT = 6
    
    def calculate(self, retrosternal_symptoms: str, 
                 normal_endoscopy: str,
                 absence_eosinophilic_esophagitis: str,
                 absence_major_motor_disorders: str,
                 normal_acid_exposure_with_symptom_association: str,
                 exclusion_alarm_symptoms: str) -> Dict[str, Any]:
        """
        Applies Rome IV diagnostic criteria for reflux hypersensitivity
        
        Args:
            retrosternal_symptoms (str): Retrosternal symptoms including heartburn and 
                chest pain for ≥3 months with onset ≥6 months ago, ≥2x/week ("yes"/"no")
            normal_endoscopy (str): Normal endoscopy findings without erosive esophagitis ("yes"/"no")
            absence_eosinophilic_esophagitis (str): Absence of evidence of eosinophilic 
                esophagitis on endoscopy and biopsy ("yes"/"no")
            absence_major_motor_disorders (str): Absence of major esophageal motor disorders 
                on manometry ("yes"/"no")
            normal_acid_exposure_with_symptom_association (str): Evidence of symptom triggering 
                by reflux events despite normal acid exposure on pH monitoring ("yes"/"no")
            exclusion_alarm_symptoms (str): Exclusion of alarm symptoms requiring further 
                evaluation ("yes"/"no")
            
        Returns:
            Dict with Rome IV reflux hypersensitivity diagnostic assessment
        """
        
        # Validate inputs
        self._validate_inputs(retrosternal_symptoms, normal_endoscopy,
                             absence_eosinophilic_esophagitis, absence_major_motor_disorders,
                             normal_acid_exposure_with_symptom_association, exclusion_alarm_symptoms)
        
        # Count criteria met
        criteria_met = self._count_criteria_met(retrosternal_symptoms, normal_endoscopy,
                                               absence_eosinophilic_esophagitis, absence_major_motor_disorders,
                                               normal_acid_exposure_with_symptom_association, exclusion_alarm_symptoms)
        
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
    
    def _validate_inputs(self, retrosternal_symptoms: str, normal_endoscopy: str,
                        absence_eosinophilic_esophagitis: str, absence_major_motor_disorders: str,
                        normal_acid_exposure_with_symptom_association: str, exclusion_alarm_symptoms: str):
        """Validates input parameters"""
        
        # List of all parameters with their names for validation
        parameters = [
            (retrosternal_symptoms, "retrosternal_symptoms"),
            (normal_endoscopy, "normal_endoscopy"),
            (absence_eosinophilic_esophagitis, "absence_eosinophilic_esophagitis"),
            (absence_major_motor_disorders, "absence_major_motor_disorders"),
            (normal_acid_exposure_with_symptom_association, "normal_acid_exposure_with_symptom_association"),
            (exclusion_alarm_symptoms, "exclusion_alarm_symptoms")
        ]
        
        for param, name in parameters:
            if not isinstance(param, str) or param.lower() not in ["yes", "no"]:
                raise ValueError(f"{name} must be either 'yes' or 'no'")
    
    def _count_criteria_met(self, retrosternal_symptoms: str, normal_endoscopy: str,
                           absence_eosinophilic_esophagitis: str, absence_major_motor_disorders: str,
                           normal_acid_exposure_with_symptom_association: str, exclusion_alarm_symptoms: str) -> int:
        """Counts how many Rome IV criteria are met"""
        
        criteria_met = 0
        
        # Criterion 1: Retrosternal symptoms including heartburn and chest pain
        if retrosternal_symptoms.lower() == "yes":
            criteria_met += 1
        
        # Criterion 2: Normal endoscopy findings
        if normal_endoscopy.lower() == "yes":
            criteria_met += 1
        
        # Criterion 3: Absence of eosinophilic esophagitis
        if absence_eosinophilic_esophagitis.lower() == "yes":
            criteria_met += 1
        
        # Criterion 4: Absence of major esophageal motor disorders
        if absence_major_motor_disorders.lower() == "yes":
            criteria_met += 1
        
        # Criterion 5: Normal acid exposure with positive symptom-reflux association
        if normal_acid_exposure_with_symptom_association.lower() == "yes":
            criteria_met += 1
        
        # Criterion 6: Exclusion of alarm symptoms
        if exclusion_alarm_symptoms.lower() == "yes":
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
                "interpretation": "Patient fulfills Rome IV diagnostic criteria for reflux hypersensitivity. Diagnosis is established when all criteria are met including retrosternal symptoms for at least 3 months (with onset ≥6 months ago, occurring ≥2 times per week), normal endoscopy, exclusion of eosinophilic esophagitis and major motor disorders, and demonstration of normal acid exposure time (<4%) with positive symptom-reflux association (SAP >95% or SI >50%) on ambulatory pH monitoring. Treatment options include acid suppression therapy (despite normal acid exposure), visceral pain modulators such as tricyclic antidepressants or gabapentinoids, psychological interventions including cognitive behavioral therapy, and lifestyle modifications. Consider dietary modifications similar to GERD management and stress reduction techniques."
            }
        else:
            return {
                "stage": "Criteria Not Met",
                "description": "Does not meet Rome IV criteria",
                "interpretation": f"Patient does not fulfill Rome IV diagnostic criteria for reflux hypersensitivity ({criteria_met}/{self.REQUIRED_CRITERIA_COUNT} criteria met). One or more essential criteria are not satisfied. Consider alternative diagnoses including GERD with abnormal acid exposure time (≥4%), functional heartburn with negative symptom-reflux association on pH monitoring, eosinophilic esophagitis with characteristic endoscopic and histologic findings, or major esophageal motor disorders such as achalasia, EGJ outflow obstruction, diffuse esophageal spasm, jackhammer esophagus, or absent peristalsis. Complete appropriate investigations including upper endoscopy with esophageal biopsies, esophageal manometry, and ambulatory pH or pH-impedance monitoring as clinically indicated. Evaluate for alarm symptoms requiring urgent attention."
            }


def calculate_rome_iv_reflux_hypersensitivity(retrosternal_symptoms: str,
                                             normal_endoscopy: str,
                                             absence_eosinophilic_esophagitis: str,
                                             absence_major_motor_disorders: str,
                                             normal_acid_exposure_with_symptom_association: str,
                                             exclusion_alarm_symptoms: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = RomeIvRefluxHypersensitivityCalculator()
    return calculator.calculate(retrosternal_symptoms, normal_endoscopy,
                               absence_eosinophilic_esophagitis, absence_major_motor_disorders,
                               normal_acid_exposure_with_symptom_association, exclusion_alarm_symptoms)