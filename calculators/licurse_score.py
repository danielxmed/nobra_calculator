"""
Licurse Score for Renal Ultrasound Calculator

Predicts likelihood of hydronephrosis on renal ultrasonography requiring urological 
intervention in adult patients with acute kidney injury.

References:
1. Licurse A, Dziura J, Spinella PC, et al. Renal ultrasonography in the evaluation 
   of acute kidney injury: developing a risk stratification framework. Archives of 
   Internal Medicine. 2010;170(21):1900-7. doi: 10.1001/archinternmed.2010.362.
2. Ip IK, Silveira PC, Alper EC, et al. External validation of risk stratification 
   strategy in the use of renal ultrasonography in the evaluation of acute kidney 
   injury. Journal of Hospital Medicine. 2016;11(5):316-21.
"""

from typing import Dict, Any


class LicurseScoreCalculator:
    """Calculator for Licurse Score for Renal Ultrasound"""
    
    def __init__(self):
        # Risk percentages for hydronephrosis and intervention by score
        self.risk_data = {
            "low_risk": {
                "hydronephrosis_risk": 4.0,
                "intervention_risk": 1.1,
                "score_range": "≤2 points"
            },
            "medium_risk": {
                "hydronephrosis_risk": 6.8,
                "intervention_risk": 0.5,
                "score_range": "3 points"
            },
            "high_risk": {
                "hydronephrosis_risk": 20.9,
                "intervention_risk": 4.9,
                "score_range": ">3 points"
            }
        }
    
    def calculate(
        self,
        history_hydronephrosis: str,
        race: str,
        recurrent_utis: str,
        obstruction_diagnosis: str,
        history_chf: str,
        prerenal_aki_sepsis: str,
        nephrotoxic_exposure: str
    ) -> Dict[str, Any]:
        """
        Calculates the Licurse Score for renal ultrasound risk stratification
        
        Args:
            history_hydronephrosis (str): History of hydronephrosis ("yes" or "no")
            race (str): Patient race ("black" or "non_black")
            recurrent_utis (str): History of recurrent UTIs ("yes" or "no")
            obstruction_diagnosis (str): Diagnosis consistent with obstruction ("yes" or "no")
            history_chf (str): History of congestive heart failure ("yes" or "no")
            prerenal_aki_sepsis (str): History of sepsis/prerenal AKI/pressors ("yes" or "no")
            nephrotoxic_exposure (str): Exposure to nephrotoxic medications ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            history_hydronephrosis, race, recurrent_utis, obstruction_diagnosis,
            history_chf, prerenal_aki_sepsis, nephrotoxic_exposure
        )
        
        # Check for automatic high-risk assignment
        if history_hydronephrosis == "yes":
            return {
                "result": 99,  # Special value indicating automatic high-risk
                "unit": "points",
                "interpretation": self._get_high_risk_interpretation_with_history(),
                "stage": "High Risk",
                "stage_description": "High risk for hydronephrosis (history of hydronephrosis)"
            }
        
        # Calculate score for patients without prior hydronephrosis
        score = self._calculate_score(
            race, recurrent_utis, obstruction_diagnosis,
            history_chf, prerenal_aki_sepsis, nephrotoxic_exposure
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(
        self, history_hydronephrosis, race, recurrent_utis, obstruction_diagnosis,
        history_chf, prerenal_aki_sepsis, nephrotoxic_exposure
    ):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_race = ["black", "non_black"]
        
        if history_hydronephrosis not in valid_yes_no:
            raise ValueError("History of hydronephrosis must be 'yes' or 'no'")
        
        if race not in valid_race:
            raise ValueError("Race must be 'black' or 'non_black'")
        
        if recurrent_utis not in valid_yes_no:
            raise ValueError("Recurrent UTIs must be 'yes' or 'no'")
        
        if obstruction_diagnosis not in valid_yes_no:
            raise ValueError("Obstruction diagnosis must be 'yes' or 'no'")
        
        if history_chf not in valid_yes_no:
            raise ValueError("History of CHF must be 'yes' or 'no'")
        
        if prerenal_aki_sepsis not in valid_yes_no:
            raise ValueError("Prerenal AKI/sepsis must be 'yes' or 'no'")
        
        if nephrotoxic_exposure not in valid_yes_no:
            raise ValueError("Nephrotoxic exposure must be 'yes' or 'no'")
    
    def _calculate_score(
        self, race, recurrent_utis, obstruction_diagnosis,
        history_chf, prerenal_aki_sepsis, nephrotoxic_exposure
    ) -> int:
        """Calculates the Licurse Score based on risk factors"""
        
        score = 0
        
        # Non-black race: 1 point
        if race == "non_black":
            score += 1
        
        # History of recurrent UTIs: 1 point
        if recurrent_utis == "yes":
            score += 1
        
        # Diagnosis consistent with possible obstruction: 1 point
        if obstruction_diagnosis == "yes":
            score += 1
        
        # No history of congestive heart failure: 1 point
        if history_chf == "no":
            score += 1
        
        # No history of sepsis/prerenal AKI/pressors/hypotension: 1 point
        if prerenal_aki_sepsis == "no":
            score += 1
        
        # No exposure to nephrotoxic medications: 1 point
        if nephrotoxic_exposure == "no":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Calculated Licurse Score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 2:
            risk_data = self.risk_data["low_risk"]
            return {
                "stage": "Low Risk",
                "stage_description": "Low risk for hydronephrosis",
                "interpretation": f"Licurse Score: {score} points. Risk category: Low Risk. "
                                f"Low risk group with {risk_data['hydronephrosis_risk']}% risk of hydronephrosis "
                                f"and {risk_data['intervention_risk']}% risk of urological intervention. "
                                f"Renal ultrasound may be deferred until other diagnostic studies prove "
                                f"unrevealing or there is inadequate response to conservative measures "
                                f"(e.g., volume expansion). The number needed to screen (NNS) to find one "
                                f"case of hydronephrosis in this group is 25, representing a cost-effective "
                                f"approach to reduce unnecessary imaging. Consider clinical context, patient "
                                f"preferences, and institutional protocols when making final decisions about "
                                f"renal ultrasound timing."
            }
        elif score == 3:
            risk_data = self.risk_data["medium_risk"]
            return {
                "stage": "Medium Risk",
                "stage_description": "Medium risk for hydronephrosis",
                "interpretation": f"Licurse Score: {score} points. Risk category: Medium Risk. "
                                f"Medium risk group with {risk_data['hydronephrosis_risk']}% risk of hydronephrosis "
                                f"and {risk_data['intervention_risk']}% risk of urological intervention. "
                                f"Consider individual clinical context, patient presentation, and institutional "
                                f"protocols when deciding on renal ultrasound. This intermediate risk group "
                                f"requires individualized decision-making based on clinical judgment, "
                                f"severity of AKI, response to initial treatment, and patient factors. "
                                f"Early ultrasound may be appropriate if clinical suspicion for obstruction "
                                f"remains high or if there is no improvement with conservative management."
            }
        else:  # score > 3
            risk_data = self.risk_data["high_risk"]
            return {
                "stage": "High Risk",
                "stage_description": "High risk for hydronephrosis",
                "interpretation": f"Licurse Score: {score} points. Risk category: High Risk. "
                                f"High risk group with {risk_data['hydronephrosis_risk']}% risk of hydronephrosis "
                                f"and {risk_data['intervention_risk']}% risk of urological intervention. "
                                f"Renal ultrasound is strongly indicated for evaluation of possible "
                                f"urinary tract obstruction. Given the significant risk of hydronephrosis "
                                f"requiring intervention, prompt imaging is recommended to guide appropriate "
                                f"management decisions. Early detection of obstruction can prevent further "
                                f"kidney damage and facilitate timely urological consultation if intervention "
                                f"is needed."
            }
    
    def _get_high_risk_interpretation_with_history(self) -> str:
        """Returns interpretation for patients with history of hydronephrosis"""
        
        return ("Licurse Score: Automatic High Risk assignment due to history of hydronephrosis. "
                "Patients with a prior history of hydronephrosis are automatically classified "
                "as high risk regardless of other clinical factors. Renal ultrasound is strongly "
                "indicated to evaluate for recurrent or persistent hydronephrosis that may be "
                "contributing to the current acute kidney injury. Given the known predisposition "
                "to urinary tract obstruction, prompt imaging is essential for appropriate "
                "management and to prevent further renal deterioration. Consider urgent "
                "urological consultation if significant hydronephrosis is identified on imaging.")


def calculate_licurse_score(
    history_hydronephrosis: str,
    race: str,
    recurrent_utis: str,
    obstruction_diagnosis: str,
    history_chf: str,
    prerenal_aki_sepsis: str,
    nephrotoxic_exposure: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_licurse_score pattern
    """
    calculator = LicurseScoreCalculator()
    return calculator.calculate(
        history_hydronephrosis, race, recurrent_utis, obstruction_diagnosis,
        history_chf, prerenal_aki_sepsis, nephrotoxic_exposure
    )