"""
IMPEDE-VTE Calculator

Predicts risk of venous thromboembolism (VTE) in patients with multiple myeloma
receiving treatment. The IMPEDE-VTE score helps identify patients at highest 
risk for VTE during multiple myeloma treatment.

References (Vancouver style):
1. Sanfilippo KM, Luo S, Wang TF, et al. Predicting venous thromboembolism in 
   multiple myeloma: development and validation of the IMPEDE VTE score. 
   Am J Hematol. 2019 Nov;94(11):1176-1184. doi: 10.1002/ajh.25603.
2. Sanfilippo KM, Luo S, Wang TF, et al. Validation of the IMPEDE VTE score 
   for prediction of venous thromboembolism in multiple myeloma: a retrospective 
   cohort study. Br J Haematol. 2021 Jun;193(5):1005-1015. doi: 10.1111/bjh.17396.
3. Li A, Wu Q, Luo S, et al. Derivation and validation of a risk assessment 
   model for immunomodulatory drug-associated thrombosis among patients with 
   multiple myeloma. J Natl Compr Canc Netw. 2019 Jul 1;17(7):840-847. 
   doi: 10.6004/jnccn.2018.7273.
4. National Comprehensive Cancer Network. Multiple Myeloma (Version 3.2023). 
   https://www.nccn.org/professionals/physician_gls/pdf/myeloma.pdf
"""

from typing import Dict, Any


class ImpedeVteCalculator:
    """Calculator for IMPEDE-VTE score"""
    
    def __init__(self):
        # IMPEDE-VTE scoring system
        self.scoring_weights = {
            "immunomodulatory_drug": {"yes": 4, "no": 0},
            "bmi_25_or_greater": {"yes": 1, "no": 0},
            "pelvic_hip_femur_fracture": {"yes": 4, "no": 0},
            "erythropoiesis_stimulating_agent": {"yes": 1, "no": 0},
            "doxorubicin_use": {"yes": 3, "no": 0},
            "dexamethasone_use": {"none": 0, "low_dose": 2, "high_dose": 4},
            "asian_pacific_islander": {"yes": -3, "no": 0},
            "history_of_vte": {"yes": 5, "no": 0},
            "tunneled_line_cvc": {"yes": 2, "no": 0},
            "therapeutic_anticoagulation": {"yes": -4, "no": 0},
            "prophylactic_anticoagulation": {"yes": -3, "no": 0}
        }
        
        # Risk thresholds
        self.risk_thresholds = {
            "low": {"min": -7, "max": 3},
            "intermediate": {"min": 4, "max": 7},
            "high": {"min": 8, "max": 19}
        }
    
    def calculate(self, immunomodulatory_drug: str, bmi_25_or_greater: str,
                 pelvic_hip_femur_fracture: str, erythropoiesis_stimulating_agent: str,
                 doxorubicin_use: str, dexamethasone_use: str,
                 asian_pacific_islander: str, history_of_vte: str,
                 tunneled_line_cvc: str, therapeutic_anticoagulation: str,
                 prophylactic_anticoagulation: str) -> Dict[str, Any]:
        """
        Calculates the IMPEDE-VTE score
        
        Args:
            immunomodulatory_drug (str): Use of IMiDs (lenalidomide, thalidomide, pomalidomide)
            bmi_25_or_greater (str): BMI ≥25 kg/m²
            pelvic_hip_femur_fracture (str): Pathologic fracture of pelvis, hip, or femur
            erythropoiesis_stimulating_agent (str): Use of ESAs
            doxorubicin_use (str): Use of doxorubicin
            dexamethasone_use (str): Dexamethasone dosing level
            asian_pacific_islander (str): Asian or Pacific Islander ethnicity
            history_of_vte (str): Previous VTE before MM diagnosis
            tunneled_line_cvc (str): Presence of tunneled CVC or central line
            therapeutic_anticoagulation (str): Current therapeutic anticoagulation
            prophylactic_anticoagulation (str): Current prophylactic anticoagulation
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(immunomodulatory_drug, bmi_25_or_greater,
                            pelvic_hip_femur_fracture, erythropoiesis_stimulating_agent,
                            doxorubicin_use, dexamethasone_use, asian_pacific_islander,
                            history_of_vte, tunneled_line_cvc, therapeutic_anticoagulation,
                            prophylactic_anticoagulation)
        
        # Calculate total score
        score = self._calculate_total_score(
            immunomodulatory_drug, bmi_25_or_greater, pelvic_hip_femur_fracture,
            erythropoiesis_stimulating_agent, doxorubicin_use, dexamethasone_use,
            asian_pacific_islander, history_of_vte, tunneled_line_cvc,
            therapeutic_anticoagulation, prophylactic_anticoagulation
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, immunomodulatory_drug: str, bmi_25_or_greater: str,
                        pelvic_hip_femur_fracture: str, erythropoiesis_stimulating_agent: str,
                        doxorubicin_use: str, dexamethasone_use: str,
                        asian_pacific_islander: str, history_of_vte: str,
                        tunneled_line_cvc: str, therapeutic_anticoagulation: str,
                        prophylactic_anticoagulation: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "immunomodulatory_drug": ["yes", "no"],
            "bmi_25_or_greater": ["yes", "no"],
            "pelvic_hip_femur_fracture": ["yes", "no"],
            "erythropoiesis_stimulating_agent": ["yes", "no"],
            "doxorubicin_use": ["yes", "no"],
            "dexamethasone_use": ["none", "low_dose", "high_dose"],
            "asian_pacific_islander": ["yes", "no"],
            "history_of_vte": ["yes", "no"],
            "tunneled_line_cvc": ["yes", "no"],
            "therapeutic_anticoagulation": ["yes", "no"],
            "prophylactic_anticoagulation": ["yes", "no"]
        }
        
        # Validate each parameter
        parameters = {
            "immunomodulatory_drug": immunomodulatory_drug,
            "bmi_25_or_greater": bmi_25_or_greater,
            "pelvic_hip_femur_fracture": pelvic_hip_femur_fracture,
            "erythropoiesis_stimulating_agent": erythropoiesis_stimulating_agent,
            "doxorubicin_use": doxorubicin_use,
            "dexamethasone_use": dexamethasone_use,
            "asian_pacific_islander": asian_pacific_islander,
            "history_of_vte": history_of_vte,
            "tunneled_line_cvc": tunneled_line_cvc,
            "therapeutic_anticoagulation": therapeutic_anticoagulation,
            "prophylactic_anticoagulation": prophylactic_anticoagulation
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, immunomodulatory_drug: str, bmi_25_or_greater: str,
                              pelvic_hip_femur_fracture: str, erythropoiesis_stimulating_agent: str,
                              doxorubicin_use: str, dexamethasone_use: str,
                              asian_pacific_islander: str, history_of_vte: str,
                              tunneled_line_cvc: str, therapeutic_anticoagulation: str,
                              prophylactic_anticoagulation: str) -> int:
        """
        Calculates the total IMPEDE-VTE score
        
        IMPEDE-VTE Scoring:
        - IMiD use: 4 points
        - BMI ≥25: 1 point
        - Pelvic/hip/femur fracture: 4 points
        - ESA use: 1 point
        - Doxorubicin: 3 points
        - Dexamethasone low dose: 2 points, high dose: 4 points
        - Asian/Pacific Islander: -3 points
        - VTE history: 5 points
        - Tunneled line/CVC: 2 points
        - Therapeutic anticoagulation: -4 points
        - Prophylactic anticoagulation: -3 points
        """
        
        total_score = 0
        
        # Add points for each risk factor
        total_score += self.scoring_weights["immunomodulatory_drug"][immunomodulatory_drug]
        total_score += self.scoring_weights["bmi_25_or_greater"][bmi_25_or_greater]
        total_score += self.scoring_weights["pelvic_hip_femur_fracture"][pelvic_hip_femur_fracture]
        total_score += self.scoring_weights["erythropoiesis_stimulating_agent"][erythropoiesis_stimulating_agent]
        total_score += self.scoring_weights["doxorubicin_use"][doxorubicin_use]
        total_score += self.scoring_weights["dexamethasone_use"][dexamethasone_use]
        total_score += self.scoring_weights["asian_pacific_islander"][asian_pacific_islander]
        total_score += self.scoring_weights["history_of_vte"][history_of_vte]
        total_score += self.scoring_weights["tunneled_line_cvc"][tunneled_line_cvc]
        total_score += self.scoring_weights["therapeutic_anticoagulation"][therapeutic_anticoagulation]
        total_score += self.scoring_weights["prophylactic_anticoagulation"][prophylactic_anticoagulation]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on IMPEDE-VTE score
        
        Args:
            score (int): IMPEDE-VTE score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.risk_thresholds["low"]["max"]:
            return {
                "stage": "Low Risk",
                "description": f"Score {score} points (≤3 points)",
                "interpretation": "Low VTE risk. 6-month cumulative VTE incidence 3.8-5.0%. Standard monitoring and general VTE prevention measures. Consider thromboprophylaxis only in presence of additional high-risk factors not captured by score."
            }
        elif score <= self.risk_thresholds["intermediate"]["max"]:
            return {
                "stage": "Intermediate Risk",
                "description": f"Score {score} points (4-7 points)",
                "interpretation": "Intermediate VTE risk. 6-month cumulative VTE incidence 8.6-12.6%. Consider thromboprophylaxis with aspirin or low molecular weight heparin based on individual patient factors, bleeding risk, and treatment regimen. Regular monitoring recommended."
            }
        else:  # High risk
            return {
                "stage": "High Risk",
                "description": f"Score {score} points (≥8 points)",
                "interpretation": "High VTE risk. 6-month cumulative VTE incidence 24.1-40.5%. Thromboprophylaxis strongly recommended unless contraindicated. Preferred agents include low molecular weight heparin or direct oral anticoagulants. Close monitoring for VTE symptoms essential."
            }


def calculate_impede_vte(immunomodulatory_drug: str, bmi_25_or_greater: str,
                        pelvic_hip_femur_fracture: str, erythropoiesis_stimulating_agent: str,
                        doxorubicin_use: str, dexamethasone_use: str,
                        asian_pacific_islander: str, history_of_vte: str,
                        tunneled_line_cvc: str, therapeutic_anticoagulation: str,
                        prophylactic_anticoagulation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImpedeVteCalculator()
    return calculator.calculate(
        immunomodulatory_drug, bmi_25_or_greater, pelvic_hip_femur_fracture,
        erythropoiesis_stimulating_agent, doxorubicin_use, dexamethasone_use,
        asian_pacific_islander, history_of_vte, tunneled_line_cvc,
        therapeutic_anticoagulation, prophylactic_anticoagulation
    )