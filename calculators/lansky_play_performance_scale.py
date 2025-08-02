"""
Lansky Play-Performance Scale for Pediatric Functional Status Calculator

Assesses functional status in pediatric patients (under 16 years) using parent description 
of child's play activity and daily function. Primarily used in pediatric oncology to evaluate 
treatment response, disease progression, and quality of life. The scale provides a standardized 
method for assessing functional capacity in children with chronic illness.

References:
1. Lansky SB, List MA, Lansky LL, Ritter-Sterr C, Miller DR. The measurement of performance 
   in childhood cancer patients. Cancer. 1987 Oct 1;60(7):1651-6.
2. Lansky LL, Cairns NU, Clark GM, Lowman J, Miller L, Trueworthy R. Childhood leukemia: 
   nonrandomized therapy with adriamycin. Cancer. 1975 Jan;35(1):306-17.
"""

from typing import Dict, Any


class LanskyPlayPerformanceScaleCalculator:
    """Calculator for Lansky Play-Performance Scale for Pediatric Functional Status"""
    
    def __init__(self):
        """Initialize performance status categories and thresholds"""
        
        # Valid performance status scores (0-100 in increments of 10)
        self.valid_scores = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        # Performance status descriptions mapping
        self.performance_descriptions = {
            100: "Fully active, normal",
            90: "Minor restrictions in strenuous physical activity",
            80: "Active, but gets tired more quickly",
            70: "Greater restriction of play and less time spent in play activity",
            60: "Up and around, but active play minimal",
            50: "Lying around much of the day, but gets dressed",
            40: "Mainly in bed; participates in quiet activities",
            30: "Bedbound; needing assistance even for quiet play",
            20: "Sleeping often; play entirely limited to very passive activities",
            10: "Doesn't play; does not get out of bed",
            0: "Unresponsive"
        }
        
        # Functional capacity thresholds
        self.normal_function_threshold = 100
        self.minimal_disability_min = 80
        self.mild_disability_threshold = 70
        self.moderate_disability_min = 40
        self.severe_disability_max = 30
    
    def calculate(self, performance_status: int) -> Dict[str, Any]:
        """
        Assesses pediatric functional status using Lansky Play-Performance Scale
        
        Args:
            performance_status (int): Current functional performance status (0-100 in increments of 10)
            
        Returns:
            Dict with performance assessment and clinical interpretation
        """
        
        # Validate input
        self._validate_input(performance_status)
        
        # Get functional status assessment
        status_assessment = self._assess_functional_status(performance_status)
        
        # Generate clinical interpretation
        interpretation = self._generate_interpretation(performance_status, status_assessment)
        
        return {
            "result": performance_status,
            "unit": "points",
            "interpretation": interpretation,
            "stage": status_assessment["stage"],
            "stage_description": status_assessment["description"]
        }
    
    def _validate_input(self, performance_status: int):
        """Validates input parameters"""
        
        if not isinstance(performance_status, int):
            raise ValueError("Performance status must be an integer")
        
        if performance_status not in self.valid_scores:
            raise ValueError(f"Performance status must be one of: {self.valid_scores}")
    
    def _assess_functional_status(self, score: int) -> Dict[str, str]:
        """
        Assesses functional status based on Lansky score
        
        Args:
            score (int): Lansky performance score
            
        Returns:
            Dict with functional status assessment
        """
        
        if score == 0:
            return {
                "stage": "Unresponsive",
                "description": "Completely unresponsive",
                "category": "Critical"
            }
        elif score == 10:
            return {
                "stage": "Severe Disability",
                "description": "Does not play; does not get out of bed",
                "category": "Severe"
            }
        elif score == 20:
            return {
                "stage": "Major Disability", 
                "description": "Sleeping often; play entirely limited to very passive activities",
                "category": "Severe"
            }
        elif score == 30:
            return {
                "stage": "Moderate-Severe Disability",
                "description": "Bedbound; needing assistance even for quiet play",
                "category": "Moderate-Severe"
            }
        elif score == 40:
            return {
                "stage": "Moderate Disability",
                "description": "Mainly in bed; participates in quiet activities",
                "category": "Moderate"
            }
        elif score in [50, 60]:
            return {
                "stage": "Mild-Moderate Disability",
                "description": "Up and around but with limited activity",
                "category": "Mild-Moderate"
            }
        elif score == 70:
            return {
                "stage": "Mild Disability",
                "description": "Greater restriction of play and less time spent in play activity",
                "category": "Mild"
            }
        elif score in [80, 90]:
            return {
                "stage": "Minimal Disability",
                "description": "Active but with some limitations",
                "category": "Minimal"
            }
        else:  # score == 100
            return {
                "stage": "Normal Function",
                "description": "Fully active, normal",
                "category": "Normal"
            }
    
    def _generate_interpretation(self, score: int, assessment: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            score (int): Lansky performance score
            assessment (Dict): Functional status assessment
            
        Returns:
            str: Detailed clinical interpretation
        """
        
        # Base interpretation with score and description
        base_description = self.performance_descriptions[score]
        interpretation = f"Lansky Play-Performance Scale score: {score} points - {base_description}. "
        
        # Add clinical significance based on score range
        if score == 100:
            interpretation += (
                "Excellent functional status with no limitations in activity or play. "
                "Child can participate fully in age-appropriate activities and has optimal quality of life. "
                "No special accommodations needed for normal activities."
            )
        elif score >= 80:
            interpretation += (
                "Good functional status with minimal limitations. "
                "Child can carry on most normal activities with some restrictions in strenuous activities. "
                "Generally able to attend school and participate in most age-appropriate activities. "
                "Monitor for fatigue and provide support as needed."
            )
        elif score == 70:
            interpretation += (
                "Mild functional impairment with some activity restrictions. "
                "Child may require modifications to normal activities and shorter activity periods. "
                "School attendance may be affected. Consider adaptive strategies and energy conservation."
            )
        elif score >= 50:
            interpretation += (
                "Moderate functional impairment requiring significant support. "
                "Child has limited ability to engage in normal activities and may need assistance with daily tasks. "
                "Consider home schooling, physical therapy, and adaptive equipment. "
                "Regular assessment of functional capacity is important."
            )
        elif score >= 30:
            interpretation += (
                "Significant functional impairment with severe activity limitations. "
                "Child requires extensive care and support for most activities. "
                "Focus on comfort measures, symptom management, and quality of life. "
                "Consider palliative care consultation and family support services."
            )
        elif score >= 10:
            interpretation += (
                "Severe functional impairment with profound activity limitations. "
                "Child is primarily bed-bound and requires complete care assistance. "
                "Palliative care approach focusing on comfort and symptom management. "
                "Provide comprehensive family support and consider end-of-life planning discussions."
            )
        else:  # score == 0
            interpretation += (
                "Complete functional impairment - child is unresponsive. "
                "Requires total care with focus on comfort measures and family support. "
                "Consider intensive palliative care and end-of-life care planning."
            )
        
        # Add general clinical guidance
        interpretation += (
            " The Lansky Play-Performance Scale should be assessed regularly to monitor "
            "disease progression and treatment response. This assessment reflects the child's "
            "functional status over the recent period and should consider parent/caregiver input. "
            "Use in conjunction with other clinical measures for comprehensive care planning."
        )
        
        return interpretation


def calculate_lansky_play_performance_scale(performance_status) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = LanskyPlayPerformanceScaleCalculator()
    return calculator.calculate(performance_status)