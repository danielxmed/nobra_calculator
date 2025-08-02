"""
Index of Severity for Eosinophilic Esophagitis (I-SEE) Calculator

Classifies severity of eosinophilic esophagitis (EoE) using a comprehensive scoring system 
that evaluates symptoms, complications, inflammatory features, and fibrostenotic changes.
The I-SEE standardizes disease severity assessment beyond eosinophil counts alone.

References (Vancouver style):
1. Hirano I, Aceves SS, Blanchard C, et al. A Clinical Severity Index for Eosinophilic 
   Esophagitis: Development, Consensus, and Future Directions. Gastroenterology. 2022 
   Jul;163(1):59-76.e16. doi: 10.1053/j.gastro.2022.02.048.
2. Rank MA, Shaffer K, Campion J, et al. A newly proposed severity index for eosinophilic 
   esophagitis is associated with baseline clinical features and successful treatment response. 
   Clin Gastroenterol Hepatol. 2023 Oct;21(11):2890-2897.e2. doi: 10.1016/j.cgh.2023.04.013.
3. Stern E, Schoepfer A, Spechler SJ, et al. The Index of Severity for Eosinophilic 
   Esophagitis (I-SEE) Reflects Longitudinal Clinicopathologic Changes in Children. 
   J Pediatr Gastroenterol Nutr. 2023 Dec;77(6):743-749. doi: 10.1097/MPG.0000000000003928.
"""

from typing import Dict, Any


class ISeeScoreCalculator:
    """Calculator for Index of Severity for Eosinophilic Esophagitis (I-SEE)"""
    
    def __init__(self):
        # I-SEE scoring weights
        self.scoring_weights = {
            "symptoms_frequency": {
                "none": 0,
                "weekly": 1,
                "daily": 2,
                "multiple_daily": 4
            },
            "food_impaction": {
                "none": 0,
                "adult_with_er": 2,
                "pediatric_with_er": 4
            },
            "hospitalization_due_eoe": {
                "no": 0,
                "yes": 4
            },
            "esophageal_perforation": {
                "no": 0,
                "yes": 15
            },
            "malnutrition": {
                "none": 0,
                "present": 15
            },
            "persistent_inflammation": {
                "none": 0,
                "present": 15
            },
            "inflammatory_features": {
                "none": 0,
                "localized": 1,
                "diffuse": 2
            },
            "eosinophil_count": {
                "under_15": 0,
                "15_to_60": 1,
                "over_60": 2
            },
            "rings_strictures": {
                "none": 0,
                "endoscope_passes_easily": 1,
                "requires_dilation": 2,
                "cannot_pass_endoscope": 15
            }
        }
        
        # Severity interpretation thresholds
        self.severity_categories = {
            0: {
                "stage": "Inactive",
                "description": "Score 0 points",
                "interpretation": "Inactive EoE. No evidence of active disease. Continue current management and monitor for disease recurrence."
            }
        }
    
    def calculate(self, symptoms_frequency: str, food_impaction: str, hospitalization_due_eoe: str,
                 esophageal_perforation: str, malnutrition: str, persistent_inflammation: str,
                 inflammatory_features: str, eosinophil_count: str, rings_strictures: str) -> Dict[str, Any]:
        """
        Calculates the I-SEE Severity Score
        
        Args:
            symptoms_frequency (str): Frequency of EoE-related symptoms
            food_impaction (str): History of food impaction requiring ER visit/endoscopy
            hospitalization_due_eoe (str): Hospitalization specifically due to EoE
            esophageal_perforation (str): History of esophageal perforation
            malnutrition (str): Malnutrition (body mass <5th percentile or decreased growth)
            persistent_inflammation (str): Persistent inflammation requiring special treatments
            inflammatory_features (str): Endoscopic inflammatory features (edema, furrows, exudates)
            eosinophil_count (str): Peak eosinophil count per high-power field
            rings_strictures (str): Presence and severity of esophageal rings or strictures
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(symptoms_frequency, food_impaction, hospitalization_due_eoe,
                            esophageal_perforation, malnutrition, persistent_inflammation,
                            inflammatory_features, eosinophil_count, rings_strictures)
        
        # Calculate total score
        score = self._calculate_total_score(
            symptoms_frequency, food_impaction, hospitalization_due_eoe, esophageal_perforation,
            malnutrition, persistent_inflammation, inflammatory_features, eosinophil_count, rings_strictures
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
    
    def _validate_inputs(self, symptoms_frequency: str, food_impaction: str, hospitalization_due_eoe: str,
                        esophageal_perforation: str, malnutrition: str, persistent_inflammation: str,
                        inflammatory_features: str, eosinophil_count: str, rings_strictures: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "symptoms_frequency": ["none", "weekly", "daily", "multiple_daily"],
            "food_impaction": ["none", "adult_with_er", "pediatric_with_er"],
            "hospitalization_due_eoe": ["no", "yes"],
            "esophageal_perforation": ["no", "yes"],
            "malnutrition": ["none", "present"],
            "persistent_inflammation": ["none", "present"],
            "inflammatory_features": ["none", "localized", "diffuse"],
            "eosinophil_count": ["under_15", "15_to_60", "over_60"],
            "rings_strictures": ["none", "endoscope_passes_easily", "requires_dilation", "cannot_pass_endoscope"]
        }
        
        # Validate each parameter
        parameters = {
            "symptoms_frequency": symptoms_frequency,
            "food_impaction": food_impaction,
            "hospitalization_due_eoe": hospitalization_due_eoe,
            "esophageal_perforation": esophageal_perforation,
            "malnutrition": malnutrition,
            "persistent_inflammation": persistent_inflammation,
            "inflammatory_features": inflammatory_features,
            "eosinophil_count": eosinophil_count,
            "rings_strictures": rings_strictures
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, symptoms_frequency: str, food_impaction: str, hospitalization_due_eoe: str,
                              esophageal_perforation: str, malnutrition: str, persistent_inflammation: str,
                              inflammatory_features: str, eosinophil_count: str, rings_strictures: str) -> int:
        """
        Calculates the total I-SEE Severity Score
        
        I-SEE Scoring System:
        - Symptoms: None (0), Weekly (1), Daily (2), Multiple daily/disrupting function (4)
        - Food impaction: None (0), Adult ER/endoscopy (2), Pediatric ER/endoscopy (4)
        - Hospitalization due to EoE: No (0), Yes (4)
        - Esophageal perforation: No (0), Yes (15)
        - Malnutrition: None (0), Present (15)
        - Persistent inflammation: None (0), Present (15)
        - Inflammatory features: None (0), Localized (1), Diffuse (2)
        - Eosinophil count: <15 (0), 15-60 (1), >60 (2)
        - Rings/strictures: None (0), Easy passage (1), Requires dilation (2), Cannot pass (15)
        """
        
        total_score = 0
        
        # Add points for each domain
        total_score += self.scoring_weights["symptoms_frequency"][symptoms_frequency]
        total_score += self.scoring_weights["food_impaction"][food_impaction]
        total_score += self.scoring_weights["hospitalization_due_eoe"][hospitalization_due_eoe]
        total_score += self.scoring_weights["esophageal_perforation"][esophageal_perforation]
        total_score += self.scoring_weights["malnutrition"][malnutrition]
        total_score += self.scoring_weights["persistent_inflammation"][persistent_inflammation]
        total_score += self.scoring_weights["inflammatory_features"][inflammatory_features]
        total_score += self.scoring_weights["eosinophil_count"][eosinophil_count]
        total_score += self.scoring_weights["rings_strictures"][rings_strictures]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on I-SEE Severity Score
        
        Args:
            score (int): I-SEE Severity Score
            
        Returns:
            Dict with interpretation details
        """
        
        # Severity classification based on I-SEE score
        if score == 0:
            return {
                "stage": "Inactive",
                "description": "Score 0 points",
                "interpretation": "Inactive EoE. No evidence of active disease. Continue current management and monitor for disease recurrence."
            }
        elif 1 <= score <= 6:
            return {
                "stage": "Mild",
                "description": f"Score {score} points (1-6 points)",
                "interpretation": "Mild EoE severity. Disease is present but with minimal impact on function and low complication risk. Standard topical corticosteroid therapy typically effective."
            }
        elif 7 <= score <= 14:
            return {
                "stage": "Moderate",
                "description": f"Score {score} points (7-14 points)",
                "interpretation": "Moderate EoE severity. Significant disease activity with moderate functional impact. May require combination therapy or dietary interventions alongside standard treatment."
            }
        else:  # score >= 15
            return {
                "stage": "Severe",
                "description": f"Score {score} points (≥15 points)",
                "interpretation": "Severe EoE. High disease burden with significant complications or refractory features. May require advanced therapies, mechanical interventions (dilation), or multidisciplinary management approach."
            }


def calculate_i_see_score(symptoms_frequency: str, food_impaction: str, hospitalization_due_eoe: str,
                         esophageal_perforation: str, malnutrition: str, persistent_inflammation: str,
                         inflammatory_features: str, eosinophil_count: str, rings_strictures: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ISeeScoreCalculator()
    return calculator.calculate(
        symptoms_frequency, food_impaction, hospitalization_due_eoe, esophageal_perforation,
        malnutrition, persistent_inflammation, inflammatory_features, eosinophil_count, rings_strictures
    )