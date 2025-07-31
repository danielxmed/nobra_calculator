"""
DRAGON Score for Post-TPA Stroke Outcome Calculator

Predicts 3-month outcome (functional independence vs dependency) in ischemic stroke 
patients treated with tissue plasminogen activator (tPA). The DRAGON score helps 
identify patients who may benefit from additional therapeutic interventions.

References:
1. Strbian D, Meretoja A, Ahlhelm FJ, et al. Predicting outcome of IV thrombolysis-treated 
   ischemic stroke patients: the DRAGON score. Neurology. 2012;78(6):427-432. 
   doi: 10.1212/WNL.0b013e318245d2a9.
2. Turc G, Maïer B, Naggara O, et al. Clinical scales do not reliably identify acute 
   ischemic stroke patients with large-artery occlusion. Stroke. 2016;47(6):1466-1472. 
   doi: 10.1161/STROKEAHA.115.011336.
3. Saposnik G, Guzik AK, Reeves M, et al. Stroke Prognosis Assessment Scale (SPAS) to 
   predict mortality and functional outcome. Stroke. 2014;45(7):2018-2024. 
   doi: 10.1161/STROKEAHA.114.004667.
"""

from typing import Dict, Any


class DragonScoreCalculator:
    """Calculator for DRAGON Score for Post-TPA Stroke Outcome"""
    
    def __init__(self):
        # Score component definitions
        self.HYPERDENSE_ARTERY_SCORES = {
            "none": 0,
            "either": 1,
            "both": 2
        }
        
        self.PRESTROKE_MRS_SCORES = {
            "no": 0,
            "yes": 1
        }
    
    def calculate(self, hyperdense_artery_infarct: str, prestroke_mrs: str, 
                 age: int, glucose: float, onset_to_treatment: int, 
                 nihss: int) -> Dict[str, Any]:
        """
        Calculates the DRAGON score for post-TPA stroke outcome prediction
        
        Args:
            hyperdense_artery_infarct (str): CT findings ("none", "either", "both")
            prestroke_mrs (str): Pre-stroke mRS >1 ("no" or "yes")
            age (int): Patient age in years
            glucose (float): Baseline glucose in mg/dL
            onset_to_treatment (int): Time from onset to treatment in minutes
            nihss (int): Baseline NIHSS score (0-42)
            
        Returns:
            Dict with the DRAGON score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hyperdense_artery_infarct, prestroke_mrs, age, 
                             glucose, onset_to_treatment, nihss)
        
        # Calculate component scores
        d_score = self._get_hyperdense_score(hyperdense_artery_infarct)
        r_score = self._get_prestroke_mrs_score(prestroke_mrs)
        a_score = self._get_age_score(age)
        g_score = self._get_glucose_score(glucose)
        o_score = self._get_onset_score(onset_to_treatment)
        n_score = self._get_nihss_score(nihss)
        
        # Calculate total score
        total_score = d_score + r_score + a_score + g_score + o_score + n_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "hyperdense_artery": d_score,
                "prestroke_mrs": r_score,
                "age": a_score,
                "glucose": g_score,
                "onset_time": o_score,
                "nihss": n_score
            }
        }
    
    def _validate_inputs(self, hyperdense_artery_infarct: str, prestroke_mrs: str,
                        age: int, glucose: float, onset_to_treatment: int, nihss: int):
        """Validates input parameters"""
        
        # Validate hyperdense artery/infarct
        if not isinstance(hyperdense_artery_infarct, str):
            raise ValueError("hyperdense_artery_infarct must be a string")
        if hyperdense_artery_infarct.lower() not in self.HYPERDENSE_ARTERY_SCORES:
            raise ValueError("hyperdense_artery_infarct must be 'none', 'either', or 'both'")
        
        # Validate prestroke mRS
        if not isinstance(prestroke_mrs, str):
            raise ValueError("prestroke_mrs must be a string")
        if prestroke_mrs.lower() not in self.PRESTROKE_MRS_SCORES:
            raise ValueError("prestroke_mrs must be 'no' or 'yes'")
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("age must be an integer")
        if age < 18 or age > 120:
            raise ValueError("age must be between 18 and 120 years")
        
        # Validate glucose
        if not isinstance(glucose, (int, float)):
            raise ValueError("glucose must be a number")
        if glucose < 50 or glucose > 800:
            raise ValueError("glucose must be between 50 and 800 mg/dL")
        
        # Validate onset to treatment time
        if not isinstance(onset_to_treatment, int):
            raise ValueError("onset_to_treatment must be an integer")
        if onset_to_treatment < 0 or onset_to_treatment > 480:
            raise ValueError("onset_to_treatment must be between 0 and 480 minutes")
        
        # Validate NIHSS
        if not isinstance(nihss, int):
            raise ValueError("nihss must be an integer")
        if nihss < 0 or nihss > 42:
            raise ValueError("nihss must be between 0 and 42")
    
    def _get_hyperdense_score(self, hyperdense_artery_infarct: str) -> int:
        """Gets score for hyperdense artery/early infarct signs"""
        return self.HYPERDENSE_ARTERY_SCORES[hyperdense_artery_infarct.lower()]
    
    def _get_prestroke_mrs_score(self, prestroke_mrs: str) -> int:
        """Gets score for pre-stroke mRS >1"""
        return self.PRESTROKE_MRS_SCORES[prestroke_mrs.lower()]
    
    def _get_age_score(self, age: int) -> int:
        """Gets score for age component"""
        if age < 65:
            return 0
        elif age <= 79:
            return 1
        else:  # age >= 80
            return 2
    
    def _get_glucose_score(self, glucose: float) -> int:
        """Gets score for glucose component (>144 mg/dL = 8 mmol/L)"""
        return 1 if glucose > 144 else 0
    
    def _get_onset_score(self, onset_to_treatment: int) -> int:
        """Gets score for onset to treatment time (>90 minutes)"""
        return 1 if onset_to_treatment > 90 else 0
    
    def _get_nihss_score(self, nihss: int) -> int:
        """Gets score for NIHSS component"""
        if nihss <= 4:
            return 0
        elif nihss <= 9:
            return 1
        elif nihss <= 15:
            return 2
        else:  # nihss >= 16
            return 3
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on DRAGON score
        
        Args:
            score (int): DRAGON score (0-10)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Excellent Prognosis",
                "description": "Very low risk",
                "interpretation": "96% chance of good outcome (mRS 0-2 at 3 months). Excellent functional prognosis with near-certain functional independence."
            }
        elif score == 2:
            return {
                "stage": "Good Prognosis",
                "description": "Low risk",
                "interpretation": "88% chance of good outcome (mRS 0-2 at 3 months). Good functional prognosis with high likelihood of functional independence."
            }
        elif score == 3:
            return {
                "stage": "Moderate Prognosis",
                "description": "Moderate risk",
                "interpretation": "74% chance of good outcome (mRS 0-2 at 3 months). Moderate functional prognosis with considerable chance of functional independence."
            }
        elif score <= 7:
            return {
                "stage": "Poor Prognosis",
                "description": "High risk",
                "interpretation": "Progressively decreasing chance of good outcome. Consider additional therapeutic interventions or advanced stroke care strategies."
            }
        elif score == 8:
            return {
                "stage": "Very Poor Prognosis",
                "description": "Very high risk",
                "interpretation": "0% chance of good outcome (mRS 0-2). 70% chance of miserable outcome (mRS 5-6). Strong consideration for additional rescue therapies."
            }
        else:  # score >= 9
            return {
                "stage": "Miserable Prognosis",
                "description": "Extremely high risk",
                "interpretation": "0% chance of good outcome (mRS 0-2). 100% chance of miserable outcome (mRS 5-6: bedridden, incontinent, requiring constant care, or death)."
            }


def calculate_dragon_score(hyperdense_artery_infarct: str, prestroke_mrs: str,
                          age: int, glucose: float, onset_to_treatment: int,
                          nihss: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dragon_score pattern
    """
    calculator = DragonScoreCalculator()
    return calculator.calculate(hyperdense_artery_infarct, prestroke_mrs, age,
                               glucose, onset_to_treatment, nihss)