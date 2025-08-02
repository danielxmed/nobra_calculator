"""
Metroticket Calculator for Hepatocellular Carcinoma (HCC) Survival

Predicts 3 and 5-year survival after liver transplantation for HCC patients,
especially those beyond Milan criteria.

References:
1. Mazzaferro V, et al. Lancet Oncol. 2009;10(1):35-43.
2. Mazzaferro V, et al. Gastroenterology. 2018;154(1):128-139.
3. Lei JY, et al. World J Gastroenterol. 2013;19(44):8093-8.
"""

from typing import Dict, Any


class MetroticketHccCalculator:
    """Calculator for Metroticket HCC Survival Prediction"""
    
    def __init__(self):
        # Up-to-Seven threshold
        self.UP_TO_SEVEN_THRESHOLD = 7
        
        # Survival rates based on the Metroticket model
        # These are approximations based on the published survival curves
        self.SURVIVAL_MATRIX = {
            # Format: (max_sum, vascular_invasion) -> (3yr%, 5yr%)
            (4, False): (85, 75),     # Sum ≤4, no VI
            (5, False): (80, 70),     # Sum 5, no VI
            (6, False): (77, 68),     # Sum 6, no VI
            (7, False): (75, 65),     # Sum 7, no VI (up-to-seven boundary)
            (8, False): (70, 60),     # Sum 8, no VI
            (9, False): (65, 55),     # Sum 9, no VI
            (10, False): (60, 50),    # Sum 10, no VI
            (11, False): (55, 45),    # Sum 11, no VI
            (12, False): (50, 40),    # Sum 12, no VI
            (999, False): (45, 35),   # Sum >12, no VI
            
            # With vascular invasion - significantly worse prognosis
            (4, True): (60, 45),      # Sum ≤4, with VI
            (7, True): (50, 35),      # Sum ≤7, with VI
            (10, True): (40, 25),     # Sum ≤10, with VI
            (999, True): (30, 20),    # Sum >10, with VI
            
            # Unknown vascular invasion - intermediate prognosis
            (4, None): (72, 60),      # Sum ≤4, VI unknown
            (7, None): (65, 50),      # Sum ≤7, VI unknown
            (10, None): (55, 40),     # Sum ≤10, VI unknown
            (999, None): (40, 30),    # Sum >10, VI unknown
        }
    
    def calculate(self, largest_nodule_size: int, number_of_nodules: int,
                  vascular_invasion: str) -> Dict[str, Any]:
        """
        Calculates the Metroticket survival prediction for HCC patients
        
        Args:
            largest_nodule_size (int): Size of largest tumor in mm
            number_of_nodules (int): Number of tumor nodules
            vascular_invasion (str): "unknown", "absent", or "present"
            
        Returns:
            Dict with survival predictions and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(largest_nodule_size, number_of_nodules, vascular_invasion)
        
        # Convert size from mm to cm for the up-to-seven calculation
        largest_nodule_size_cm = largest_nodule_size / 10.0
        
        # Calculate the sum for up-to-seven criteria
        sum_score = largest_nodule_size_cm + number_of_nodules
        
        # Map vascular invasion status
        vi_map = {
            "unknown": None,
            "absent": False,
            "present": True
        }
        vi_status = vi_map[vascular_invasion]
        
        # Get survival rates
        survival_3yr, survival_5yr = self._get_survival_rates(sum_score, vi_status)
        
        # Determine if within up-to-seven criteria
        within_up_to_seven = (sum_score <= self.UP_TO_SEVEN_THRESHOLD and 
                             vascular_invasion != "present")
        
        # Get interpretation
        interpretation = self._get_interpretation(sum_score, vi_status, 
                                                 within_up_to_seven, 
                                                 survival_3yr, survival_5yr)
        
        return {
            "result": {
                "sum_score": round(sum_score, 1),
                "within_up_to_seven": within_up_to_seven,
                "survival_3_year": survival_3yr,
                "survival_5_year": survival_5yr
            },
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, largest_nodule_size: int, number_of_nodules: int,
                        vascular_invasion: str):
        """Validates input parameters"""
        
        # Validate largest nodule size
        if not isinstance(largest_nodule_size, int):
            raise ValueError("Largest nodule size must be an integer")
        if largest_nodule_size < 0 or largest_nodule_size > 99:
            raise ValueError(f"Largest nodule size must be between 0 and 99 mm, got {largest_nodule_size}")
        
        # Validate number of nodules
        if not isinstance(number_of_nodules, int):
            raise ValueError("Number of nodules must be an integer")
        if number_of_nodules < 0 or number_of_nodules > 10:
            raise ValueError(f"Number of nodules must be between 0 and 10, got {number_of_nodules}")
        
        # Validate vascular invasion
        valid_options = ["unknown", "absent", "present"]
        if vascular_invasion not in valid_options:
            raise ValueError(f"Vascular invasion must be one of {valid_options}, got '{vascular_invasion}'")
    
    def _get_survival_rates(self, sum_score: float, vi_status: bool) -> tuple:
        """
        Determines survival rates based on sum score and vascular invasion
        
        Args:
            sum_score (float): Sum of tumor size (cm) and number
            vi_status (bool): Vascular invasion status (True/False/None)
            
        Returns:
            Tuple of (3-year survival %, 5-year survival %)
        """
        
        # Find appropriate survival rates from matrix
        for (max_sum, vi), (surv_3yr, surv_5yr) in self.SURVIVAL_MATRIX.items():
            if vi == vi_status and sum_score <= max_sum:
                return surv_3yr, surv_5yr
        
        # Should not reach here due to 999 catch-all, but just in case
        return 30, 20  # Worst case scenario
    
    def _get_interpretation(self, sum_score: float, vi_status: bool,
                           within_up_to_seven: bool, survival_3yr: int,
                           survival_5yr: int) -> Dict[str, str]:
        """
        Generates interpretation based on calculated values
        
        Args:
            sum_score (float): Sum of tumor size (cm) and number
            vi_status (bool): Vascular invasion status
            within_up_to_seven (bool): Whether within up-to-seven criteria
            survival_3yr (int): 3-year survival percentage
            survival_5yr (int): 5-year survival percentage
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if within_up_to_seven:
            stage = "Within Up-to-Seven Criteria"
            description = f"Sum = {sum_score:.1f} (≤7), no vascular invasion"
            interpretation = (
                f"Excellent prognosis with predicted 3-year survival of {survival_3yr}% "
                f"and 5-year survival of {survival_5yr}%. These patients have outcomes "
                "comparable to those within Milan criteria and are good candidates for "
                "liver transplantation."
            )
        elif vi_status:
            stage = "Vascular Invasion Present"
            description = f"Sum = {sum_score:.1f}, vascular invasion present"
            interpretation = (
                f"Poor prognosis with predicted 3-year survival of {survival_3yr}% "
                f"and 5-year survival of {survival_5yr}%. Vascular invasion significantly "
                "worsens outcomes. Careful multidisciplinary evaluation needed to determine "
                "transplant candidacy."
            )
        else:
            stage = "Beyond Up-to-Seven Criteria"
            description = f"Sum = {sum_score:.1f} (>7), no vascular invasion"
            interpretation = (
                f"Intermediate prognosis with predicted 3-year survival of {survival_3yr}% "
                f"and 5-year survival of {survival_5yr}%. These patients exceed up-to-seven "
                "criteria but may still be considered for transplantation based on individual "
                "factors and center expertise."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }


def calculate_metroticket_hcc(largest_nodule_size: int, number_of_nodules: int,
                              vascular_invasion: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MetroticketHccCalculator()
    return calculator.calculate(largest_nodule_size, number_of_nodules, vascular_invasion)