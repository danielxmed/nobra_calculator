"""
Modified Bishop Score for Vaginal Delivery and Induction of Labor Calculator

Predicts likelihood of successful vaginal delivery with additional parameters 
to the original Bishop score, using simplified cervical assessment criteria.

References:
1. Bishop EH. Obstet Gynecol. 1964;24:266-8.
2. Laughon SK, et al. Obstet Gynecol. 2011;117(4):805-11.
3. Kolkman DG, et al. Am J Perinatol. 2013;30(8):625-30.
"""

from typing import Dict, Any


class ModifiedBishopScoreCalculator:
    """Calculator for Modified Bishop Score for Vaginal Delivery and Induction of Labor"""
    
    def __init__(self):
        # Scoring system for Modified Bishop Score
        self.DILATION_SCORES = {
            "closed": 0,
            "1_2_cm": 2,
            "3_4_cm": 4,
            "greater_than_4_cm": 6
        }
        
        self.LENGTH_SCORES = {
            "3_cm": 0,
            "2_cm": 1,
            "1_cm": 2,
            "0_cm": 3
        }
        
        self.STATION_SCORES = {
            "minus_3": 0,
            "minus_2": 1,
            "minus_1_or_0": 2,
            "plus_1_or_2": 3
        }
        
        self.POSITION_SCORES = {
            "posterior": 0,
            "mid_position": 1,
            "anterior": 2
        }
        
        self.CONSISTENCY_SCORES = {
            "firm": 0,
            "medium": 1,
            "soft": 2
        }
    
    def calculate(self, cervical_dilation: str, cervical_length: str, fetal_station: str,
                  cervical_position: str, cervical_consistency: str, prior_vaginal_deliveries: str,
                  preeclampsia: str, postdate_pregnancy: str, nulliparity: str, 
                  pprom: str) -> Dict[str, Any]:
        """
        Calculates the Modified Bishop Score
        
        Args:
            cervical_dilation (str): Cervical dilation category
            cervical_length (str): Cervical length category
            fetal_station (str): Fetal station relative to ischial spines
            cervical_position (str): Position of cervix
            cervical_consistency (str): Consistency of cervix
            prior_vaginal_deliveries (str): History of prior vaginal deliveries
            preeclampsia (str): Presence of pre-eclampsia
            postdate_pregnancy (str): Postdate pregnancy status
            nulliparity (str): Nulliparous status
            pprom (str): PPROM status
            
        Returns:
            Dict with Modified Bishop Score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(cervical_dilation, cervical_length, fetal_station,
                            cervical_position, cervical_consistency, prior_vaginal_deliveries,
                            preeclampsia, postdate_pregnancy, nulliparity, pprom)
        
        # Calculate base Bishop score components
        base_score = self._calculate_base_score(cervical_dilation, cervical_length, fetal_station,
                                              cervical_position, cervical_consistency)
        
        # Calculate modifier points
        modifier_score = self._calculate_modifiers(prior_vaginal_deliveries, preeclampsia,
                                                 postdate_pregnancy, nulliparity, pprom)
        
        # Total score
        total_score = base_score + modifier_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, cervical_dilation: str, cervical_length: str, fetal_station: str,
                        cervical_position: str, cervical_consistency: str, 
                        prior_vaginal_deliveries: str, preeclampsia: str, postdate_pregnancy: str,
                        nulliparity: str, pprom: str):
        """Validates input parameters"""
        
        # Validate categorical parameters
        valid_dilations = ["closed", "1_2_cm", "3_4_cm", "greater_than_4_cm"]
        valid_lengths = ["3_cm", "2_cm", "1_cm", "0_cm"]
        valid_stations = ["minus_3", "minus_2", "minus_1_or_0", "plus_1_or_2"]
        valid_positions = ["posterior", "mid_position", "anterior"]
        valid_consistencies = ["firm", "medium", "soft"]
        valid_yes_no = ["yes", "no"]
        
        if cervical_dilation not in valid_dilations:
            raise ValueError(f"cervical_dilation must be one of: {', '.join(valid_dilations)}")
        if cervical_length not in valid_lengths:
            raise ValueError(f"cervical_length must be one of: {', '.join(valid_lengths)}")
        if fetal_station not in valid_stations:
            raise ValueError(f"fetal_station must be one of: {', '.join(valid_stations)}")
        if cervical_position not in valid_positions:
            raise ValueError(f"cervical_position must be one of: {', '.join(valid_positions)}")
        if cervical_consistency not in valid_consistencies:
            raise ValueError(f"cervical_consistency must be one of: {', '.join(valid_consistencies)}")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("prior_vaginal_deliveries", prior_vaginal_deliveries),
            ("preeclampsia", preeclampsia),
            ("postdate_pregnancy", postdate_pregnancy),
            ("nulliparity", nulliparity),
            ("pprom", pprom)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_base_score(self, cervical_dilation: str, cervical_length: str, 
                            fetal_station: str, cervical_position: str, 
                            cervical_consistency: str) -> int:
        """Calculates base Bishop score from cervical parameters"""
        
        score = 0
        score += self.DILATION_SCORES[cervical_dilation]
        score += self.LENGTH_SCORES[cervical_length]
        score += self.STATION_SCORES[fetal_station]
        score += self.POSITION_SCORES[cervical_position]
        score += self.CONSISTENCY_SCORES[cervical_consistency]
        
        return score
    
    def _calculate_modifiers(self, prior_vaginal_deliveries: str, preeclampsia: str,
                           postdate_pregnancy: str, nulliparity: str, pprom: str) -> int:
        """Calculates modifier points from clinical factors"""
        
        modifier_score = 0
        
        # Prior vaginal deliveries adds points
        if prior_vaginal_deliveries == "yes":
            modifier_score += 1
        
        # Pre-eclampsia adds points
        if preeclampsia == "yes":
            modifier_score += 1
        
        # Postdate pregnancy adds points
        if postdate_pregnancy == "yes":
            modifier_score += 1
        
        # Nulliparity subtracts points (makes induction less likely to succeed)
        if nulliparity == "yes":
            modifier_score -= 1
        
        # PPROM adds points
        if pprom == "yes":
            modifier_score += 1
        
        return modifier_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Modified Bishop Score
        
        Args:
            score: Modified Bishop Score (typically 0-20)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 5:
            return {
                "stage": "Unfavorable",
                "description": "Unfavorable cervix",
                "interpretation": (f"Modified Bishop Score of {score} indicates an unfavorable cervix. "
                                 "Low likelihood of successful vaginal delivery. Consider cervical "
                                 "ripening agents (prostaglandins, mechanical methods) before induction "
                                 "of labor. Higher risk of failed induction and cesarean delivery. "
                                 "Discuss risks and benefits with patient.")
            }
        elif 6 <= score <= 7:
            return {
                "stage": "Intermediate",
                "description": "Intermediate favorability",
                "interpretation": (f"Modified Bishop Score of {score} indicates intermediate cervical "
                                 "favorability. Uncertain prediction for successful vaginal delivery. "
                                 "Clinical judgment required based on individual patient factors, "
                                 "obstetric history, and indication for delivery. Consider cervical "
                                 "ripening if time permits.")
            }
        else:  # score >= 8
            return {
                "stage": "Favorable",
                "description": "Favorable cervix",
                "interpretation": (f"Modified Bishop Score of {score} indicates a favorable cervix. "
                                 "High likelihood of successful vaginal delivery. Induction of labor "
                                 "likely to be successful without need for cervical ripening. "
                                 "Consider proceeding with induction using oxytocin or amniotomy "
                                 "as appropriate.")
            }


def calculate_modified_bishop_score(cervical_dilation: str, cervical_length: str,
                                  fetal_station: str, cervical_position: str,
                                  cervical_consistency: str, prior_vaginal_deliveries: str,
                                  preeclampsia: str, postdate_pregnancy: str,
                                  nulliparity: str, pprom: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedBishopScoreCalculator()
    return calculator.calculate(cervical_dilation, cervical_length, fetal_station,
                              cervical_position, cervical_consistency, prior_vaginal_deliveries,
                              preeclampsia, postdate_pregnancy, nulliparity, pprom)