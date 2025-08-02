"""
IMPROVE Bleeding Risk Score Calculator

Assesses bleeding risk at hospital admission for acutely ill medical patients,
particularly when considering anticoagulation therapy. The IMPROVE Bleeding Risk Score
helps identify patients at high risk for bleeding complications.

References (Vancouver style):
1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
   Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
   Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
   model of the International Medical Prevention Registry on Venous Thromboembolism 
   (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
   Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.
4. Stuck AK, Spirk D, Schaudt J, Kucher N. Risk assessment models for venous 
   thromboembolism in acutely ill medical patients. A systematic review. Thromb 
   Haemost. 2017 May 3;117(5):801-808. doi: 10.1160/TH16-08-0631.
"""

from typing import Dict, Any


class ImproveBleedingRiskScoreCalculator:
    """Calculator for IMPROVE Bleeding Risk Score"""
    
    def __init__(self):
        # IMPROVE Bleeding Risk Score weights
        self.scoring_weights = {
            "age_category": {
                "under_40": 0,
                "40_to_84": 1.5,
                "85_or_over": 3.5
            },
            "gender": {
                "female": 0,
                "male": 1
            },
            "renal_function": {
                "gfr_60_or_above": 0,
                "gfr_30_to_59": 1,
                "gfr_under_30": 2.5
            },
            "current_cancer": {
                "no": 0,
                "yes": 2
            },
            "rheumatic_disease": {
                "no": 0,
                "yes": 2
            },
            "central_venous_catheter": {
                "no": 0,
                "yes": 2
            },
            "icu_ccu_stay": {
                "no": 0,
                "yes": 2.5
            },
            "hepatic_failure": {
                "no": 0,
                "yes": 2.5
            },
            "platelet_count_category": {
                "50_or_above": 0,
                "under_50": 4
            },
            "bleeding_in_3_months": {
                "no": 0,
                "yes": 4
            },
            "active_gastroduodenal_ulcer": {
                "no": 0,
                "yes": 4.5
            }
        }
        
        # Risk threshold
        self.risk_threshold = 7.0
    
    def calculate(self, age_category: str, gender: str, renal_function: str,
                 current_cancer: str, rheumatic_disease: str, central_venous_catheter: str,
                 icu_ccu_stay: str, hepatic_failure: str, platelet_count_category: str,
                 bleeding_in_3_months: str, active_gastroduodenal_ulcer: str) -> Dict[str, Any]:
        """
        Calculates the IMPROVE Bleeding Risk Score
        
        Args:
            age_category (str): Patient age category
            gender (str): Patient gender
            renal_function (str): GFR category
            current_cancer (str): Active cancer within 6 months
            rheumatic_disease (str): Presence of rheumatic disease
            central_venous_catheter (str): Presence of central venous catheter
            icu_ccu_stay (str): Current ICU/CCU stay
            hepatic_failure (str): Hepatic failure (INR >1.5)
            platelet_count_category (str): Platelet count category
            bleeding_in_3_months (str): Recent bleeding history
            active_gastroduodenal_ulcer (str): Active peptic ulcer disease
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, gender, renal_function, current_cancer,
                            rheumatic_disease, central_venous_catheter, icu_ccu_stay,
                            hepatic_failure, platelet_count_category, bleeding_in_3_months,
                            active_gastroduodenal_ulcer)
        
        # Calculate total score
        score = self._calculate_total_score(
            age_category, gender, renal_function, current_cancer, rheumatic_disease,
            central_venous_catheter, icu_ccu_stay, hepatic_failure, platelet_count_category,
            bleeding_in_3_months, active_gastroduodenal_ulcer
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
    
    def _validate_inputs(self, age_category: str, gender: str, renal_function: str,
                        current_cancer: str, rheumatic_disease: str, central_venous_catheter: str,
                        icu_ccu_stay: str, hepatic_failure: str, platelet_count_category: str,
                        bleeding_in_3_months: str, active_gastroduodenal_ulcer: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "age_category": ["under_40", "40_to_84", "85_or_over"],
            "gender": ["female", "male"],
            "renal_function": ["gfr_60_or_above", "gfr_30_to_59", "gfr_under_30"],
            "current_cancer": ["yes", "no"],
            "rheumatic_disease": ["yes", "no"],
            "central_venous_catheter": ["yes", "no"],
            "icu_ccu_stay": ["yes", "no"],
            "hepatic_failure": ["yes", "no"],
            "platelet_count_category": ["50_or_above", "under_50"],
            "bleeding_in_3_months": ["yes", "no"],
            "active_gastroduodenal_ulcer": ["yes", "no"]
        }
        
        # Validate each parameter
        parameters = {
            "age_category": age_category,
            "gender": gender,
            "renal_function": renal_function,
            "current_cancer": current_cancer,
            "rheumatic_disease": rheumatic_disease,
            "central_venous_catheter": central_venous_catheter,
            "icu_ccu_stay": icu_ccu_stay,
            "hepatic_failure": hepatic_failure,
            "platelet_count_category": platelet_count_category,
            "bleeding_in_3_months": bleeding_in_3_months,
            "active_gastroduodenal_ulcer": active_gastroduodenal_ulcer
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, age_category: str, gender: str, renal_function: str,
                              current_cancer: str, rheumatic_disease: str, central_venous_catheter: str,
                              icu_ccu_stay: str, hepatic_failure: str, platelet_count_category: str,
                              bleeding_in_3_months: str, active_gastroduodenal_ulcer: str) -> float:
        """
        Calculates the total IMPROVE Bleeding Risk Score
        
        IMPROVE Bleeding Risk Scoring:
        - Age: <40 (0), 40-84 (1.5), ≥85 (3.5) points
        - Gender: Female (0), Male (1) point
        - Renal function: GFR ≥60 (0), 30-59 (1), <30 (2.5) points
        - Current cancer: 2 points
        - Rheumatic disease: 2 points
        - Central venous catheter: 2 points
        - ICU/CCU stay: 2.5 points
        - Hepatic failure: 2.5 points
        - Platelet <50k: 4 points
        - Recent bleeding: 4 points
        - Active GI ulcer: 4.5 points
        """
        
        total_score = 0.0
        
        # Add points for each risk factor
        total_score += self.scoring_weights["age_category"][age_category]
        total_score += self.scoring_weights["gender"][gender]
        total_score += self.scoring_weights["renal_function"][renal_function]
        total_score += self.scoring_weights["current_cancer"][current_cancer]
        total_score += self.scoring_weights["rheumatic_disease"][rheumatic_disease]
        total_score += self.scoring_weights["central_venous_catheter"][central_venous_catheter]
        total_score += self.scoring_weights["icu_ccu_stay"][icu_ccu_stay]
        total_score += self.scoring_weights["hepatic_failure"][hepatic_failure]
        total_score += self.scoring_weights["platelet_count_category"][platelet_count_category]
        total_score += self.scoring_weights["bleeding_in_3_months"][bleeding_in_3_months]
        total_score += self.scoring_weights["active_gastroduodenal_ulcer"][active_gastroduodenal_ulcer]
        
        return total_score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on IMPROVE Bleeding Risk Score
        
        Args:
            score (float): IMPROVE Bleeding Risk Score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.risk_threshold:
            return {
                "stage": "No Increased Risk",
                "description": f"Score {score} points (<7 points)",
                "interpretation": "No increased bleeding risk identified. Standard anticoagulation protocols may be followed as clinically indicated. Routine monitoring for bleeding complications recommended."
            }
        else:  # High risk
            return {
                "stage": "Increased Risk",
                "description": f"Score {score} points (≥7 points)",
                "interpretation": "Increased bleeding risk identified. Major bleeding rate 3.9% vs 1.2% in low-risk patients. Consider avoiding anticoagulants if possible, using non-pharmacologic thromboprophylaxis interventions, or implementing enhanced monitoring for bleeding events if anticoagulation is necessary. Careful risk-benefit assessment required."
            }


def calculate_improve_bleeding_risk_score(age_category: str, gender: str, renal_function: str,
                                        current_cancer: str, rheumatic_disease: str,
                                        central_venous_catheter: str, icu_ccu_stay: str,
                                        hepatic_failure: str, platelet_count_category: str,
                                        bleeding_in_3_months: str,
                                        active_gastroduodenal_ulcer: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ImproveBleedingRiskScoreCalculator()
    return calculator.calculate(
        age_category, gender, renal_function, current_cancer, rheumatic_disease,
        central_venous_catheter, icu_ccu_stay, hepatic_failure, platelet_count_category,
        bleeding_in_3_months, active_gastroduodenal_ulcer
    )