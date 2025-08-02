"""
Roth Score for Hypoxia Screening Calculator

Screens for hypoxia in dyspneic patients using a simple verbal counting test.
The Roth Score evaluates respiratory distress by measuring how high a patient 
can count from 1 to 30 in a single breath and how long it takes.

References (Vancouver style):
1. Chorin E, Padegimas A, Havakuk O, Birati EY, Shacham Y, Milman A, Flint N, 
   Konigstein M, Nevzorov R, Moshe Y, Margolis G, Alcalai R, Topilsky Y. 
   Assessment of Respiratory Distress by the Roth Score. Clin Cardiol. 
   2016 Nov;39(11):636-639. doi: 10.1002/clc.22570.
2. Sánchez-Martínez C, Freitas-Alvarenga T, Puerta-García E, Navarro-Martínez S, 
   Iglesias-Vázquez JA, Rodríguez-Suárez P, Carbajales-Pérez C, Miró Ò. 
   Validity of the 'Roth score' for hypoxemia screening. Am J Emerg Med. 
   2023 May;67:1-7. doi: 10.1016/j.ajem.2023.01.038.
3. García-Villafranca M, Escolano-Casado G, González-Del Castillo J, 
   Martín-Sánchez FJ. The use of the Roth score in emergency department 
   for patients with acute exacerbation of chronic obstructive pulmonary disease. 
   Am J Emerg Med. 2024 Dec;86:164-165. doi: 10.1016/j.ajem.2024.09.025.
"""

from typing import Dict, Any


class RothScoreCalculator:
    """Calculator for Roth Score hypoxia screening"""
    
    def __init__(self):
        # Risk thresholds based on original validation studies
        self.HIGH_RISK_COUNT_THRESHOLD = 7  # <7 numbers = high risk for O2 sat <90%
        self.HIGH_RISK_TIME_THRESHOLD = 5   # <5 seconds = high risk for O2 sat <90%
        self.MODERATE_RISK_COUNT_THRESHOLD = 10  # <10 numbers = risk for O2 sat <95%
        self.MODERATE_RISK_TIME_THRESHOLD = 7    # <7 seconds = risk for O2 sat <95%
        
        # Performance characteristics from validation studies
        self.SENSITIVITY_COUNT_95 = 0.91  # 91% sensitive for O2 sat <95% when max <10
        self.SENSITIVITY_COUNT_90 = 0.87  # 87% sensitive for O2 sat <90% when max <7
        self.SENSITIVITY_TIME_95 = 0.83   # 83% sensitive for O2 sat <95% when time <7s
        self.SENSITIVITY_TIME_90 = 0.82   # 82% sensitive for O2 sat <90% when time <5s
    
    def calculate(self, max_number_reached: int, total_seconds_counted: float) -> Dict[str, Any]:
        """
        Calculates the Roth Score assessment for hypoxia screening
        
        The Roth Score uses both counting performance and time duration to assess
        respiratory distress and screen for hypoxia. Patients take a deep breath
        and count from 1 to 30 as fast as possible without stopping.
        
        Args:
            max_number_reached (int): Maximum number reached when counting 1-30 in single breath (0-30)
            total_seconds_counted (float): Total seconds taken to count (regardless of final number)
            
        Returns:
            Dict with the assessment category and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(max_number_reached, total_seconds_counted)
        
        # Determine risk category based on both parameters
        risk_category = self._determine_risk_category(max_number_reached, total_seconds_counted)
        
        # Get detailed interpretation
        interpretation = self._get_interpretation(risk_category, max_number_reached, total_seconds_counted)
        
        return {
            "result": risk_category,
            "unit": "risk level",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, max_number_reached: int, total_seconds_counted: float):
        """Validates input parameters for Roth Score assessment"""
        
        if not isinstance(max_number_reached, int):
            raise ValueError("Maximum number reached must be an integer")
        
        if max_number_reached < 0 or max_number_reached > 30:
            raise ValueError("Maximum number reached must be between 0 and 30")
        
        if not isinstance(total_seconds_counted, (int, float)):
            raise ValueError("Total seconds counted must be a number")
        
        if total_seconds_counted < 0:
            raise ValueError("Total seconds counted cannot be negative")
        
        if total_seconds_counted > 60:
            raise ValueError("Total seconds counted should not exceed 60 seconds")
        
        # Clinical validity check
        if max_number_reached == 0 and total_seconds_counted == 0:
            raise ValueError("Patient must attempt counting - both parameters cannot be zero")
    
    def _determine_risk_category(self, max_count: int, total_time: float) -> int:
        """
        Determines risk category based on counting performance and time
        
        Risk assessment combines both counting ability and time duration:
        - Category 0 (High Risk): Severe impairment in counting or time
        - Category 1 (Moderate-High Risk): Moderate impairment 
        - Category 2 (Low-Moderate Risk): Mild impairment
        - Category 3 (Low Risk): Normal performance
        
        Args:
            max_count (int): Maximum number reached
            total_time (float): Total time in seconds
            
        Returns:
            int: Risk category (0-3)
        """
        
        # High risk criteria (Category 0) - Severe respiratory distress
        # Either very low count OR very short time indicates severe hypoxia risk
        if (max_count < self.HIGH_RISK_COUNT_THRESHOLD or 
            total_time < self.HIGH_RISK_TIME_THRESHOLD):
            return 0
        
        # Moderate to high risk (Category 1) - Moderate respiratory compromise
        # Count between 7-9 OR time between 5-7 seconds suggests moderate risk
        if ((self.HIGH_RISK_COUNT_THRESHOLD <= max_count < self.MODERATE_RISK_COUNT_THRESHOLD) or 
            (self.HIGH_RISK_TIME_THRESHOLD <= total_time < self.MODERATE_RISK_TIME_THRESHOLD)):
            return 1
        
        # Low to moderate risk (Category 2) - Mild respiratory compromise
        # Good count (≥10) but shorter time, or adequate time but lower count
        if (max_count >= self.MODERATE_RISK_COUNT_THRESHOLD and 
            total_time < self.MODERATE_RISK_TIME_THRESHOLD):
            return 2
        
        # Low risk (Category 3) - Normal respiratory performance
        # Both good counting ability (≥10) AND adequate time (≥7 seconds)
        return 3
    
    def _get_interpretation(self, category: int, max_count: int, total_time: float) -> Dict[str, str]:
        """
        Provides detailed clinical interpretation based on risk category
        
        Args:
            category (int): Risk category (0-3)
            max_count (int): Maximum number reached for context
            total_time (float): Total time for context
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        interpretations = {
            0: {
                "stage": "High Risk for Hypoxia",
                "description": "Severe counting impairment",
                "interpretation": (
                    f"Patient shows severe respiratory distress with very limited counting ability "
                    f"(max: {max_count}, time: {total_time:.1f}s). High risk for significant hypoxia "
                    f"(O2 sat likely <90%). Immediate pulse oximetry measurement and oxygen assessment "
                    f"required. Consider emergency respiratory support and further evaluation for "
                    f"underlying respiratory pathology. This finding suggests severe dyspnea that "
                    f"warrants urgent clinical intervention."
                )
            },
            1: {
                "stage": "Moderate to High Risk",
                "description": "Moderate counting impairment", 
                "interpretation": (
                    f"Patient demonstrates moderate respiratory distress with impaired counting "
                    f"performance (max: {max_count}, time: {total_time:.1f}s). Increased risk for "
                    f"hypoxia (O2 sat potentially <95%). Pulse oximetry measurement recommended to "
                    f"confirm oxygen saturation status. Consider oxygen supplementation if clinically "
                    f"indicated and evaluate for underlying respiratory conditions. Monitor closely "
                    f"for worsening respiratory status."
                )
            },
            2: {
                "stage": "Low to Moderate Risk",
                "description": "Mild counting impairment",
                "interpretation": (
                    f"Patient shows mild respiratory compromise with some counting difficulty "
                    f"(max: {max_count}, time: {total_time:.1f}s). Lower risk for severe hypoxia "
                    f"but clinical correlation recommended. Pulse oximetry should be performed to "
                    f"confirm oxygen saturation. Consider underlying respiratory conditions and "
                    f"continue monitoring. May benefit from supportive care and further assessment "
                    f"based on clinical presentation."
                )
            },
            3: {
                "stage": "Low Risk",
                "description": "Normal counting performance",
                "interpretation": (
                    f"Patient demonstrates good respiratory reserve with normal counting ability "
                    f"(max: {max_count}, time: {total_time:.1f}s). Low risk for significant hypoxia. "
                    f"While pulse oximetry remains the gold standard for oxygen assessment, this "
                    f"finding suggests adequate respiratory function. Continue routine monitoring "
                    f"and evaluate other clinical factors contributing to dyspnea symptoms if present."
                )
            }
        }
        
        return interpretations[category]


def calculate_roth_score(max_number_reached: int, total_seconds_counted: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates Roth Score for hypoxia screening using counting performance.
    
    Args:
        max_number_reached (int): Maximum number reached when counting 1-30 in single breath
        total_seconds_counted (float): Total seconds taken to count
        
    Returns:
        Dict with risk assessment and clinical interpretation
    """
    calculator = RothScoreCalculator()
    return calculator.calculate(max_number_reached, total_seconds_counted)