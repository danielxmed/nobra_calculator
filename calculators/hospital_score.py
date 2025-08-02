"""
HOSPITAL Score for Readmissions Calculator

Predicts potentially avoidable 30-day hospital readmissions in medical patients.

References:
- Donzé J, et al. JAMA Intern Med. 2013;173(8):632-8.
- Donzé JD, et al. JAMA Intern Med. 2016;176(4):496-502.
"""

from typing import Dict, Any


class HospitalScoreCalculator:
    """Calculator for HOSPITAL Score for Readmissions"""
    
    def __init__(self):
        # Hemoglobin scoring
        self.hemoglobin_points = {
            "gte_12": 0,  # ≥12 g/dL
            "lt_12": 1    # <12 g/dL
        }
        
        # Oncology service discharge scoring
        self.oncology_points = {
            "no": 0,
            "yes": 2
        }
        
        # Sodium scoring
        self.sodium_points = {
            "gte_135": 0,  # ≥135 mEq/L
            "lt_135": 1    # <135 mEq/L
        }
        
        # Procedure scoring
        self.procedure_points = {
            "no": 0,
            "yes": 1
        }
        
        # Admission type scoring
        self.admission_type_points = {
            "elective": 0,
            "urgent_emergent": 1
        }
        
        # Previous admissions scoring
        self.previous_admissions_points = {
            "0_to_1": 0,
            "2_to_5": 2,
            "over_5": 5
        }
        
        # Length of stay scoring
        self.length_of_stay_points = {
            "lt_5_days": 0,    # <5 days
            "gte_5_days": 2    # ≥5 days
        }
    
    def calculate(self, hemoglobin: str, oncology_discharge: str, sodium: str,
                  procedure: str, admission_type: str, previous_admissions: str,
                  length_of_stay: str) -> Dict[str, Any]:
        """
        Calculates the HOSPITAL score
        
        Args:
            hemoglobin (str): Hemoglobin level category
            oncology_discharge (str): Discharged from oncology service
            sodium (str): Sodium level category
            procedure (str): ICD-9 coded procedure during stay
            admission_type (str): Type of admission
            previous_admissions (str): Number of admissions in previous year
            length_of_stay (str): Length of current stay
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hemoglobin, oncology_discharge, sodium, procedure,
                            admission_type, previous_admissions, length_of_stay)
        
        # Calculate score
        score = (self.hemoglobin_points[hemoglobin] +
                self.oncology_points[oncology_discharge] +
                self.sodium_points[sodium] +
                self.procedure_points[procedure] +
                self.admission_type_points[admission_type] +
                self.previous_admissions_points[previous_admissions] +
                self.length_of_stay_points[length_of_stay])
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hemoglobin: str, oncology_discharge: str, sodium: str,
                        procedure: str, admission_type: str, previous_admissions: str,
                        length_of_stay: str):
        """Validates input parameters"""
        
        if hemoglobin not in self.hemoglobin_points:
            raise ValueError(f"Invalid hemoglobin: {hemoglobin}")
        
        if oncology_discharge not in self.oncology_points:
            raise ValueError(f"Invalid oncology_discharge: {oncology_discharge}")
        
        if sodium not in self.sodium_points:
            raise ValueError(f"Invalid sodium: {sodium}")
        
        if procedure not in self.procedure_points:
            raise ValueError(f"Invalid procedure: {procedure}")
        
        if admission_type not in self.admission_type_points:
            raise ValueError(f"Invalid admission_type: {admission_type}")
        
        if previous_admissions not in self.previous_admissions_points:
            raise ValueError(f"Invalid previous_admissions: {previous_admissions}")
        
        if length_of_stay not in self.length_of_stay_points:
            raise ValueError(f"Invalid length_of_stay: {length_of_stay}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HOSPITAL score
        
        Args:
            score (int): Calculated HOSPITAL score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Score 0-4",
                "interpretation": "Low risk of potentially avoidable 30-day readmission (5.8%). "
                                "Standard discharge planning and follow-up may be sufficient."
            }
        elif score <= 6:
            return {
                "stage": "Intermediate Risk",
                "description": "Score 5-6",
                "interpretation": "Intermediate risk of potentially avoidable 30-day readmission (12.0%). "
                                "Consider enhanced discharge planning and closer outpatient follow-up."
            }
        else:  # score >= 7
            return {
                "stage": "High Risk",
                "description": "Score ≥7",
                "interpretation": "High risk of potentially avoidable 30-day readmission (22.8%). "
                                "Intensive transitional care interventions recommended, including "
                                "early follow-up, medication reconciliation, and care coordination."
            }


def calculate_hospital_score(hemoglobin: str, oncology_discharge: str, sodium: str,
                           procedure: str, admission_type: str, previous_admissions: str,
                           length_of_stay: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HospitalScoreCalculator()
    return calculator.calculate(hemoglobin, oncology_discharge, sodium, procedure,
                              admission_type, previous_admissions, length_of_stay)