"""
G8 Geriatric Screening Tool Calculator

Identifies older cancer patients who could benefit from comprehensive geriatric assessment (CGA).

References:
1. Bellera CA, Rainfray M, Mathoulin-Pélissier S, et al. Screening older cancer patients: 
   first evaluation of the G-8 geriatric screening tool. Ann Oncol. 2012;23(8):2166-72. 
   doi: 10.1093/annonc/mdr587.
2. Soubeyran P, Bellera C, Goyard J, et al. Screening for vulnerability in older cancer 
   patients: the ONCODAGE Prospective Multicenter Cohort Study. PLoS One. 
   2014;9(12):e115060. doi: 10.1371/journal.pone.0115060.
3. Kenis C, Decoster L, Van Puyvelde K, et al. Performance of two geriatric screening 
   tools in older patients with cancer. J Clin Oncol. 2014;32(1):19-26. 
   doi: 10.1200/JCO.2013.51.1345.
"""

from typing import Dict, Any


class G8GeriatricScreeningToolCalculator:
    """Calculator for G8 Geriatric Screening Tool"""
    
    def __init__(self):
        # G8 scoring system
        self.AGE_POINTS = {
            "over_85": 0,
            "80_to_85": 1,
            "under_80": 2
        }
        
        self.FOOD_INTAKE_POINTS = {
            "severe_decrease": 0,
            "moderate_decrease": 1,
            "no_decrease": 2
        }
        
        self.WEIGHT_LOSS_POINTS = {
            "over_3kg": 0,
            "does_not_know": 1,
            "1_to_3kg": 2,
            "no_weight_loss": 3
        }
        
        self.MOBILITY_POINTS = {
            "bed_chair_bound": 0,
            "out_of_bed_no_outside": 1,
            "goes_out": 2
        }
        
        self.NEUROPSYCH_POINTS = {
            "severe_dementia_depression": 0,
            "mild_dementia": 1,
            "no_psychological_conditions": 2
        }
        
        self.BMI_POINTS = {
            "under_19": 0,
            "19_to_21": 1,
            "21_to_23": 2,
            "23_or_over": 3
        }
        
        self.MEDICATION_POINTS = {
            "yes": 0,
            "no": 1
        }
        
        self.HEALTH_STATUS_POINTS = {
            "not_as_good": 0,
            "does_not_know": 0.5,
            "as_good": 1,
            "better": 2
        }
    
    def calculate(self, age_category: str, food_intake_decline: str, weight_loss: str,
                  mobility: str, neuropsychological_conditions: str, bmi_category: str,
                  multiple_medications: str, health_status_vs_peers: str) -> Dict[str, Any]:
        """
        Calculates G8 Geriatric Screening Tool score
        
        Args:
            age_category (str): Patient age category (over_85, 80_to_85, under_80)
            food_intake_decline (str): Food intake decline over past 3 months
            weight_loss (str): Weight loss during last 3 months
            mobility (str): Patient mobility status
            neuropsychological_conditions (str): Neuropsychological conditions
            bmi_category (str): Body Mass Index category
            multiple_medications (str): Takes >3 prescription drugs per day (yes/no)
            health_status_vs_peers (str): Health status compared to peers
            
        Returns:
            Dict with G8 score and interpretation
        """
        
        # Validations
        self._validate_inputs(
            age_category, food_intake_decline, weight_loss, mobility,
            neuropsychological_conditions, bmi_category, multiple_medications,
            health_status_vs_peers
        )
        
        # Calculate total score
        total_score = self._calculate_total_score(
            age_category, food_intake_decline, weight_loss, mobility,
            neuropsychological_conditions, bmi_category, multiple_medications,
            health_status_vs_peers
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, food_intake_decline: str, weight_loss: str,
                        mobility: str, neuropsychological_conditions: str, bmi_category: str,
                        multiple_medications: str, health_status_vs_peers: str):
        """Validates input parameters"""
        
        if age_category not in self.AGE_POINTS:
            raise ValueError(f"Invalid age_category: {age_category}")
        
        if food_intake_decline not in self.FOOD_INTAKE_POINTS:
            raise ValueError(f"Invalid food_intake_decline: {food_intake_decline}")
        
        if weight_loss not in self.WEIGHT_LOSS_POINTS:
            raise ValueError(f"Invalid weight_loss: {weight_loss}")
        
        if mobility not in self.MOBILITY_POINTS:
            raise ValueError(f"Invalid mobility: {mobility}")
        
        if neuropsychological_conditions not in self.NEUROPSYCH_POINTS:
            raise ValueError(f"Invalid neuropsychological_conditions: {neuropsychological_conditions}")
        
        if bmi_category not in self.BMI_POINTS:
            raise ValueError(f"Invalid bmi_category: {bmi_category}")
        
        if multiple_medications not in self.MEDICATION_POINTS:
            raise ValueError(f"Invalid multiple_medications: {multiple_medications}")
        
        if health_status_vs_peers not in self.HEALTH_STATUS_POINTS:
            raise ValueError(f"Invalid health_status_vs_peers: {health_status_vs_peers}")
    
    def _calculate_total_score(self, age_category: str, food_intake_decline: str, weight_loss: str,
                              mobility: str, neuropsychological_conditions: str, bmi_category: str,
                              multiple_medications: str, health_status_vs_peers: str) -> float:
        """Calculates the total G8 score"""
        
        total_score = (
            self.AGE_POINTS[age_category] +
            self.FOOD_INTAKE_POINTS[food_intake_decline] +
            self.WEIGHT_LOSS_POINTS[weight_loss] +
            self.MOBILITY_POINTS[mobility] +
            self.NEUROPSYCH_POINTS[neuropsychological_conditions] +
            self.BMI_POINTS[bmi_category] +
            self.MEDICATION_POINTS[multiple_medications] +
            self.HEALTH_STATUS_POINTS[health_status_vs_peers]
        )
        
        return round(total_score, 1)
    
    def _get_interpretation(self, total_score: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on G8 score
        
        Args:
            total_score (float): Total G8 score (0-17)
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 14:
            return {
                "stage": "High Risk",
                "description": "Requires comprehensive geriatric assessment",
                "interpretation": (f"G8 score of {total_score} indicates high risk for geriatric impairment. "
                                f"A comprehensive geriatric assessment (CGA) by trained geriatric professionals is "
                                f"strongly recommended to evaluate functional status, comorbidities, cognition, mental health, "
                                f"social support, nutrition, and geriatric syndromes. This assessment will help guide appropriate "
                                f"cancer treatment decisions and identify opportunities for interventions to optimize patient "
                                f"outcomes. The CGA should be performed before initiating cancer treatment when possible to "
                                f"inform treatment planning and supportive care needs.")
            }
        else:
            return {
                "stage": "Low Risk",
                "description": "Low risk for geriatric impairment",
                "interpretation": (f"G8 score of {total_score} indicates low risk for significant geriatric impairment. "
                                f"While a full comprehensive geriatric assessment may not be immediately necessary, continued "
                                f"monitoring during cancer treatment is appropriate. Consider reassessment if clinical status "
                                f"changes, treatment-related complications arise, or functional decline is observed. Standard "
                                f"oncological care may proceed with routine age-appropriate considerations including attention "
                                f"to polypharmacy, functional status, and treatment tolerability.")
            }


def calculate_g8_geriatric_screening_tool(age_category: str, food_intake_decline: str, weight_loss: str,
                                        mobility: str, neuropsychological_conditions: str, bmi_category: str,
                                        multiple_medications: str, health_status_vs_peers: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_g8_geriatric_screening_tool pattern
    """
    calculator = G8GeriatricScreeningToolCalculator()
    return calculator.calculate(
        age_category, food_intake_decline, weight_loss, mobility,
        neuropsychological_conditions, bmi_category, multiple_medications,
        health_status_vs_peers
    )