"""
Infective Endocarditis (IE) Mortality Risk Score Calculator

Predicts 6-month mortality in patients with infective endocarditis using validated 
clinical parameters from the International Collaboration on Endocarditis (ICE) 
Prospective Cohort Study.

References (Vancouver style):
1. Gunes M, Gecmen C, Beker Evans M, et al. Validated Risk Score for Predicting 
   6-Month Mortality in Infective Endocarditis. J Am Heart Assoc. 2017 Apr 7;6(4):e003016. 
   doi: 10.1161/JAHA.115.003016.
2. Murdoch DR, Corey GR, Hoen B, et al. Clinical presentation, etiology, and outcome 
   of infective endocarditis in the 21st century: the International Collaboration on 
   Endocarditis-Prospective Cohort Study. Arch Intern Med. 2009 Mar 9;169(5):463-73. 
   doi: 10.1001/archinternmed.2008.603.
3. Cahill TJ, Baddour LM, Habib G, et al. Challenges in Infective Endocarditis. 
   J Am Coll Cardiol. 2017 Jul 25;70(3):325-335. doi: 10.1016/j.jacc.2017.06.007.
"""

import math
from typing import Dict, Any


class IeMortalityRiskScoreCalculator:
    """Calculator for Infective Endocarditis (IE) Mortality Risk Score"""
    
    def __init__(self):
        # IE Mortality Risk Score point values
        self.scoring_weights = {
            "age_category": {
                "45_or_under": 0,
                "46_to_60": 2,
                "61_to_70": 3,
                "over_70": 4
            },
            "history_of_dialysis": {
                "no": 0,
                "yes": 3
            },
            "nosocomial_ie": {
                "no": 0,
                "yes": 2
            },
            "prosthetic_ie": {
                "no": 0,
                "yes": 1
            },
            "symptoms_over_1_month": {
                "no": 0,
                "yes": -1  # Negative points for better prognosis
            },
            "staphylococcus_aureus": {
                "no": 0,
                "yes": 1
            },
            "viridans_group_streptococci": {
                "no": 0,
                "yes": -2  # Negative points for better prognosis
            },
            "aortic_vegetation": {
                "no": 0,
                "yes": 1
            },
            "mitral_vegetation": {
                "no": 0,
                "yes": 1
            },
            "nyha_class_3_or_4_hf": {
                "no": 0,
                "yes": 3
            },
            "stroke": {
                "no": 0,
                "yes": 2
            },
            "paravalvular_complication": {
                "no": 0,
                "yes": 2
            },
            "persistent_bacteremia": {
                "no": 0,
                "yes": 2
            },
            "surgical_treatment": {
                "no": 0,
                "yes": -2  # Negative points for better prognosis
            }
        }
    
    def calculate(self, age_category: str, history_of_dialysis: str, nosocomial_ie: str,
                 prosthetic_ie: str, symptoms_over_1_month: str, staphylococcus_aureus: str,
                 viridans_group_streptococci: str, aortic_vegetation: str, mitral_vegetation: str,
                 nyha_class_3_or_4_hf: str, stroke: str, paravalvular_complication: str,
                 persistent_bacteremia: str, surgical_treatment: str) -> Dict[str, Any]:
        """
        Calculates the IE Mortality Risk Score and 6-month mortality probability
        
        Args:
            age_category (str): Patient age category
            history_of_dialysis (str): History of chronic dialysis
            nosocomial_ie (str): Healthcare-associated IE
            prosthetic_ie (str): Prosthetic valve IE
            symptoms_over_1_month (str): Symptoms >1 month before admission
            staphylococcus_aureus (str): S. aureus as causative pathogen
            viridans_group_streptococci (str): Viridans group strep as pathogen
            aortic_vegetation (str): Aortic valve vegetation
            mitral_vegetation (str): Mitral valve vegetation
            nyha_class_3_or_4_hf (str): NYHA Class 3-4 heart failure
            stroke (str): Stroke complication
            paravalvular_complication (str): Paravalvular complications
            persistent_bacteremia (str): Persistent bacteremia
            surgical_treatment (str): Surgical treatment performed
            
        Returns:
            Dict with the mortality probability and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_category, history_of_dialysis, nosocomial_ie, prosthetic_ie,
            symptoms_over_1_month, staphylococcus_aureus, viridans_group_streptococci,
            aortic_vegetation, mitral_vegetation, nyha_class_3_or_4_hf, stroke,
            paravalvular_complication, persistent_bacteremia, surgical_treatment
        )
        
        # Calculate total score
        score = self._calculate_total_score(
            age_category, history_of_dialysis, nosocomial_ie, prosthetic_ie,
            symptoms_over_1_month, staphylococcus_aureus, viridans_group_streptococci,
            aortic_vegetation, mitral_vegetation, nyha_class_3_or_4_hf, stroke,
            paravalvular_complication, persistent_bacteremia, surgical_treatment
        )
        
        # Calculate mortality probability
        mortality_probability = self._calculate_mortality_probability(score)
        
        # Get interpretation
        interpretation = self._get_interpretation(mortality_probability)
        
        return {
            "result": round(mortality_probability, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, history_of_dialysis: str, nosocomial_ie: str,
                        prosthetic_ie: str, symptoms_over_1_month: str, staphylococcus_aureus: str,
                        viridans_group_streptococci: str, aortic_vegetation: str, mitral_vegetation: str,
                        nyha_class_3_or_4_hf: str, stroke: str, paravalvular_complication: str,
                        persistent_bacteremia: str, surgical_treatment: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "age_category": ["45_or_under", "46_to_60", "61_to_70", "over_70"],
            "binary_params": ["no", "yes"]
        }
        
        # Validate age category
        if age_category not in valid_options["age_category"]:
            raise ValueError(f"age_category must be one of: {valid_options['age_category']}")
        
        # Validate binary parameters
        binary_params = [
            ("history_of_dialysis", history_of_dialysis),
            ("nosocomial_ie", nosocomial_ie),
            ("prosthetic_ie", prosthetic_ie),
            ("symptoms_over_1_month", symptoms_over_1_month),
            ("staphylococcus_aureus", staphylococcus_aureus),
            ("viridans_group_streptococci", viridans_group_streptococci),
            ("aortic_vegetation", aortic_vegetation),
            ("mitral_vegetation", mitral_vegetation),
            ("nyha_class_3_or_4_hf", nyha_class_3_or_4_hf),
            ("stroke", stroke),
            ("paravalvular_complication", paravalvular_complication),
            ("persistent_bacteremia", persistent_bacteremia),
            ("surgical_treatment", surgical_treatment)
        ]
        
        for param_name, param_value in binary_params:
            if param_value not in valid_options["binary_params"]:
                raise ValueError(f"{param_name} must be 'no' or 'yes'")
    
    def _calculate_total_score(self, age_category: str, history_of_dialysis: str, nosocomial_ie: str,
                              prosthetic_ie: str, symptoms_over_1_month: str, staphylococcus_aureus: str,
                              viridans_group_streptococci: str, aortic_vegetation: str, mitral_vegetation: str,
                              nyha_class_3_or_4_hf: str, stroke: str, paravalvular_complication: str,
                              persistent_bacteremia: str, surgical_treatment: str) -> int:
        """
        Calculates the total IE Mortality Risk Score
        
        IE Mortality Risk Score Components:
        Host Factors: Age (0-4 points), Dialysis history (0 or 3 points)
        IE Factors: Nosocomial (0 or 2), Prosthetic (0 or 1), Symptoms >1mo (0 or -1),
                   S. aureus (0 or 1), Viridans strep (0 or -2), Aortic veg (0 or 1), Mitral veg (0 or 1)
        Complications: NYHA 3-4 HF (0 or 3), Stroke (0 or 2), Paravalvular (0 or 2), 
                      Persistent bacteremia (0 or 2), Surgery (0 or -2)
        
        Total score range: approximately -5 to +20 points
        """
        
        total_score = 0
        
        # Add points for each parameter
        total_score += self.scoring_weights["age_category"][age_category]
        total_score += self.scoring_weights["history_of_dialysis"][history_of_dialysis]
        total_score += self.scoring_weights["nosocomial_ie"][nosocomial_ie]
        total_score += self.scoring_weights["prosthetic_ie"][prosthetic_ie]
        total_score += self.scoring_weights["symptoms_over_1_month"][symptoms_over_1_month]
        total_score += self.scoring_weights["staphylococcus_aureus"][staphylococcus_aureus]
        total_score += self.scoring_weights["viridans_group_streptococci"][viridans_group_streptococci]
        total_score += self.scoring_weights["aortic_vegetation"][aortic_vegetation]
        total_score += self.scoring_weights["mitral_vegetation"][mitral_vegetation]
        total_score += self.scoring_weights["nyha_class_3_or_4_hf"][nyha_class_3_or_4_hf]
        total_score += self.scoring_weights["stroke"][stroke]
        total_score += self.scoring_weights["paravalvular_complication"][paravalvular_complication]
        total_score += self.scoring_weights["persistent_bacteremia"][persistent_bacteremia]
        total_score += self.scoring_weights["surgical_treatment"][surgical_treatment]
        
        return total_score
    
    def _calculate_mortality_probability(self, score: int) -> float:
        """
        Calculates 6-month mortality probability using the validated formula
        
        Formula: Probability = 100 × [1 / (1 + exp(-(2.416×score + 0.109×score² - 4.849)))]
        
        This is the logistic regression formula converted from the original:
        Original: 2.416×score + 0.109×score² - 4.849
        Logistic: 1 / (1 + exp(-linear_predictor))
        
        Args:
            score (int): Total IE mortality risk score
            
        Returns:
            float: 6-month mortality probability as percentage (0-100)
        """
        
        # Calculate linear predictor
        linear_predictor = 2.416 * score + 0.109 * (score ** 2) - 4.849
        
        # Calculate probability using logistic function
        try:
            probability = 1 / (1 + math.exp(-linear_predictor))
            probability_percentage = probability * 100
            
            # Ensure probability is between 0 and 100
            probability_percentage = max(0, min(100, probability_percentage))
            
            return probability_percentage
            
        except OverflowError:
            # Handle extreme values
            if linear_predictor > 500:
                return 100.0
            else:
                return 0.0
    
    def _get_interpretation(self, mortality_probability: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mortality probability
        
        Args:
            mortality_probability (float): 6-month mortality probability percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if mortality_probability <= 10:
            return {
                "stage": "Low Risk",
                "description": f"Mortality probability {mortality_probability:.1f}% (≤10%)",
                "interpretation": "Low risk of 6-month mortality. Consider standard medical management with close monitoring."
            }
        elif mortality_probability <= 25:
            return {
                "stage": "Moderate Risk",
                "description": f"Mortality probability {mortality_probability:.1f}% (10-25%)",
                "interpretation": "Moderate risk of 6-month mortality. Consider intensive medical management and evaluation for surgical intervention if indicated."
            }
        elif mortality_probability <= 50:
            return {
                "stage": "High Risk",
                "description": f"Mortality probability {mortality_probability:.1f}% (25-50%)",
                "interpretation": "High risk of 6-month mortality. Consider aggressive treatment including surgical evaluation if appropriate. Discuss prognosis with patient and family."
            }
        else:  # > 50%
            return {
                "stage": "Very High Risk",
                "description": f"Mortality probability {mortality_probability:.1f}% (>50%)",
                "interpretation": "Very high risk of 6-month mortality. Consider palliative care consultation and goals of care discussion. Surgical intervention may be considered only in highly selected cases."
            }


def calculate_ie_mortality_risk_score(age_category: str, history_of_dialysis: str, nosocomial_ie: str,
                                     prosthetic_ie: str, symptoms_over_1_month: str, staphylococcus_aureus: str,
                                     viridans_group_streptococci: str, aortic_vegetation: str, mitral_vegetation: str,
                                     nyha_class_3_or_4_hf: str, stroke: str, paravalvular_complication: str,
                                     persistent_bacteremia: str, surgical_treatment: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = IeMortalityRiskScoreCalculator()
    return calculator.calculate(
        age_category, history_of_dialysis, nosocomial_ie, prosthetic_ie,
        symptoms_over_1_month, staphylococcus_aureus, viridans_group_streptococci,
        aortic_vegetation, mitral_vegetation, nyha_class_3_or_4_hf, stroke,
        paravalvular_complication, persistent_bacteremia, surgical_treatment
    )