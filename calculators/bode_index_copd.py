"""
BODE Index for COPD Survival Calculator

Predicts survival and mortality risk in patients with Chronic Obstructive Pulmonary Disease (COPD).
The BODE Index is a multidimensional grading system that incorporates Body-Mass Index, 
Obstruction (FEV1), Dyspnea (mMRC scale), and Exercise capacity (6-minute walk distance).

References:
1. Celli BR, Cote CG, Marin JM, et al. The body-mass index, airflow obstruction, dyspnea, 
   and exercise capacity index in chronic obstructive pulmonary disease. N Engl J Med. 2004 Mar 4;350(10):1005-12.
2. Ong KC, Earnest A, Lu SJ. A multidimensional grading system (BODE index) as predictor 
   of hospitalization for COPD. Chest. 2005 Dec;128(6):3810-6.
"""

from typing import Dict, Any


class BodeIndexCopdCalculator:
    """Calculator for BODE Index for COPD Survival"""
    
    def __init__(self):
        # Scoring thresholds for each component
        self.FEV1_THRESHOLDS = [
            (65, 0),   # ≥65% = 0 points
            (50, 1),   # 50-64% = 1 point
            (36, 2),   # 36-49% = 2 points
            (0, 3)     # ≤35% = 3 points
        ]
        
        self.WALK_DISTANCE_THRESHOLDS = [
            (350, 0),  # ≥350m = 0 points
            (250, 1),  # 250-349m = 1 point
            (150, 2),  # 150-249m = 2 points
            (0, 3)     # ≤149m = 3 points
        ]
        
        self.MMRC_SCORES = {
            'grade_0_strenuous_only': 0,  # Dyspnea only with strenuous exercise
            'grade_1_walks_slower': 1,    # Walks slower than peers due to dyspnea
            'grade_2_stops_100m': 2,      # Stops for breath after walking 100m
            'grade_3_too_dyspneic': 3     # Too dyspneic to leave house
        }
        
        # BMI threshold (only one threshold at 21)
        self.BMI_THRESHOLD = 21  # >21 = 0 points, ≤21 = 1 point
    
    def calculate(self, fev1_percent_predicted: float, six_minute_walk_distance: int, 
                  mmrc_dyspnea_scale: str, body_mass_index: float) -> Dict[str, Any]:
        """
        Calculates the BODE Index score and survival prediction
        
        Args:
            fev1_percent_predicted (float): FEV1 as percentage of predicted
            six_minute_walk_distance (int): 6-minute walk distance in meters
            mmrc_dyspnea_scale (str): mMRC dyspnea scale grade
            body_mass_index (float): BMI in kg/m²
            
        Returns:
            Dict with BODE score, component scores, and survival interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fev1_percent_predicted, six_minute_walk_distance, 
                             mmrc_dyspnea_scale, body_mass_index)
        
        # Calculate component scores
        fev1_score = self._calculate_fev1_score(fev1_percent_predicted)
        walk_score = self._calculate_walk_score(six_minute_walk_distance)
        dyspnea_score = self._calculate_dyspnea_score(mmrc_dyspnea_scale)
        bmi_score = self._calculate_bmi_score(body_mass_index)
        
        # Calculate total BODE score
        total_score = fev1_score + walk_score + dyspnea_score + bmi_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": self._format_interpretation(total_score, interpretation, 
                                                        fev1_score, walk_score, 
                                                        dyspnea_score, bmi_score),
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fev1_percent_predicted: float, six_minute_walk_distance: int, 
                        mmrc_dyspnea_scale: str, body_mass_index: float):
        """Validates input parameters"""
        
        if not isinstance(fev1_percent_predicted, (int, float)) or fev1_percent_predicted <= 0:
            raise ValueError("FEV1 percentage predicted must be a positive number")
        
        if fev1_percent_predicted < 10 or fev1_percent_predicted > 150:
            raise ValueError("FEV1 percentage predicted must be between 10% and 150%")
        
        if not isinstance(six_minute_walk_distance, (int, float)) or six_minute_walk_distance < 0:
            raise ValueError("6-minute walk distance must be a non-negative number")
        
        if six_minute_walk_distance > 1000:
            raise ValueError("6-minute walk distance must be ≤1000 meters")
        
        if mmrc_dyspnea_scale not in self.MMRC_SCORES:
            valid_grades = list(self.MMRC_SCORES.keys())
            raise ValueError(f"mMRC dyspnea scale must be one of: {valid_grades}")
        
        if not isinstance(body_mass_index, (int, float)) or body_mass_index <= 0:
            raise ValueError("BMI must be a positive number")
        
        if body_mass_index < 10 or body_mass_index > 50:
            raise ValueError("BMI must be between 10 and 50 kg/m²")
    
    def _calculate_fev1_score(self, fev1_percent: float) -> int:
        """
        Calculates FEV1 component score
        
        Args:
            fev1_percent (float): FEV1 as percentage of predicted
            
        Returns:
            int: Points (0-3)
        """
        if fev1_percent >= 65:
            return 0
        elif fev1_percent >= 50:
            return 1
        elif fev1_percent >= 36:
            return 2
        else:  # fev1_percent <= 35
            return 3
    
    def _calculate_walk_score(self, walk_distance: int) -> int:
        """
        Calculates 6-minute walk distance component score
        
        Args:
            walk_distance (int): Distance in meters
            
        Returns:
            int: Points (0-3)
        """
        if walk_distance >= 350:
            return 0
        elif walk_distance >= 250:
            return 1
        elif walk_distance >= 150:
            return 2
        else:  # walk_distance <= 149
            return 3
    
    def _calculate_dyspnea_score(self, mmrc_grade: str) -> int:
        """
        Calculates mMRC dyspnea component score
        
        Args:
            mmrc_grade (str): mMRC dyspnea scale grade
            
        Returns:
            int: Points (0-3)
        """
        return self.MMRC_SCORES[mmrc_grade]
    
    def _calculate_bmi_score(self, bmi: float) -> int:
        """
        Calculates BMI component score
        
        Args:
            bmi (float): Body mass index in kg/m²
            
        Returns:
            int: Points (0-1)
        """
        if bmi > self.BMI_THRESHOLD:
            return 0
        else:
            return 1
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines BODE Index interpretation and survival prediction
        
        Args:
            total_score (int): Total BODE score
            
        Returns:
            Dict with stage, description, interpretation, and survival rate
        """
        
        if total_score <= 2:
            return {
                "stage": "Quartile 1 (Low Risk)",
                "description": "BODE Index 0-2 points",
                "interpretation": "Lowest mortality risk with 80% 4-year survival rate. Patients in this quartile have relatively preserved lung function, exercise capacity, and minimal functional disability. Continue current management and monitor disease progression.",
                "survival_rate": "80%"
            }
        elif total_score <= 4:
            return {
                "stage": "Quartile 2 (Moderate Risk)",
                "description": "BODE Index 3-4 points",
                "interpretation": "Moderate mortality risk with 67% 4-year survival rate. Patients show moderate impairment in multiple domains. Consider intensification of bronchodilator therapy, pulmonary rehabilitation, and regular monitoring.",
                "survival_rate": "67%"
            }
        elif total_score <= 6:
            return {
                "stage": "Quartile 3 (High Risk)",
                "description": "BODE Index 5-6 points",
                "interpretation": "High mortality risk with 57% 4-year survival rate. Significant impairment across multiple domains requiring comprehensive management including optimization of medical therapy, pulmonary rehabilitation, and consideration of oxygen therapy.",
                "survival_rate": "57%"
            }
        else:  # total_score >= 7
            return {
                "stage": "Quartile 4 (Very High Risk)",
                "description": "BODE Index 7-10 points",
                "interpretation": "Very high mortality risk with only 18% 4-year survival rate. Severe disease with marked functional impairment. Requires aggressive management including oxygen therapy, consideration of lung volume reduction surgery or transplantation, and palliative care planning.",
                "survival_rate": "18%"
            }
    
    def _format_interpretation(self, total_score: int, interpretation: Dict[str, str],
                             fev1_score: int, walk_score: int, dyspnea_score: int, 
                             bmi_score: int) -> str:
        """
        Formats comprehensive clinical interpretation
        
        Args:
            total_score (int): Total BODE score
            interpretation (dict): Interpretation details
            fev1_score (int): FEV1 component score
            walk_score (int): Walk distance component score
            dyspnea_score (int): Dyspnea component score
            bmi_score (int): BMI component score
            
        Returns:
            str: Formatted interpretation text
        """
        
        component_breakdown = (
            f"BODE Index: {total_score} points (FEV1: {fev1_score}, 6MWD: {walk_score}, "
            f"mMRC: {dyspnea_score}, BMI: {bmi_score}). "
            f"4-year survival rate: {interpretation['survival_rate']}. "
            f"{interpretation['interpretation']} "
            f"The BODE Index provides more accurate prognosis than FEV1 alone by incorporating "
            f"multiple dimensions of COPD severity including lung function, exercise capacity, "
            f"symptom burden, and nutritional status."
        )
        
        return component_breakdown


def calculate_bode_index_copd(fev1_percent_predicted: float, six_minute_walk_distance: int, 
                             mmrc_dyspnea_scale: str, body_mass_index: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BodeIndexCopdCalculator()
    return calculator.calculate(fev1_percent_predicted, six_minute_walk_distance, 
                               mmrc_dyspnea_scale, body_mass_index)