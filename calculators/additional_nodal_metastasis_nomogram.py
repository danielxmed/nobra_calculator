"""
Additional Nodal Metastasis Nomogram Calculator

Predicts probability of additional non-sentinel lymph node metastases in breast cancer 
patients with a positive sentinel node biopsy.

References:
- Van Zee KJ, Manasseh DM, Bevilacqua JL, et al. A nomogram for predicting the likelihood 
  of additional nodal metastases in breast cancer patients with a positive sentinel node 
  biopsy. Ann Surg Oncol. 2003 Dec;10(10):1140-51.
"""

import math
from typing import Dict, Any


class AdditionalNodalMetastasisNomogramCalculator:
    """Calculator for Additional Nodal Metastasis Nomogram"""
    
    def __init__(self):
        # Coefficient values based on the original nomogram
        self.INTERCEPT = -1.5
        
        # Nuclear grade coefficients
        self.NUCLEAR_GRADE_SCORES = {
            "ductal_i": 0,
            "ductal_ii": 1,
            "ductal_iii": 10,
            "lobular": 6
        }
        
        # Other parameter coefficients
        self.LVI_SCORE = 22
        self.MULTIFOCAL_SCORE = 15
        self.ER_POSITIVE_SCORE = 17
        
        # Detection method coefficients
        self.DETECTION_METHOD_SCORES = {
            "ihc": 0,
            "serial_he": 23,
            "routine": 35,
            "frozen": 81
        }
    
    def calculate(self, nuclear_grade: str, lymphovascular_invasion: str, 
                 multifocal: str, estrogen_receptor_status: str, negative_slns: int,
                 positive_slns: int, pathologic_size: float, detection_method: str) -> Dict[str, Any]:
        """
        Calculates the probability of additional non-sentinel lymph node metastases
        
        Args:
            nuclear_grade: Nuclear grade and tumor type (ductal_i, ductal_ii, ductal_iii, lobular)
            lymphovascular_invasion: Lymphovascular invasion present (no, yes)
            multifocal: Multifocal tumor (no, yes)
            estrogen_receptor_status: ER status (negative, positive)
            negative_slns: Number of negative sentinel lymph nodes (0-14)
            positive_slns: Number of positive sentinel lymph nodes (0-7)
            pathologic_size: Pathologic tumor size in cm (0-9)
            detection_method: Method of SLN metastasis detection (ihc, serial_he, routine, frozen)
            
        Returns:
            Dict with the probability and interpretation
        """
        
        # Validations
        self._validate_inputs(nuclear_grade, lymphovascular_invasion, multifocal, 
                            estrogen_receptor_status, negative_slns, positive_slns,
                            pathologic_size, detection_method)
        
        # Calculate linear predictor
        linear_predictor = self._calculate_linear_predictor(
            nuclear_grade, lymphovascular_invasion, multifocal, 
            estrogen_receptor_status, negative_slns, positive_slns,
            pathologic_size, detection_method
        )
        
        # Convert to probability using logistic function
        probability = self._calculate_probability(linear_predictor)
        
        # Get interpretation
        interpretation = self._get_interpretation(probability)
        
        return {
            "result": probability,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, nuclear_grade, lymphovascular_invasion, multifocal,
                        estrogen_receptor_status, negative_slns, positive_slns,
                        pathologic_size, detection_method):
        """Validates input parameters"""
        
        # Validate nuclear grade
        if nuclear_grade not in self.NUCLEAR_GRADE_SCORES:
            raise ValueError("Nuclear grade must be one of: ductal_i, ductal_ii, ductal_iii, lobular")
        
        # Validate yes/no parameters
        if lymphovascular_invasion not in ["no", "yes"]:
            raise ValueError("Lymphovascular invasion must be 'no' or 'yes'")
        
        if multifocal not in ["no", "yes"]:
            raise ValueError("Multifocal must be 'no' or 'yes'")
        
        if estrogen_receptor_status not in ["negative", "positive"]:
            raise ValueError("Estrogen receptor status must be 'negative' or 'positive'")
        
        # Validate numeric ranges
        if not isinstance(negative_slns, int) or negative_slns < 0 or negative_slns > 14:
            raise ValueError("Number of negative SLNs must be an integer between 0 and 14")
        
        if not isinstance(positive_slns, int) or positive_slns < 0 or positive_slns > 7:
            raise ValueError("Number of positive SLNs must be an integer between 0 and 7")
        
        if positive_slns == 0:
            raise ValueError("Number of positive SLNs must be at least 1 for this nomogram")
        
        if pathologic_size < 0 or pathologic_size > 9:
            raise ValueError("Pathologic size must be between 0 and 9 cm")
        
        # Validate detection method
        if detection_method not in self.DETECTION_METHOD_SCORES:
            raise ValueError("Detection method must be one of: ihc, serial_he, routine, frozen")
    
    def _calculate_linear_predictor(self, nuclear_grade, lymphovascular_invasion, 
                                   multifocal, estrogen_receptor_status, negative_slns,
                                   positive_slns, pathologic_size, detection_method):
        """Calculates the linear predictor for the nomogram"""
        
        # Start with intercept
        predictor = self.INTERCEPT
        
        # Add nuclear grade score
        predictor += self.NUCLEAR_GRADE_SCORES[nuclear_grade]
        
        # Add LVI score
        if lymphovascular_invasion == "yes":
            predictor += self.LVI_SCORE
        
        # Add multifocal score
        if multifocal == "yes":
            predictor += self.MULTIFOCAL_SCORE
        
        # Add ER status score
        if estrogen_receptor_status == "positive":
            predictor += self.ER_POSITIVE_SCORE
        
        # Add continuous variables (coefficients estimated from nomogram)
        predictor += negative_slns * (-2.5)  # Negative SLNs reduce risk
        predictor += positive_slns * 12      # Positive SLNs increase risk
        predictor += pathologic_size * 8     # Larger size increases risk
        
        # Add detection method score
        predictor += self.DETECTION_METHOD_SCORES[detection_method]
        
        # Scale the predictor to match probability range
        predictor = predictor / 100
        
        return predictor
    
    def _calculate_probability(self, linear_predictor):
        """Converts linear predictor to probability using logistic function"""
        
        try:
            # Logistic function: p = exp(x) / (1 + exp(x))
            exp_predictor = math.exp(linear_predictor)
            probability = exp_predictor / (1 + exp_predictor)
            
            # Convert to percentage and round
            probability_percent = round(probability * 100, 1)
            
            # Ensure probability is within reasonable bounds
            probability_percent = max(0.1, min(99.9, probability_percent))
            
            return probability_percent
            
        except OverflowError:
            # Handle extreme values
            if linear_predictor > 0:
                return 99.9
            else:
                return 0.1
    
    def _get_interpretation(self, probability: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the probability
        
        Args:
            probability: Calculated probability percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if probability < 10:
            return {
                "stage": "Very Low Risk",
                "description": "Very low probability",
                "interpretation": "Very low probability (<10%) of additional non-sentinel lymph node metastases. Consider omitting completion axillary lymph node dissection."
            }
        elif probability < 20:
            return {
                "stage": "Low Risk",
                "description": "Low probability", 
                "interpretation": "Low probability (10-20%) of additional non-sentinel lymph node metastases. Clinical decision-making should incorporate patient factors and preferences."
            }
        elif probability < 50:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate probability",
                "interpretation": "Moderate probability (20-50%) of additional non-sentinel lymph node metastases. Consider completion axillary lymph node dissection or axillary radiation therapy."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High probability",
                "interpretation": "High probability (>50%) of additional non-sentinel lymph node metastases. Strong consideration for completion axillary lymph node dissection or axillary radiation therapy."
            }


def calculate_additional_nodal_metastasis_nomogram(nuclear_grade, lymphovascular_invasion,
                                                  multifocal, estrogen_receptor_status,
                                                  negative_slns, positive_slns, 
                                                  pathologic_size, detection_method) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AdditionalNodalMetastasisNomogramCalculator()
    return calculator.calculate(nuclear_grade, lymphovascular_invasion, multifocal,
                              estrogen_receptor_status, negative_slns, positive_slns,
                              pathologic_size, detection_method)