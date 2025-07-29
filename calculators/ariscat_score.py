"""
ARISCAT Score Calculator

Predicts risk of postoperative pulmonary complications including respiratory failure, 
respiratory infection, pleural effusion, atelectasis, pneumothorax, bronchospasm, 
or aspiration pneumonitis after surgery.

References:
1. Canet J, Gallart L, Gomar C, Paluzie G, Vallès J, Castillo J, et al. Prediction of 
   postoperative pulmonary complications in a population-based surgical cohort. 
   Anesthesiology. 2010;113(6):1338-50.
2. Mazo V, Sabaté S, Canet J, Gallart L, de Abreu MG, Belda J, et al. Prospective 
   external validation of a predictive score for postoperative pulmonary complications. 
   Anesthesiology. 2014;121(2):219-31.
"""

from typing import Dict, Any


class AriscatScoreCalculator:
    """Calculator for ARISCAT Score for Postoperative Pulmonary Complications"""
    
    def __init__(self):
        # Age scoring
        self.AGE_SCORES = {
            "50_or_less": 0,
            "51_to_80": 3,
            "over_80": 16
        }
        
        # Preoperative SpO2 scoring
        self.SPO2_SCORES = {
            "96_or_higher": 0,
            "91_to_95": 8,
            "90_or_less": 24
        }
        
        # Respiratory infection last month scoring
        self.RESPIRATORY_INFECTION_SCORES = {
            "no": 0,
            "yes": 17
        }
        
        # Preoperative anemia scoring
        self.ANEMIA_SCORES = {
            "no": 0,
            "yes": 11
        }
        
        # Surgical incision scoring
        self.SURGICAL_INCISION_SCORES = {
            "peripheral": 0,
            "upper_abdominal": 15,
            "intrathoracic": 24
        }
        
        # Surgery duration scoring
        self.SURGERY_DURATION_SCORES = {
            "less_than_2": 0,
            "2_to_3": 16,
            "more_than_3": 23
        }
        
        # Emergency procedure scoring
        self.EMERGENCY_SCORES = {
            "no": 0,
            "yes": 8
        }
    
    def calculate(self, age: str, preoperative_spo2: str, respiratory_infection_last_month: str,
                  preoperative_anemia: str, surgical_incision: str, surgery_duration: str,
                  emergency_procedure: str) -> Dict[str, Any]:
        """
        Calculates ARISCAT Score for postoperative pulmonary complications
        
        Args:
            age (str): Patient age category (50_or_less, 51_to_80, over_80)
            preoperative_spo2 (str): Preoperative oxygen saturation (96_or_higher, 91_to_95, 90_or_less)
            respiratory_infection_last_month (str): Respiratory infection in last month (no, yes)
            preoperative_anemia (str): Preoperative anemia Hb ≤10 g/dL (no, yes)
            surgical_incision (str): Type of surgical incision (peripheral, upper_abdominal, intrathoracic)
            surgery_duration (str): Duration of surgery (less_than_2, 2_to_3, more_than_3)
            emergency_procedure (str): Emergency surgical procedure (no, yes)
            
        Returns:
            Dict with the ARISCAT score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, preoperative_spo2, respiratory_infection_last_month,
                             preoperative_anemia, surgical_incision, surgery_duration,
                             emergency_procedure)
        
        # Calculate score
        score = self._calculate_score(age, preoperative_spo2, respiratory_infection_last_month,
                                    preoperative_anemia, surgical_incision, surgery_duration,
                                    emergency_procedure)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, preoperative_spo2: str, respiratory_infection_last_month: str,
                        preoperative_anemia: str, surgical_incision: str, surgery_duration: str,
                        emergency_procedure: str):
        """Validates input parameters"""
        
        if age not in self.AGE_SCORES:
            raise ValueError(f"Invalid age category: {age}. Must be one of: {list(self.AGE_SCORES.keys())}")
        
        if preoperative_spo2 not in self.SPO2_SCORES:
            raise ValueError(f"Invalid preoperative SpO2: {preoperative_spo2}. Must be one of: {list(self.SPO2_SCORES.keys())}")
        
        if respiratory_infection_last_month not in self.RESPIRATORY_INFECTION_SCORES:
            raise ValueError(f"Invalid respiratory infection status: {respiratory_infection_last_month}. Must be one of: {list(self.RESPIRATORY_INFECTION_SCORES.keys())}")
        
        if preoperative_anemia not in self.ANEMIA_SCORES:
            raise ValueError(f"Invalid anemia status: {preoperative_anemia}. Must be one of: {list(self.ANEMIA_SCORES.keys())}")
        
        if surgical_incision not in self.SURGICAL_INCISION_SCORES:
            raise ValueError(f"Invalid surgical incision: {surgical_incision}. Must be one of: {list(self.SURGICAL_INCISION_SCORES.keys())}")
        
        if surgery_duration not in self.SURGERY_DURATION_SCORES:
            raise ValueError(f"Invalid surgery duration: {surgery_duration}. Must be one of: {list(self.SURGERY_DURATION_SCORES.keys())}")
        
        if emergency_procedure not in self.EMERGENCY_SCORES:
            raise ValueError(f"Invalid emergency procedure status: {emergency_procedure}. Must be one of: {list(self.EMERGENCY_SCORES.keys())}")
    
    def _calculate_score(self, age: str, preoperative_spo2: str, respiratory_infection_last_month: str,
                        preoperative_anemia: str, surgical_incision: str, surgery_duration: str,
                        emergency_procedure: str) -> int:
        """Calculates the ARISCAT score"""
        
        score = 0
        
        # Add points for each parameter
        score += self.AGE_SCORES[age]
        score += self.SPO2_SCORES[preoperative_spo2]
        score += self.RESPIRATORY_INFECTION_SCORES[respiratory_infection_last_month]
        score += self.ANEMIA_SCORES[preoperative_anemia]
        score += self.SURGICAL_INCISION_SCORES[surgical_incision]
        score += self.SURGERY_DURATION_SCORES[surgery_duration]
        score += self.EMERGENCY_SCORES[emergency_procedure]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the ARISCAT score
        
        Args:
            score (int): Calculated ARISCAT score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 25:
            return {
                "stage": "Low Risk",
                "description": "Low risk of postoperative pulmonary complications",
                "interpretation": "Patients in this category have a low probability of developing postoperative pulmonary complications. Standard perioperative care and monitoring are usually sufficient."
            }
        elif score <= 44:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk of postoperative pulmonary complications",
                "interpretation": "Patients in this category have an intermediate probability of developing postoperative pulmonary complications. Enhanced respiratory monitoring and preventive measures should be considered."
            }
        else:  # score >= 45
            return {
                "stage": "High Risk",
                "description": "High risk of postoperative pulmonary complications",
                "interpretation": "Patients in this category have a high probability of developing postoperative pulmonary complications. Intensive respiratory monitoring, prophylactic measures, and possibly ICU care should be strongly considered."
            }


def calculate_ariscat_score(age: str, preoperative_spo2: str, respiratory_infection_last_month: str,
                           preoperative_anemia: str, surgical_incision: str, surgery_duration: str,
                           emergency_procedure: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ariscat_score pattern
    """
    calculator = AriscatScoreCalculator()
    return calculator.calculate(age, preoperative_spo2, respiratory_infection_last_month,
                               preoperative_anemia, surgical_incision, surgery_duration,
                               emergency_procedure)
