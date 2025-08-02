"""
Kt/V for Dialysis Adequacy Calculator

Quantifies adequacy of both hemodialysis and peritoneal dialysis treatment using 
the Daugirdas second-generation equation. This calculator assesses urea clearance 
and overall dialysis effectiveness to help clinicians optimize dialysis prescriptions.

References:
1. Daugirdas JT. Second generation logarithmic estimates of single-pool variable 
   volume Kt/V: an analysis of error. J Am Soc Nephrol. 1993 Nov;4(5):1205-13.
2. National Kidney Foundation. KDOQI Clinical Practice Guidelines for Hemodialysis 
   Adequacy: 2015 update. Am J Kidney Dis. 2015 Nov;66(5):884-930.
"""

import math
from typing import Dict, Any


class KtvDialysisAdequacyCalculator:
    """Calculator for Kt/V Dialysis Adequacy using Daugirdas equation"""
    
    def __init__(self):
        """Initialize adequacy thresholds and parameters"""
        # Hemodialysis adequacy thresholds
        self.hd_minimum_threshold = 1.2
        self.hd_target_threshold = 1.3
        
        # Peritoneal dialysis adequacy threshold (weekly)
        self.pd_target_threshold = 1.7
        
        # Daugirdas equation constants
        self.urea_generation_correction = 0.008  # per hour
        self.volume_correction_factor = 4.0
        self.volume_correction_multiplier = 3.5
    
    def calculate(self, pre_dialysis_bun: float, post_dialysis_bun: float,
                 dialysis_time_hours: float, ultrafiltration_volume: float,
                 post_dialysis_weight: float, dialysis_type: str) -> Dict[str, Any]:
        """
        Calculates Kt/V for dialysis adequacy assessment
        
        Args:
            pre_dialysis_bun (float): Pre-dialysis BUN in mg/dL
            post_dialysis_bun (float): Post-dialysis BUN in mg/dL
            dialysis_time_hours (float): Dialysis session time in hours
            ultrafiltration_volume (float): Ultrafiltration volume in liters
            post_dialysis_weight (float): Post-dialysis weight in kg
            dialysis_type (str): Type of dialysis ("hemodialysis" or "peritoneal_dialysis")
            
        Returns:
            Dict with Kt/V calculation and adequacy assessment
        """
        
        # Validate inputs
        self._validate_inputs(pre_dialysis_bun, post_dialysis_bun, dialysis_time_hours,
                            ultrafiltration_volume, post_dialysis_weight, dialysis_type)
        
        # Calculate BUN reduction ratio (R)
        bun_ratio = post_dialysis_bun / pre_dialysis_bun
        
        # Calculate Kt/V using Daugirdas second-generation equation
        ktv_value = self._calculate_daugirdas_ktv(
            bun_ratio, dialysis_time_hours, ultrafiltration_volume, post_dialysis_weight
        )
        
        # Calculate additional metrics
        urea_reduction_ratio = self._calculate_urr(pre_dialysis_bun, post_dialysis_bun)
        
        # Get adequacy assessment
        adequacy_result = self._assess_adequacy(ktv_value, dialysis_type)
        
        # Create detailed result
        result = {
            "ktv_value": ktv_value,
            "urea_reduction_ratio": urea_reduction_ratio,
            "bun_ratio": bun_ratio,
            "dialysis_type": dialysis_type,
            "adequacy_assessment": adequacy_result,
            "calculation_components": {
                "pre_dialysis_bun": pre_dialysis_bun,
                "post_dialysis_bun": post_dialysis_bun,
                "dialysis_time_hours": dialysis_time_hours,
                "ultrafiltration_volume": ultrafiltration_volume,
                "post_dialysis_weight": post_dialysis_weight,
                "first_term": -math.log(bun_ratio - self.urea_generation_correction * dialysis_time_hours),
                "second_term": (self.volume_correction_factor - self.volume_correction_multiplier * bun_ratio) * (ultrafiltration_volume / post_dialysis_weight)
            },
            "thresholds": self._get_thresholds(dialysis_type)
        }
        
        # Generate interpretation
        interpretation = self._generate_interpretation(ktv_value, dialysis_type, urea_reduction_ratio, adequacy_result)
        
        return {
            "result": result,
            "unit": "dimensionless",
            "interpretation": interpretation,
            "stage": adequacy_result["stage"],
            "stage_description": adequacy_result["description"]
        }
    
    def _validate_inputs(self, pre_dialysis_bun: float, post_dialysis_bun: float,
                        dialysis_time_hours: float, ultrafiltration_volume: float,
                        post_dialysis_weight: float, dialysis_type: str):
        """Validates input parameters"""
        
        if not isinstance(pre_dialysis_bun, (int, float)) or pre_dialysis_bun <= 0:
            raise ValueError("Pre-dialysis BUN must be a positive number")
        
        if not isinstance(post_dialysis_bun, (int, float)) or post_dialysis_bun <= 0:
            raise ValueError("Post-dialysis BUN must be a positive number")
            
        if post_dialysis_bun >= pre_dialysis_bun:
            raise ValueError("Post-dialysis BUN must be lower than pre-dialysis BUN")
        
        if not isinstance(dialysis_time_hours, (int, float)) or dialysis_time_hours <= 0:
            raise ValueError("Dialysis time must be a positive number")
            
        if not isinstance(ultrafiltration_volume, (int, float)) or ultrafiltration_volume < 0:
            raise ValueError("Ultrafiltration volume must be a non-negative number")
            
        if not isinstance(post_dialysis_weight, (int, float)) or post_dialysis_weight <= 0:
            raise ValueError("Post-dialysis weight must be a positive number")
            
        if dialysis_type not in ["hemodialysis", "peritoneal_dialysis"]:
            raise ValueError("Dialysis type must be 'hemodialysis' or 'peritoneal_dialysis'")
        
        # Additional clinical validations
        if pre_dialysis_bun < 5 or pre_dialysis_bun > 200:
            raise ValueError("Pre-dialysis BUN should be between 5-200 mg/dL")
            
        if post_dialysis_bun < 2 or post_dialysis_bun > 150:
            raise ValueError("Post-dialysis BUN should be between 2-150 mg/dL")
            
        if dialysis_time_hours > 24:
            raise ValueError("Dialysis time should not exceed 24 hours")
            
        if post_dialysis_weight < 20 or post_dialysis_weight > 300:
            raise ValueError("Post-dialysis weight should be between 20-300 kg")
    
    def _calculate_daugirdas_ktv(self, bun_ratio: float, dialysis_time_hours: float,
                                ultrafiltration_volume: float, post_dialysis_weight: float) -> float:
        """
        Calculates Kt/V using Daugirdas second-generation equation
        
        Formula: Kt/V = -ln(R - 0.008 × t) + (4 - 3.5 × R) × UF/V
        
        Args:
            bun_ratio (float): Post-BUN/Pre-BUN ratio
            dialysis_time_hours (float): Session time in hours
            ultrafiltration_volume (float): UF volume in liters
            post_dialysis_weight (float): Post-dialysis weight in kg
            
        Returns:
            float: Calculated Kt/V value
        """
        
        # First term: -ln(R - 0.008 × t)
        # Accounts for urea removal during dialysis
        corrected_ratio = bun_ratio - (self.urea_generation_correction * dialysis_time_hours)
        
        # Ensure the argument to ln is positive
        if corrected_ratio <= 0:
            raise ValueError("Invalid BUN ratio or dialysis time leading to negative logarithm argument")
        
        first_term = -math.log(corrected_ratio)
        
        # Second term: (4 - 3.5 × R) × UF/V
        # Accounts for convective clearance from ultrafiltration
        second_term = (self.volume_correction_factor - self.volume_correction_multiplier * bun_ratio) * (ultrafiltration_volume / post_dialysis_weight)
        
        # Total Kt/V
        ktv = first_term + second_term
        
        return round(ktv, 3)
    
    def _calculate_urr(self, pre_bun: float, post_bun: float) -> float:
        """
        Calculates Urea Reduction Ratio (URR)
        
        Formula: URR = ((Pre-BUN - Post-BUN) / Pre-BUN) × 100
        
        Args:
            pre_bun (float): Pre-dialysis BUN
            post_bun (float): Post-dialysis BUN
            
        Returns:
            float: URR percentage
        """
        
        urr = ((pre_bun - post_bun) / pre_bun) * 100
        return round(urr, 1)
    
    def _assess_adequacy(self, ktv_value: float, dialysis_type: str) -> Dict[str, str]:
        """
        Assesses dialysis adequacy based on Kt/V value and dialysis type
        
        Args:
            ktv_value (float): Calculated Kt/V
            dialysis_type (str): Type of dialysis
            
        Returns:
            Dict with adequacy assessment
        """
        
        if dialysis_type == "hemodialysis":
            if ktv_value < self.hd_minimum_threshold:
                return {
                    "stage": "Inadequate",
                    "description": "Below minimum adequacy threshold",
                    "meets_guidelines": False
                }
            elif ktv_value < self.hd_target_threshold:
                return {
                    "stage": "Minimum Adequate (HD)",
                    "description": "Meets minimum hemodialysis adequacy",
                    "meets_guidelines": True
                }
            else:
                return {
                    "stage": "Target Adequate (HD)",
                    "description": "Meets target hemodialysis adequacy",
                    "meets_guidelines": True
                }
        
        else:  # peritoneal_dialysis
            if ktv_value < self.pd_target_threshold:
                return {
                    "stage": "Inadequate",
                    "description": "Below peritoneal dialysis adequacy threshold",
                    "meets_guidelines": False
                }
            else:
                return {
                    "stage": "Target Adequate (PD)",
                    "description": "Meets peritoneal dialysis adequacy",
                    "meets_guidelines": True
                }
    
    def _get_thresholds(self, dialysis_type: str) -> Dict[str, float]:
        """Returns adequacy thresholds for the dialysis type"""
        
        if dialysis_type == "hemodialysis":
            return {
                "minimum": self.hd_minimum_threshold,
                "target": self.hd_target_threshold
            }
        else:
            return {
                "target": self.pd_target_threshold
            }
    
    def _generate_interpretation(self, ktv_value: float, dialysis_type: str,
                               urr: float, adequacy_result: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            ktv_value (float): Calculated Kt/V
            dialysis_type (str): Type of dialysis
            urr (float): Urea reduction ratio
            adequacy_result (Dict): Adequacy assessment
            
        Returns:
            str: Detailed clinical interpretation
        """
        
        # Base interpretation
        interpretation = f"Kt/V = {ktv_value:.3f} for {dialysis_type.replace('_', ' ')} treatment. "
        interpretation += f"Urea Reduction Ratio (URR) = {urr:.1f}%. "
        
        # Adequacy assessment
        if adequacy_result["meets_guidelines"]:
            interpretation += f"This Kt/V value meets clinical adequacy guidelines. "
        else:
            interpretation += f"This Kt/V value is below recommended adequacy thresholds. "
        
        # Specific recommendations based on dialysis type and adequacy
        if dialysis_type == "hemodialysis":
            if ktv_value < self.hd_minimum_threshold:
                interpretation += (
                    f"KDOQI guidelines recommend minimum Kt/V ≥{self.hd_minimum_threshold} and target ≥{self.hd_target_threshold} "
                    f"for hemodialysis. Consider increasing dialysis time, frequency, or optimizing dialyzer efficiency. "
                    f"URR target is ≥65% (current: {urr:.1f}%). "
                )
            elif ktv_value < self.hd_target_threshold:
                interpretation += (
                    f"Kt/V meets minimum adequacy ({self.hd_minimum_threshold}) but below target ({self.hd_target_threshold}). "
                    f"Consider optimization to achieve target Kt/V for improved outcomes. "
                )
            else:
                interpretation += (
                    f"Kt/V meets KDOQI target guidelines (≥{self.hd_target_threshold}). "
                    f"Adequate dialysis clearance achieved. "
                )
        
        else:  # peritoneal_dialysis
            if ktv_value < self.pd_target_threshold:
                interpretation += (
                    f"ISPD and KDOQI guidelines recommend Kt/V ≥{self.pd_target_threshold}/week for peritoneal dialysis. "
                    f"Consider increasing dwell times, exchange volumes, or daily exchange frequency. "
                    f"Assess residual renal function contribution. "
                )
            else:
                interpretation += (
                    f"Kt/V meets ISPD/KDOQI guidelines (≥{self.pd_target_threshold}/week) for peritoneal dialysis. "
                    f"Adequate clearance achieved. "
                )
        
        # Additional clinical guidance
        interpretation += (
            f"Monitor dialysis adequacy regularly (monthly for hemodialysis, every 4-6 months for peritoneal dialysis). "
            f"Consider patient symptoms, laboratory values, and overall clinical status in addition to Kt/V. "
        )
        
        # Note about formula limitations
        if ktv_value > 1.3:
            interpretation += (
                f"Note: Daugirdas equation may overestimate Kt/V when values exceed 1.3. "
                f"Consider equilibrated Kt/V (eKt/V) for more accurate assessment. "
            )
        
        return interpretation


def calculate_ktv_dialysis_adequacy(pre_dialysis_bun, post_dialysis_bun, dialysis_time_hours,
                                  ultrafiltration_volume, post_dialysis_weight, dialysis_type) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = KtvDialysisAdequacyCalculator()
    return calculator.calculate(pre_dialysis_bun, post_dialysis_bun, dialysis_time_hours,
                              ultrafiltration_volume, post_dialysis_weight, dialysis_type)