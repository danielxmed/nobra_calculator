"""
Indian Takayasu Clinical Activity Score (ITAS2010) Calculator

Differentiates between active and inactive disease in Takayasu arteritis (TA).
The ITAS2010 is a validated clinical activity measure specifically developed 
for Takayasu arteritis, assessing new or worsening symptoms within the past 3 months.

References (Vancouver style):
1. Misra R, Danda D, Rajappa SM, et al. Development and initial validation of the 
   Indian Takayasu Clinical Activity Score (ITAS2010). Rheumatology (Oxford). 
   2013 Oct;52(10):1795-801. doi: 10.1093/rheumatology/ket128.
2. Abularrage CJ, Sidawy AN, White PW, et al. Evaluation of the clinical effectiveness 
   of percutaneous transluminal angioplasty for Takayasu arteritis. J Vasc Surg. 
   2007;45(2):314-318.
3. Kerr GS, Hallahan CW, Giordano J, et al. Takayasu arteritis. Ann Intern Med. 
   1994;120(11):919-929.
"""

from typing import Dict, Any


class Itas2010Calculator:
    """Calculator for Indian Takayasu Clinical Activity Score (ITAS2010)"""
    
    def __init__(self):
        # ITAS2010 scoring weights
        self.scoring_weights = {
            # Systemic manifestations (1 point each)
            "malaise_weight_loss": {"no": 0, "yes": 1},
            "myalgia_arthralgia": {"no": 0, "yes": 1}, 
            "headache": {"no": 0, "yes": 1},
            
            # Abdominal manifestations (1 point)
            "severe_abdominal_pain": {"no": 0, "yes": 1},
            
            # Genitourinary manifestations (1 point)
            "recent_spontaneous_abortion": {"no": 0, "yes": 1},
            
            # Renal manifestations (systolic 1 point, diastolic 2 points)
            "systolic_bp_over_140": {"no": 0, "yes": 1},
            "diastolic_bp_over_90": {"no": 0, "yes": 2},  # Weighted 2 points
            
            # Neurological manifestations (stroke 2 points, others 1 point)
            "stroke": {"no": 0, "yes": 2},  # Weighted 2 points
            "seizures": {"no": 0, "yes": 1},
            "syncope": {"no": 0, "yes": 1},
            "vertigo_dizziness": {"no": 0, "yes": 1},
            
            # Cardiovascular manifestations (key items 2 points, others 1 point)
            "bruits": {"no": 0, "yes": 2},  # Weighted 2 points
            "pulse_inequality": {"no": 0, "yes": 2},  # Weighted 2 points
            "new_loss_of_pulses": {"no": 0, "yes": 2},  # Weighted 2 points
            "claudication": {"no": 0, "yes": 2},  # Weighted 2 points
            "carotidynia": {"no": 0, "yes": 2},  # Weighted 2 points
            "aortic_incompetence": {"no": 0, "yes": 1},
            "mi_angina": {"no": 0, "yes": 1},
            "cardiomyopathy_cardiac_failure": {"no": 0, "yes": 1}
        }
    
    def calculate(self, malaise_weight_loss: str, myalgia_arthralgia: str, headache: str,
                 severe_abdominal_pain: str, recent_spontaneous_abortion: str, 
                 systolic_bp_over_140: str, diastolic_bp_over_90: str, stroke: str,
                 seizures: str, syncope: str, vertigo_dizziness: str, bruits: str,
                 pulse_inequality: str, new_loss_of_pulses: str, claudication: str,
                 carotidynia: str, aortic_incompetence: str, mi_angina: str,
                 cardiomyopathy_cardiac_failure: str) -> Dict[str, Any]:
        """
        Calculates the ITAS2010 score
        
        Args:
            malaise_weight_loss (str): Malaise or weight loss >2 kg
            myalgia_arthralgia (str): Myalgia, arthralgia, or arthritis
            headache (str): New or worsening headache
            severe_abdominal_pain (str): Severe abdominal pain
            recent_spontaneous_abortion (str): Recent spontaneous abortion
            systolic_bp_over_140 (str): Systolic BP >140 mmHg
            diastolic_bp_over_90 (str): Diastolic BP >90 mmHg  
            stroke (str): Stroke
            seizures (str): Seizures
            syncope (str): Syncope
            vertigo_dizziness (str): Vertigo or dizziness
            bruits (str): Arterial bruits
            pulse_inequality (str): Pulse inequality between limbs
            new_loss_of_pulses (str): New loss of pulses
            claudication (str): Claudication
            carotidynia (str): Carotidynia (carotid artery tenderness)
            aortic_incompetence (str): Aortic incompetence
            mi_angina (str): Myocardial infarction or angina
            cardiomyopathy_cardiac_failure (str): Cardiomyopathy or cardiac failure
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            malaise_weight_loss, myalgia_arthralgia, headache, severe_abdominal_pain,
            recent_spontaneous_abortion, systolic_bp_over_140, diastolic_bp_over_90,
            stroke, seizures, syncope, vertigo_dizziness, bruits, pulse_inequality,
            new_loss_of_pulses, claudication, carotidynia, aortic_incompetence,
            mi_angina, cardiomyopathy_cardiac_failure
        )
        
        # Calculate total score
        score = self._calculate_total_score(
            malaise_weight_loss, myalgia_arthralgia, headache, severe_abdominal_pain,
            recent_spontaneous_abortion, systolic_bp_over_140, diastolic_bp_over_90,
            stroke, seizures, syncope, vertigo_dizziness, bruits, pulse_inequality,
            new_loss_of_pulses, claudication, carotidynia, aortic_incompetence,
            mi_angina, cardiomyopathy_cardiac_failure
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
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # All parameters should be "no" or "yes"
        valid_options = ["no", "yes"]
        parameter_names = [
            "malaise_weight_loss", "myalgia_arthralgia", "headache", "severe_abdominal_pain",
            "recent_spontaneous_abortion", "systolic_bp_over_140", "diastolic_bp_over_90",
            "stroke", "seizures", "syncope", "vertigo_dizziness", "bruits", "pulse_inequality",
            "new_loss_of_pulses", "claudication", "carotidynia", "aortic_incompetence",
            "mi_angina", "cardiomyopathy_cardiac_failure"
        ]
        
        for i, value in enumerate(args):
            if value not in valid_options:
                raise ValueError(f"{parameter_names[i]} must be 'no' or 'yes'")
    
    def _calculate_total_score(self, malaise_weight_loss: str, myalgia_arthralgia: str, 
                              headache: str, severe_abdominal_pain: str, 
                              recent_spontaneous_abortion: str, systolic_bp_over_140: str,
                              diastolic_bp_over_90: str, stroke: str, seizures: str,
                              syncope: str, vertigo_dizziness: str, bruits: str,
                              pulse_inequality: str, new_loss_of_pulses: str,
                              claudication: str, carotidynia: str, aortic_incompetence: str,
                              mi_angina: str, cardiomyopathy_cardiac_failure: str) -> int:
        """
        Calculates the total ITAS2010 score
        
        ITAS2010 Scoring System:
        Systemic: Malaise/weight loss (1), Myalgia/arthralgia (1), Headache (1)
        Abdominal: Severe abdominal pain (1)
        Genitourinary: Recent spontaneous abortion (1)
        Renal: Systolic BP >140 (1), Diastolic BP >90 (2)
        Neurological: Stroke (2), Seizures (1), Syncope (1), Vertigo/dizziness (1)
        Cardiovascular: Bruits (2), Pulse inequality (2), New loss of pulses (2), 
                       Claudication (2), Carotidynia (2), Aortic incompetence (1),
                       MI/angina (1), Cardiomyopathy/cardiac failure (1)
        """
        
        total_score = 0
        
        # Collect all parameters in a dictionary
        parameters = {
            "malaise_weight_loss": malaise_weight_loss,
            "myalgia_arthralgia": myalgia_arthralgia,
            "headache": headache,
            "severe_abdominal_pain": severe_abdominal_pain,
            "recent_spontaneous_abortion": recent_spontaneous_abortion,
            "systolic_bp_over_140": systolic_bp_over_140,
            "diastolic_bp_over_90": diastolic_bp_over_90,
            "stroke": stroke,
            "seizures": seizures,
            "syncope": syncope,
            "vertigo_dizziness": vertigo_dizziness,
            "bruits": bruits,
            "pulse_inequality": pulse_inequality,
            "new_loss_of_pulses": new_loss_of_pulses,
            "claudication": claudication,
            "carotidynia": carotidynia,
            "aortic_incompetence": aortic_incompetence,
            "mi_angina": mi_angina,
            "cardiomyopathy_cardiac_failure": cardiomyopathy_cardiac_failure
        }
        
        # Add points for each positive finding
        for param_name, param_value in parameters.items():
            total_score += self.scoring_weights[param_name][param_value]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on ITAS2010 score
        
        Args:
            score (int): ITAS2010 score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 2:
            return {
                "stage": "Inactive",
                "description": f"Score {score} points (<2 points)",
                "interpretation": "Inactive disease. No evidence of active Takayasu arteritis. Continue current maintenance therapy and monitor for disease recurrence."
            }
        else:
            return {
                "stage": "Active", 
                "description": f"Score {score} points (≥2 points)",
                "interpretation": "Active disease. Evidence of active Takayasu arteritis requiring treatment intensification. Consider immunosuppressive therapy escalation or initiation of biological agents."
            }


def calculate_itas_2010(malaise_weight_loss: str, myalgia_arthralgia: str, headache: str,
                       severe_abdominal_pain: str, recent_spontaneous_abortion: str,
                       systolic_bp_over_140: str, diastolic_bp_over_90: str, stroke: str,
                       seizures: str, syncope: str, vertigo_dizziness: str, bruits: str,
                       pulse_inequality: str, new_loss_of_pulses: str, claudication: str,
                       carotidynia: str, aortic_incompetence: str, mi_angina: str,
                       cardiomyopathy_cardiac_failure: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Itas2010Calculator()
    return calculator.calculate(
        malaise_weight_loss, myalgia_arthralgia, headache, severe_abdominal_pain,
        recent_spontaneous_abortion, systolic_bp_over_140, diastolic_bp_over_90,
        stroke, seizures, syncope, vertigo_dizziness, bruits, pulse_inequality,
        new_loss_of_pulses, claudication, carotidynia, aortic_incompetence,
        mi_angina, cardiomyopathy_cardiac_failure
    )