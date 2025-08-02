"""
Hour-Specific Risk for Neonatal Hyperbilirubinemia Calculator

Uses the Bhutani nomogram to predict risk of hyperbilirubinemia in neonates based on 
total serum bilirubin measurement at specific postnatal age in hours.

References:
- Bhutani VK, Johnson L, Sivieri EM. Predictive ability of a predischarge hour-specific 
  serum bilirubin for subsequent significant hyperbilirubinemia in healthy term and 
  near-term newborns. Pediatrics. 1999 Jan;103(1):6-14.
"""

from typing import Dict, Any


class HourSpecificNeonatalHyperbilirubinemiaCalculator:
    """Calculator for Hour-Specific Risk for Neonatal Hyperbilirubinemia"""
    
    def __init__(self):
        # Define Bhutani nomogram percentile curves (hours: bilirubin mg/dL)
        # Based on the published nomogram data points
        self.percentile_40 = {
            12: 4.0, 18: 5.0, 24: 5.8, 30: 6.5, 36: 7.2, 42: 7.8,
            48: 8.4, 54: 8.9, 60: 9.3, 66: 9.7, 72: 10.0, 78: 10.3,
            84: 10.5, 90: 10.7, 96: 10.9, 102: 11.0, 108: 11.1, 114: 11.2,
            120: 11.3, 126: 11.4, 132: 11.5, 138: 11.6, 144: 11.7, 150: 11.8,
            156: 11.9, 162: 11.9, 168: 12.0
        }
        
        self.percentile_75 = {
            12: 5.5, 18: 6.7, 24: 7.8, 30: 8.7, 36: 9.5, 42: 10.2,
            48: 10.9, 54: 11.5, 60: 12.0, 66: 12.4, 72: 12.8, 78: 13.1,
            84: 13.4, 90: 13.6, 96: 13.8, 102: 14.0, 108: 14.1, 114: 14.2,
            120: 14.3, 126: 14.4, 132: 14.5, 138: 14.6, 144: 14.7, 150: 14.8,
            156: 14.9, 162: 14.9, 168: 15.0
        }
        
        self.percentile_95 = {
            12: 7.0, 18: 8.5, 24: 10.0, 30: 11.1, 36: 12.1, 42: 12.9,
            48: 13.7, 54: 14.3, 60: 14.9, 66: 15.4, 72: 15.8, 78: 16.2,
            84: 16.5, 90: 16.8, 96: 17.0, 102: 17.2, 108: 17.4, 114: 17.5,
            120: 17.6, 126: 17.7, 132: 17.8, 138: 17.9, 144: 18.0, 150: 18.1,
            156: 18.2, 162: 18.2, 168: 18.3
        }
    
    def calculate(self, age_hours: int, total_bilirubin: float) -> Dict[str, Any]:
        """
        Calculates risk zone based on hour-specific bilirubin level
        
        Args:
            age_hours (int): Age of neonate in hours (12-168)
            total_bilirubin (float): Total serum bilirubin in mg/dL
            
        Returns:
            Dict with risk zone classification and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_hours, total_bilirubin)
        
        # Get interpolated percentile thresholds for the specific hour
        p40_threshold = self._interpolate_percentile(age_hours, self.percentile_40)
        p75_threshold = self._interpolate_percentile(age_hours, self.percentile_75)
        p95_threshold = self._interpolate_percentile(age_hours, self.percentile_95)
        
        # Determine risk zone based on bilirubin level
        if total_bilirubin < p40_threshold:
            zone = "Low Risk"
            interpretation = self._get_interpretation(0)
        elif total_bilirubin < p75_threshold:
            zone = "Low-Intermediate Risk"
            interpretation = self._get_interpretation(50)
        elif total_bilirubin < p95_threshold:
            zone = "High-Intermediate Risk"
            interpretation = self._get_interpretation(85)
        else:
            zone = "High Risk"
            interpretation = self._get_interpretation(95)
        
        # Calculate approximate percentile
        percentile = self._calculate_percentile(age_hours, total_bilirubin, 
                                               p40_threshold, p75_threshold, p95_threshold)
        
        return {
            "result": zone,
            "unit": "zone",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "percentile": round(percentile, 1)
        }
    
    def _validate_inputs(self, age_hours: int, total_bilirubin: float):
        """Validates input parameters"""
        
        if not isinstance(age_hours, int):
            raise ValueError("Age must be an integer value in hours")
        
        if age_hours < 12 or age_hours > 168:
            raise ValueError("Age must be between 12 and 168 hours")
        
        if not isinstance(total_bilirubin, (int, float)):
            raise ValueError("Total bilirubin must be a numeric value")
        
        if total_bilirubin < 0.1 or total_bilirubin > 30:
            raise ValueError("Total bilirubin must be between 0.1 and 30 mg/dL")
    
    def _interpolate_percentile(self, age_hours: int, percentile_data: dict) -> float:
        """
        Interpolates percentile threshold for specific hour
        
        Args:
            age_hours: Age in hours
            percentile_data: Dictionary of hour: bilirubin values
            
        Returns:
            Interpolated bilirubin threshold
        """
        
        # Get exact data points
        hours_list = sorted(percentile_data.keys())
        
        # If exact hour exists, return it
        if age_hours in percentile_data:
            return percentile_data[age_hours]
        
        # Find surrounding hours for interpolation
        lower_hour = max([h for h in hours_list if h < age_hours])
        upper_hour = min([h for h in hours_list if h > age_hours])
        
        # Linear interpolation
        lower_value = percentile_data[lower_hour]
        upper_value = percentile_data[upper_hour]
        
        # Calculate interpolated value
        fraction = (age_hours - lower_hour) / (upper_hour - lower_hour)
        interpolated = lower_value + fraction * (upper_value - lower_value)
        
        return round(interpolated, 2)
    
    def _calculate_percentile(self, age_hours: int, total_bilirubin: float,
                            p40: float, p75: float, p95: float) -> float:
        """
        Estimates approximate percentile based on bilirubin level
        
        Args:
            age_hours: Age in hours
            total_bilirubin: Measured bilirubin level
            p40, p75, p95: Percentile thresholds
            
        Returns:
            Estimated percentile (0-100)
        """
        
        if total_bilirubin < p40:
            # Linear interpolation between 0 and 40th percentile
            # Assuming 0th percentile is approximately 60% of 40th percentile value
            p0_estimate = p40 * 0.6
            if total_bilirubin <= p0_estimate:
                return 0.0
            return 40 * (total_bilirubin - p0_estimate) / (p40 - p0_estimate)
        
        elif total_bilirubin < p75:
            # Linear interpolation between 40th and 75th percentile
            return 40 + 35 * (total_bilirubin - p40) / (p75 - p40)
        
        elif total_bilirubin < p95:
            # Linear interpolation between 75th and 95th percentile
            return 75 + 20 * (total_bilirubin - p75) / (p95 - p75)
        
        else:
            # Above 95th percentile
            # Asymptotic approach to 100th percentile
            excess = total_bilirubin - p95
            return min(99.9, 95 + 5 * (1 - 1 / (1 + excess)))
    
    def _get_interpretation(self, percentile: float) -> Dict[str, str]:
        """
        Determines the interpretation based on percentile
        
        Args:
            percentile (float): Estimated percentile
            
        Returns:
            Dict with interpretation details
        """
        
        if percentile < 40:
            return {
                "stage": "Low Risk",
                "description": "<40th percentile",
                "interpretation": "Low risk zone. No measurable risk for subsequent significant hyperbilirubinemia (0% probability). Routine follow-up as per discharge timing guidelines."
            }
        elif percentile < 75:
            return {
                "stage": "Low-Intermediate Risk",
                "description": "40th-75th percentile",
                "interpretation": "Low-intermediate risk zone. Small risk of subsequent hyperbilirubinemia (2.2% probability). Follow-up within 48-72 hours recommended based on clinical factors."
            }
        elif percentile < 95:
            return {
                "stage": "High-Intermediate Risk",
                "description": "76th-94th percentile",
                "interpretation": "High-intermediate risk zone. Moderate risk of subsequent hyperbilirubinemia (12.9% probability). Closer follow-up within 24-48 hours recommended."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "≥95th percentile",
                "interpretation": "High risk zone. Significant risk of subsequent hyperbilirubinemia (39.5% probability). Consider extended hospitalization or close follow-up within 24 hours. May require early intervention."
            }


def calculate_hour_specific_neonatal_hyperbilirubinemia(age_hours: int, 
                                                       total_bilirubin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HourSpecificNeonatalHyperbilirubinemiaCalculator()
    return calculator.calculate(age_hours, total_bilirubin)