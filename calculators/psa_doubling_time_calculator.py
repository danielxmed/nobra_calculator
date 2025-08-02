"""
PSA Doubling Time (PSADT) Calculator

Calculates PSA doubling rate in prostate cancer patients with biochemical recurrence 
after treatment. This prognostic tool correlates with survival and helps guide 
treatment decisions for salvage therapy, imaging studies, and castration-resistant 
disease management.

References:
1. D'Amico AV, Moul JW, Carroll PR, Sun L, Lubeck D, Chen MH. Surrogate end point 
   for prostate cancer-specific mortality after radical prostatectomy or radiation 
   therapy. J Natl Cancer Inst. 2003;95(18):1376-83. doi: 10.1093/jnci/djg043.
2. Freedland SJ, Humphreys EB, Mangold LA, Eisenberger M, Dorey FJ, Walsh PC, et al. 
   Risk of prostate cancer-specific mortality following biochemical recurrence after 
   radical prostatectomy. JAMA. 2005;294(4):433-9. doi: 10.1001/jama.294.4.433.
3. Pound CR, Partin AW, Eisenberger MA, Chan DW, Pearson JD, Walsh PC. Natural 
   history of progression after PSA elevation following radical prostatectomy. 
   JAMA. 1999;281(17):1591-7. doi: 10.1001/jama.281.17.1591.
"""

import math
from typing import Dict, Any, List, Tuple, Optional
from scipy.stats import linregress


class PsaDoublingTimeCalculator:
    """Calculator for PSA Doubling Time (PSADT)"""
    
    def __init__(self):
        # Risk thresholds in months
        self.VERY_HIGH_RISK_THRESHOLD = 3.0
        self.HIGH_RISK_THRESHOLD = 6.0
        self.INTERMEDIATE_RISK_THRESHOLD = 12.0
        self.LOW_RISK_THRESHOLD = 36.0
    
    def calculate(self, psa_1: float, days_1: int, psa_2: float, days_2: int,
                 psa_3: Optional[float] = None, days_3: Optional[int] = None,
                 psa_4: Optional[float] = None, days_4: Optional[int] = None,
                 psa_5: Optional[float] = None, days_5: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates PSA doubling time using linear regression of ln(PSA) vs time
        
        Args:
            psa_1 (float): First PSA measurement in ng/mL
            days_1 (int): Days from baseline for first measurement
            psa_2 (float): Second PSA measurement in ng/mL
            days_2 (int): Days from baseline for second measurement
            psa_3 (float, optional): Third PSA measurement in ng/mL
            days_3 (int, optional): Days from baseline for third measurement
            psa_4 (float, optional): Fourth PSA measurement in ng/mL
            days_4 (int, optional): Days from baseline for fourth measurement
            psa_5 (float, optional): Fifth PSA measurement in ng/mL
            days_5 (int, optional): Days from baseline for fifth measurement
            
        Returns:
            Dict with PSA doubling time and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(psa_1, days_1, psa_2, days_2, psa_3, days_3, 
                            psa_4, days_4, psa_5, days_5)
        
        # Prepare data points
        psa_values, time_points = self._prepare_data(
            psa_1, days_1, psa_2, days_2, psa_3, days_3, 
            psa_4, days_4, psa_5, days_5
        )
        
        # Calculate PSA doubling time
        psadt_months = self._calculate_psadt(psa_values, time_points)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(psadt_months)
        
        return {
            "result": round(psadt_months, 1),
            "unit": "months",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, psa_1: float, days_1: int, psa_2: float, days_2: int,
                        psa_3: Optional[float], days_3: Optional[int],
                        psa_4: Optional[float], days_4: Optional[int],
                        psa_5: Optional[float], days_5: Optional[int]):
        """Validates input parameters"""
        
        # Check required parameters
        if not isinstance(psa_1, (int, float)) or psa_1 <= 0:
            raise ValueError("PSA 1 must be a positive number")
        if not isinstance(days_1, int) or days_1 < 0:
            raise ValueError("Days 1 must be a non-negative integer")
        if not isinstance(psa_2, (int, float)) or psa_2 <= 0:
            raise ValueError("PSA 2 must be a positive number")
        if not isinstance(days_2, int) or days_2 < 0:
            raise ValueError("Days 2 must be a non-negative integer")
            
        # Check that time points are different
        if days_1 == days_2:
            raise ValueError("Time points must be different between measurements")
            
        # Validate optional parameters if provided
        optional_params = [
            (psa_3, days_3, "3"), (psa_4, days_4, "4"), (psa_5, days_5, "5")
        ]
        
        for psa, days, num in optional_params:
            if psa is not None or days is not None:
                if psa is None or days is None:
                    raise ValueError(f"Both PSA {num} and Days {num} must be provided together")
                if not isinstance(psa, (int, float)) or psa <= 0:
                    raise ValueError(f"PSA {num} must be a positive number")
                if not isinstance(days, int) or days < 0:
                    raise ValueError(f"Days {num} must be a non-negative integer")
        
        # Check for PSA progression (all values should be positive and generally increasing)
        psa_values = [psa_1, psa_2]
        time_points = [days_1, days_2]
        
        if psa_3 is not None:
            psa_values.append(psa_3)
            time_points.append(days_3)
        if psa_4 is not None:
            psa_values.append(psa_4)
            time_points.append(days_4)
        if psa_5 is not None:
            psa_values.append(psa_5)
            time_points.append(days_5)
            
        # Check for unique time points
        if len(set(time_points)) != len(time_points):
            raise ValueError("All time points must be unique")
    
    def _prepare_data(self, psa_1: float, days_1: int, psa_2: float, days_2: int,
                     psa_3: Optional[float], days_3: Optional[int],
                     psa_4: Optional[float], days_4: Optional[int],
                     psa_5: Optional[float], days_5: Optional[int]) -> Tuple[List[float], List[float]]:
        """Prepares PSA values and time points for calculation"""
        
        psa_values = [psa_1, psa_2]
        time_points = [days_1, days_2]
        
        # Add optional measurements if provided
        if psa_3 is not None and days_3 is not None:
            psa_values.append(psa_3)
            time_points.append(days_3)
        if psa_4 is not None and days_4 is not None:
            psa_values.append(psa_4)
            time_points.append(days_4)
        if psa_5 is not None and days_5 is not None:
            psa_values.append(psa_5)
            time_points.append(days_5)
        
        # Sort by time points to ensure proper chronological order
        paired_data = list(zip(time_points, psa_values))
        paired_data.sort(key=lambda x: x[0])
        time_points, psa_values = zip(*paired_data)
        
        return list(psa_values), list(time_points)
    
    def _calculate_psadt(self, psa_values: List[float], time_points: List[int]) -> float:
        """
        Calculates PSA doubling time using linear regression
        
        Formula: PSADT = ln(2) / slope
        Where slope is from linear regression of ln(PSA) vs time
        """
        
        # Convert days to months for calculation
        time_months = [days / 30.44 for days in time_points]  # Average days per month
        
        # Take natural log of PSA values
        ln_psa_values = [math.log(psa) for psa in psa_values]
        
        # Perform linear regression: ln(PSA) = slope * time + intercept
        slope, intercept, r_value, p_value, std_err = linregress(time_months, ln_psa_values)
        
        # Calculate PSA doubling time
        if slope <= 0:
            # If slope is negative or zero, PSA is stable or decreasing
            # Return a very large value indicating very slow/no doubling
            return 999.0
        
        # PSADT = ln(2) / slope
        psadt = math.log(2) / slope
        
        # Ensure reasonable bounds
        if psadt < 0:
            return 999.0
        if psadt > 999:
            return 999.0
            
        return psadt
    
    def _get_interpretation(self, psadt_months: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PSA doubling time
        
        Args:
            psadt_months (float): PSA doubling time in months
            
        Returns:
            Dict with clinical interpretation
        """
        
        if psadt_months < self.VERY_HIGH_RISK_THRESHOLD:  # < 3 months
            return {
                "stage": "Very High Risk",
                "description": "Rapid PSA progression",
                "interpretation": "Very rapid PSA doubling indicates aggressive disease with high risk of metastasis and mortality. Urgent treatment consideration required including immediate imaging, salvage therapy evaluation, and consideration of systemic therapy. Close monitoring with monthly PSA levels recommended."
            }
        elif psadt_months < self.HIGH_RISK_THRESHOLD:  # 3-6 months
            return {
                "stage": "High Risk",
                "description": "Fast PSA progression",
                "interpretation": "Rapid PSA doubling associated with increased risk of metastasis and reduced survival. Consider aggressive treatment options including salvage radiation therapy, androgen deprivation therapy, or clinical trial enrollment. Imaging studies recommended to evaluate for metastatic disease."
            }
        elif psadt_months < self.INTERMEDIATE_RISK_THRESHOLD:  # 6-12 months
            return {
                "stage": "Intermediate Risk",
                "description": "Moderate PSA progression",
                "interpretation": "Moderate PSA doubling time indicates intermediate risk for progression requiring close monitoring and treatment consideration. Consider salvage therapy options based on patient factors and preferences. Monitor PSA every 3-6 months with imaging if indicated."
            }
        elif psadt_months < self.LOW_RISK_THRESHOLD:  # 12-36 months
            return {
                "stage": "Low Risk",
                "description": "Slow PSA progression",
                "interpretation": "Slower PSA doubling associated with better prognosis and lower risk of aggressive disease progression. Active surveillance may be appropriate with regular PSA monitoring every 6 months. Consider treatment if doubling time shortens or other concerning factors develop."
            }
        else:  # ≥ 36 months
            return {
                "stage": "Very Low Risk",
                "description": "Very slow PSA progression",
                "interpretation": "Very slow PSA doubling indicates indolent disease with excellent prognosis and low risk of clinically significant progression. Active surveillance is typically appropriate with PSA monitoring every 6-12 months. Treatment may be deferred unless other high-risk features develop."
            }


def calculate_psa_doubling_time_calculator(psa_1: float, days_1: int, psa_2: float, days_2: int,
                                         psa_3: Optional[float] = None, days_3: Optional[int] = None,
                                         psa_4: Optional[float] = None, days_4: Optional[int] = None,
                                         psa_5: Optional[float] = None, days_5: Optional[int] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PsaDoublingTimeCalculator()
    return calculator.calculate(psa_1, days_1, psa_2, days_2, psa_3, days_3, 
                               psa_4, days_4, psa_5, days_5)