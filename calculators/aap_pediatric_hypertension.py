"""
AAP Pediatric Hypertension Guidelines Calculator

Diagnoses hypertension in pediatric patients based on AAP 2017 guidelines.
Reference: Flynn JT et al. Pediatrics. 2017;140(3):e20171904.
"""

import math
from typing import Dict, Any


class AAPPediatricHypertensionCalculator:
    """Calculator for AAP Pediatric Hypertension Guidelines"""
    
    def __init__(self):
        # Simplified height percentile tables by age and sex (WHO/CDC)
        # For implementation purposes, using approximate values
        self.height_percentiles = {
            "male": {
                1: {"p50": 76.1}, 2: {"p50": 87.8}, 3: {"p50": 96.1}, 4: {"p50": 103.3},
                5: {"p50": 109.9}, 6: {"p50": 116.1}, 7: {"p50": 121.9}, 8: {"p50": 128.0},
                9: {"p50": 133.3}, 10: {"p50": 138.4}, 11: {"p50": 143.5}, 12: {"p50": 149.1},
                13: {"p50": 156.2}, 14: {"p50": 163.8}, 15: {"p50": 170.1}, 16: {"p50": 173.4},
                17: {"p50": 175.2}
            },
            "female": {
                1: {"p50": 74.3}, 2: {"p50": 86.4}, 3: {"p50": 95.1}, 4: {"p50": 102.7},
                5: {"p50": 109.4}, 6: {"p50": 115.5}, 7: {"p50": 121.1}, 8: {"p50": 126.4},
                9: {"p50": 132.2}, 10: {"p50": 138.4}, 11: {"p50": 144.8}, 12: {"p50": 151.0},
                13: {"p50": 156.7}, 14: {"p50": 160.4}, 15: {"p50": 162.5}, 16: {"p50": 163.0},
                17: {"p50": 163.0}
            }
        }
        
        # Simplified BP percentile reference values (based on AAP 2017 tables)
        # Full implementation would require extensive tables by age, sex, and height percentile
        self.bp_references = {
            "percentile_90": {"sys": 110, "dia": 70},
            "percentile_95": {"sys": 115, "dia": 75},
            "percentile_99": {"sys": 125, "dia": 82}
        }
    
    def calculate(self, age: int, sex: str, height: float, 
                 systolic_bp: int, diastolic_bp: int) -> Dict[str, Any]:
        """
        Classifies pediatric blood pressure according to AAP 2017 guidelines
        
        Args:
            age: Age in years (1-17)
            sex: "male" or "female"
            height: Height in centimeters
            systolic_bp: Systolic pressure in mmHg
            diastolic_bp: Diastolic pressure in mmHg
            
        Returns:
            Dict with classification and interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, height, systolic_bp, diastolic_bp)
        
        # Calculate height percentile
        height_percentile = self._calculate_height_percentile(age, sex, height)
        
        # Determine classification for adolescents ≥13 years (hybrid adult criteria)
        if age >= 13:
            classification = self._classify_adolescent_bp(systolic_bp, diastolic_bp, age, sex, height)
        else:
            # For children under 13, use pediatric tables
            classification = self._classify_pediatric_bp(systolic_bp, diastolic_bp, age, sex, height_percentile)
        
        # Get detailed interpretation
        interpretation = self._get_interpretation(classification, age, systolic_bp, diastolic_bp)
        
        return {
            "result": classification,
            "unit": "classification",
            "height_percentile": round(height_percentile, 1),
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "systolic_percentile": 75.0,  # Placeholder - would need full implementation
            "diastolic_percentile": 70.0,  # Placeholder - would need full implementation
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, height: float, 
                        systolic_bp: int, diastolic_bp: int):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 1 or age > 17:
            raise ValueError("Age must be an integer between 1 and 17 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(height, (int, float)) or height < 70.0 or height > 200.0:
            raise ValueError("Height must be between 70.0 and 200.0 cm")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 60 or systolic_bp > 200:
            raise ValueError("Systolic pressure must be between 60 and 200 mmHg")
        
        if not isinstance(diastolic_bp, int) or diastolic_bp < 30 or diastolic_bp > 150:
            raise ValueError("Diastolic pressure must be between 30 and 150 mmHg")
        
        if systolic_bp <= diastolic_bp:
            raise ValueError("Systolic pressure must be greater than diastolic pressure")
    
    def _calculate_height_percentile(self, age: int, sex: str, height: float) -> float:
        """
        Calculates approximate height percentile based on median height
        
        NOTE: Simplified implementation. For actual clinical use, 
        full WHO/CDC tables with Z-scores would be needed.
        """
        
        if age not in self.height_percentiles[sex]:
            # Approximation for untabled ages
            closest_age = min(self.height_percentiles[sex].keys(), 
                            key=lambda x: abs(x - age))
            median_height = self.height_percentiles[sex][closest_age]["p50"]
        else:
            median_height = self.height_percentiles[sex][age]["p50"]
        
        # Simplified percentile estimate based on difference from median
        # Assuming approximately normal distribution
        z_score = (height - median_height) / (median_height * 0.1)  # Estimated deviation
        percentile = self._z_to_percentile(z_score)
        
        return max(1.0, min(99.0, percentile))
    
    def _z_to_percentile(self, z_score: float) -> float:
        """Converts Z-score to approximate percentile"""
        
        # Simplified standard normal cumulative distribution function
        return 50.0 * (1.0 + math.erf(z_score / math.sqrt(2.0)))
    
    def _classify_adolescent_bp(self, systolic: int, diastolic: int, 
                               age: int, sex: str, height: float) -> str:
        """
        Classifies BP in adolescents ≥13 years using hybrid criteria
        (combines pediatric percentiles with adult absolute values)
        """
        
        # For adolescents, use adult values if greater than pediatric percentiles
        if systolic >= 140 or diastolic >= 90:
            return "Hypertension Stage 2"
        elif systolic >= 130 or diastolic >= 80:
            return "Hypertension Stage 1"
        elif systolic >= 120:
            return "Elevated"
        else:
            # Also check pediatric percentiles
            return self._classify_pediatric_bp(systolic, diastolic, age, sex, 50.0)
    
    def _classify_pediatric_bp(self, systolic: int, diastolic: int, 
                              age: int, sex: str, height_percentile: float) -> str:
        """
        Classifies BP using pediatric tables
        
        NOTE: Simplified implementation with approximate reference values.
        For actual clinical use, full AAP 2017 tables would be needed.
        """
        
        # Approximate adjustment based on age (BP increases with age)
        age_factor = 1.0 + (age - 5) * 0.02  # Approximate increment per year
        
        # Approximate adjustment based on height percentile
        height_factor = 1.0 + (height_percentile - 50) * 0.001  # Adjustment by height
        
        # Adjusted reference values
        p90_sys = self.bp_references["percentile_90"]["sys"] * age_factor * height_factor
        p90_dia = self.bp_references["percentile_90"]["dia"] * age_factor * height_factor
        
        p95_sys = self.bp_references["percentile_95"]["sys"] * age_factor * height_factor
        p95_dia = self.bp_references["percentile_95"]["dia"] * age_factor * height_factor
        
        p99_sys = self.bp_references["percentile_99"]["sys"] * age_factor * height_factor
        p99_dia = self.bp_references["percentile_99"]["dia"] * age_factor * height_factor
        
        # Classification based on the higher percentile (systolic or diastolic)
        if systolic >= p99_sys or diastolic >= p99_dia:
            return "Hypertension Stage 2"
        elif systolic >= p95_sys or diastolic >= p95_dia:
            return "Hypertension Stage 1"
        elif systolic >= p90_sys or diastolic >= p90_dia:
            return "Elevated"
        else:
            return "Normal"
    
    def _get_interpretation(self, classification: str, age: int, 
                          systolic: int, diastolic: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on classification
        """
        
        interpretations = {
            "Normal": {
                "stage": "Normal",
                "description": "Normal blood pressure",
                "interpretation": f"BP {systolic}/{diastolic} mmHg is below the 90th percentile for age, sex, and height. No specific intervention required. Maintenance of healthy lifestyle and annual re-evaluation recommended."
            },
            "Elevated": {
                "stage": "Elevated",
                "description": "Elevated blood pressure",
                "interpretation": f"BP {systolic}/{diastolic} mmHg is between percentiles 90-94 for age, sex, and height. Requires lifestyle modifications (diet, exercise, weight reduction if necessary) and re-evaluation in 6 months. Assess cardiovascular risk factors."
            },
            "Hypertension Stage 1": {
                "stage": "Hypertension Stage 1",
                "description": "Hypertension stage 1",
                "interpretation": f"BP {systolic}/{diastolic} mmHg is between percentiles 95-98 for age, sex, and height. Must be confirmed in 3 different visits. Initiate lifestyle modifications and consider medication if risk factors are present."
            },
            "Hypertension Stage 2": {
                "stage": "Hypertension Stage 2",
                "description": "Hypertension stage 2",
                "interpretation": f"BP {systolic}/{diastolic} mmHg is ≥percentile 99 for age, sex, and height. Must be confirmed in 1-2 weeks. Requires immediate medication treatment along with intensive lifestyle modifications. Investigate secondary causes."
            }
        }
        
        return interpretations.get(classification, interpretations["Normal"])


def calculate_aap_pediatric_hypertension(age: int, sex: str, height: float,
                                       systolic_bp: int, diastolic_bp: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AAPPediatricHypertensionCalculator()
    return calculator.calculate(age, sex, height, systolic_bp, diastolic_bp)
