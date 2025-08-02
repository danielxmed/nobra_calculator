"""
Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM) Calculator

Predicts survival in patients with myelofibrosis secondary to polycythemia vera (PV) 
and essential thrombocythemia (ET) using clinical and molecular parameters.

References:
1. Passamonti F, Giorgino T, Mora B, Guglielmelli P, Rumi E, Maffioli M, et al. 
   A clinical-molecular prognostic model to predict survival in patients with post 
   polycythemia vera and post essential thrombocythemia myelofibrosis. Leukemia. 
   2017;31(12):2726-2731. doi: 10.1038/leu.2017.169.
2. Guglielmelli P, Rotunno G, Pacilli A, Rumi E, Rosti V, Delaini F, et al. 
   Prognostic impact of bone marrow fibrosis in primary myelofibrosis. A study of 
   the AGIMM group on 490 patients. Am J Hematol. 2016;91(9):918-22. 
   doi: 10.1002/ajh.24423.
"""

from typing import Dict, Any
import math


class MysecPmCalculator:
    """Calculator for MYSEC-PM Score"""
    
    def __init__(self):
        # Scoring criteria based on published literature
        self.AGE_COEFFICIENT = 0.15  # points per year
        self.HEMOGLOBIN_THRESHOLD = 11.0  # g/dL
        self.BLAST_THRESHOLD = 3.0  # %
        self.PLATELET_THRESHOLD = 150.0  # ×10⁹/L
        
        # Risk category thresholds
        self.LOW_RISK_THRESHOLD = 11.0
        self.INTERMEDIATE_1_THRESHOLD = 14.0
        self.INTERMEDIATE_2_THRESHOLD = 16.0
    
    def calculate(self, age_years: int, hemoglobin: float, circulating_blasts: float,
                 platelet_count: float, constitutional_symptoms: str, 
                 calr_mutation_status: str) -> Dict[str, Any]:
        """
        Calculates the MYSEC-PM Score for secondary myelofibrosis prognosis
        
        Args:
            age_years (int): Patient age in years
            hemoglobin (float): Hemoglobin level in g/dL
            circulating_blasts (float): Percentage of circulating blasts
            platelet_count (float): Platelet count in ×10⁹/L
            constitutional_symptoms (str): Presence of constitutional symptoms ("yes" or "no")
            calr_mutation_status (str): CALR mutation status ("mutated", "unmutated", or "unknown")
            
        Returns:
            Dict with the MYSEC-PM score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_years, hemoglobin, circulating_blasts, platelet_count,
                            constitutional_symptoms, calr_mutation_status)
        
        # Calculate component scores
        score_components = self._calculate_component_scores(
            age_years, hemoglobin, circulating_blasts, platelet_count,
            constitutional_symptoms, calr_mutation_status
        )
        
        # Calculate total score
        total_score = sum(score_components.values())
        
        # Round to 2 decimal places
        total_score = round(total_score, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_years: int, hemoglobin: float, circulating_blasts: float,
                        platelet_count: float, constitutional_symptoms: str, calr_mutation_status: str):
        """Validates input parameters"""
        
        if not isinstance(age_years, int) or age_years < 18 or age_years > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 3.0 or hemoglobin > 20.0:
            raise ValueError("Hemoglobin must be between 3.0 and 20.0 g/dL")
        
        if not isinstance(circulating_blasts, (int, float)) or circulating_blasts < 0.0 or circulating_blasts > 100.0:
            raise ValueError("Circulating blasts must be between 0.0 and 100.0%")
        
        if not isinstance(platelet_count, (int, float)) or platelet_count < 1.0 or platelet_count > 2000.0:
            raise ValueError("Platelet count must be between 1.0 and 2000.0 ×10⁹/L")
        
        if constitutional_symptoms not in ["yes", "no"]:
            raise ValueError("Constitutional symptoms must be 'yes' or 'no'")
        
        if calr_mutation_status not in ["mutated", "unmutated", "unknown"]:
            raise ValueError("CALR mutation status must be 'mutated', 'unmutated', or 'unknown'")
    
    def _calculate_component_scores(self, age_years: int, hemoglobin: float, 
                                  circulating_blasts: float, platelet_count: float,
                                  constitutional_symptoms: str, calr_mutation_status: str) -> Dict[str, float]:
        """Calculates individual component scores"""
        
        scores = {}
        
        # Age score (continuous variable)
        scores["age"] = age_years * self.AGE_COEFFICIENT
        
        # Hemoglobin score
        scores["hemoglobin"] = 2.0 if hemoglobin < self.HEMOGLOBIN_THRESHOLD else 0.0
        
        # Circulating blasts score
        scores["blasts"] = 2.0 if circulating_blasts >= self.BLAST_THRESHOLD else 0.0
        
        # Platelet count score
        scores["platelets"] = 1.0 if platelet_count < self.PLATELET_THRESHOLD else 0.0
        
        # Constitutional symptoms score
        scores["symptoms"] = 1.0 if constitutional_symptoms == "yes" else 0.0
        
        # CALR mutation status score
        scores["calr"] = 2.0 if calr_mutation_status == "unmutated" else 0.0
        
        return scores
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on MYSEC-PM score
        
        Args:
            score (float): Calculated MYSEC-PM score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low risk secondary myelofibrosis",
                "interpretation": f"LOW RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: {score}): Excellent prognosis "
                                "with median survival not reached. MANAGEMENT: Regular monitoring with routine clinical "
                                "assessments every 3-6 months. Supportive care approach with symptom management as needed. "
                                "TREATMENT: Consider observation or symptom-directed therapy. JAK inhibitors only if "
                                "symptomatic splenomegaly or constitutional symptoms significantly impact quality of life. "
                                "TRANSPLANT: Allogeneic stem cell transplantation not indicated due to excellent prognosis. "
                                "MONITORING: Regular complete blood counts, assessment for disease progression, and "
                                "quality of life evaluation. Excellent long-term survival expected."
            }
        elif score < self.INTERMEDIATE_1_THRESHOLD:
            return {
                "stage": "Intermediate-1 Risk",
                "description": "Intermediate-1 risk secondary myelofibrosis",
                "interpretation": f"INTERMEDIATE-1 RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: {score}): Good prognosis "
                                "with median survival 9.3 years. MANAGEMENT: Regular monitoring every 2-4 months with "
                                "symptom assessment and laboratory evaluation. TREATMENT: Consider JAK inhibitor therapy "
                                "for symptomatic disease (splenomegaly, constitutional symptoms, anemia). Supportive care "
                                "for disease-related complications. TRANSPLANT: Allogeneic transplantation generally not "
                                "recommended unless disease progression or development of high-risk features. "
                                "MONITORING: Watch for signs of progression and assess treatment response. Good long-term "
                                "survival with appropriate management."
            }
        elif score < self.INTERMEDIATE_2_THRESHOLD:
            return {
                "stage": "Intermediate-2 Risk",
                "description": "Intermediate-2 risk secondary myelofibrosis",
                "interpretation": f"INTERMEDIATE-2 RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: {score}): Intermediate "
                                "prognosis with median survival 4.4 years. MANAGEMENT: Close monitoring every 1-3 months "
                                "with comprehensive assessment. TREATMENT: JAK inhibitor therapy recommended for symptom "
                                "control and potential survival benefit. Aggressive supportive care for cytopenias and "
                                "complications. TRANSPLANT: Consider allogeneic stem cell transplantation evaluation if "
                                "appropriate candidate (age, performance status, comorbidities). Timing of transplant "
                                "referral is critical for optimal outcomes. MONITORING: Regular assessment for disease "
                                "progression and transplant eligibility."
            }
        else:  # score >= 16
            return {
                "stage": "High Risk",
                "description": "High risk secondary myelofibrosis",
                "interpretation": f"HIGH RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: {score}): Poor prognosis with "
                                "median survival 2.0 years. MANAGEMENT: Intensive monitoring and aggressive treatment "
                                "approach. TREATMENT: JAK inhibitor therapy for symptom palliation and potential survival "
                                "benefit. Aggressive supportive care including transfusion support, infection prophylaxis, "
                                "and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell "
                                "transplantation evaluation and referral to transplant center if appropriate candidate. "
                                "Consider experimental therapies and clinical trial participation. PROGNOSIS: Poor survival "
                                "outcomes requiring intensive multidisciplinary care and urgent transplant consideration."
            }


def calculate_mysec_pm(age_years: int, hemoglobin: float, circulating_blasts: float,
                      platelet_count: float, constitutional_symptoms: str, 
                      calr_mutation_status: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MysecPmCalculator()
    return calculator.calculate(age_years, hemoglobin, circulating_blasts, platelet_count,
                               constitutional_symptoms, calr_mutation_status)