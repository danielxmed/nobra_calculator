"""
Bishop Score for Vaginal Delivery and Induction of Labor Calculator

Predicts likelihood of successful vaginal delivery and determines favorable cervical 
conditions for labor induction in pregnant women at term. Developed by Dr. Edward 
Bishop in 1964 and remains a cornerstone assessment tool in obstetrics.

References (Vancouver style):
1. Bishop EH. Pelvic scoring for elective induction. Obstet Gynecol. 1964 Aug;24:266-8.
2. Laughon SK, Zhang J, Troendle J, Sun L, Reddy UM. Using a simplified Bishop score 
   to predict vaginal delivery. Obstet Gynecol. 2011 Apr;117(4):805-11.
3. Crane JM. Factors predicting labor induction success: a critical analysis. 
   Clin Obstet Gynecol. 2006 Sep;49(3):573-84.
"""

from typing import Dict, Any


class BishopScoreCalculator:
    """Calculator for Bishop Score for Vaginal Delivery and Induction of Labor"""
    
    def __init__(self):
        # Bishop score component mappings
        self.dilation_scores = {
            "closed": 0,
            "1_2_cm": 1,
            "3_4_cm": 2,
            "5_or_more_cm": 3
        }
        
        self.effacement_scores = {
            "0_30_percent": 0,
            "40_50_percent": 1,
            "60_70_percent": 2,
            "80_or_more_percent": 3
        }
        
        self.station_scores = {
            "minus_3": 0,
            "minus_2": 1,
            "minus_1_or_0": 2,
            "plus_1_or_2": 3
        }
        
        self.position_scores = {
            "posterior": 0,
            "mid_position": 1,
            "anterior": 2
        }
        
        self.consistency_scores = {
            "firm": 0,
            "moderately_firm": 1,
            "soft": 2
        }
        
        # Score interpretation thresholds
        self.UNFAVORABLE_THRESHOLD = 5
        self.INDETERMINATE_MIN = 6
        self.INDETERMINATE_MAX = 7
        self.FAVORABLE_THRESHOLD = 8
    
    def calculate(self, cervical_dilation: str, cervical_effacement: str,
                 fetal_station: str, cervical_position: str, 
                 cervical_consistency: str) -> Dict[str, Any]:
        """
        Calculates Bishop score for predicting vaginal delivery success
        
        Args:
            cervical_dilation (str): Cervical dilation category
            cervical_effacement (str): Cervical effacement percentage category
            fetal_station (str): Fetal station relative to ischial spines
            cervical_position (str): Position of cervix
            cervical_consistency (str): Consistency/firmness of cervix
            
        Returns:
            Dict with Bishop score, interpretation, and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(cervical_dilation, cervical_effacement, fetal_station,
                            cervical_position, cervical_consistency)
        
        # Calculate individual component scores
        dilation_score = self.dilation_scores[cervical_dilation]
        effacement_score = self.effacement_scores[cervical_effacement]
        station_score = self.station_scores[fetal_station]
        position_score = self.position_scores[cervical_position]
        consistency_score = self.consistency_scores[cervical_consistency]
        
        # Calculate total Bishop score
        total_score = (dilation_score + effacement_score + station_score + 
                      position_score + consistency_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, cervical_dilation, cervical_effacement, fetal_station,
                        cervical_position, cervical_consistency):
        """Validates input parameters"""
        
        # Validate cervical dilation
        if cervical_dilation not in self.dilation_scores:
            raise ValueError(f"cervical_dilation must be one of: {list(self.dilation_scores.keys())}")
        
        # Validate cervical effacement
        if cervical_effacement not in self.effacement_scores:
            raise ValueError(f"cervical_effacement must be one of: {list(self.effacement_scores.keys())}")
        
        # Validate fetal station
        if fetal_station not in self.station_scores:
            raise ValueError(f"fetal_station must be one of: {list(self.station_scores.keys())}")
        
        # Validate cervical position
        if cervical_position not in self.position_scores:
            raise ValueError(f"cervical_position must be one of: {list(self.position_scores.keys())}")
        
        # Validate cervical consistency
        if cervical_consistency not in self.consistency_scores:
            raise ValueError(f"cervical_consistency must be one of: {list(self.consistency_scores.keys())}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Bishop score
        
        Args:
            score (int): Total Bishop score (0-13)
            
        Returns:
            Dict with interpretation, stage, and description
        """
        
        if score <= self.UNFAVORABLE_THRESHOLD:
            return {
                "stage": "Unfavorable Cervix",
                "description": "Scores ≤5 suggest unfavorable cervix",
                "interpretation": "Unfavorable cervix with low likelihood of successful vaginal delivery. Labor induction may be necessary and cervical ripening agents should be considered before induction. Higher risk of cesarean delivery."
            }
        elif self.INDETERMINATE_MIN <= score <= self.INDETERMINATE_MAX:
            return {
                "stage": "Indeterminate",
                "description": "Scores 6-7 are indeterminate for induction success",
                "interpretation": "Intermediate cervical favorability. Success of labor induction is uncertain. Clinical judgment should guide decision-making regarding timing and method of delivery. Consider individual patient factors and circumstances."
            }
        else:  # score >= 8
            return {
                "stage": "Favorable Cervix",
                "description": "Scores ≥8 suggest favorable cervix",
                "interpretation": "Favorable cervix with high likelihood of successful vaginal delivery. Spontaneous labor likely to occur soon or labor induction has good chance of success. Low risk of cesarean delivery."
            }


def calculate_bishop_score(cervical_dilation: str, cervical_effacement: str,
                          fetal_station: str, cervical_position: str, 
                          cervical_consistency: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates Bishop score for predicting successful vaginal delivery and 
    determining favorable cervical conditions for labor induction. The score 
    evaluates five cervical and fetal factors: dilation, effacement, station, 
    position, and consistency. Developed by Dr. Edward Bishop in 1964.
    """
    calculator = BishopScoreCalculator()
    return calculator.calculate(cervical_dilation, cervical_effacement, fetal_station,
                               cervical_position, cervical_consistency)