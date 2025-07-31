"""
Gail Model for Breast Cancer Risk Calculator

Estimates risk for breast cancer based on demographic and clinical data.

References:
1. Gail MH, Brinton LA, Byar DP, et al. Projecting individualized probabilities of 
   developing breast cancer for white females who are being examined annually. 
   J Natl Cancer Inst. 1989;81(24):1879-86. doi: 10.1093/jnci/81.24.1879.
2. Costantino JP, Gail MH, Pee D, et al. Validation studies for models projecting 
   the risk of invasive and total breast cancer incidence. J Natl Cancer Inst. 
   1999;91(18):1541-8. doi: 10.1093/jnci/91.18.1541.
3. Matsuno RK, Costantino JP, Ziegler RG, et al. Projecting individualized absolute 
   invasive breast cancer risk in Asian and Pacific Islander American women. 
   J Natl Cancer Inst. 2011;103(12):951-61. doi: 10.1093/jnci/djr154.

Note: This is a simplified implementation using representative relative risk values 
from the literature. The exact NCI Gail Model uses complex race-specific coefficients 
and competing hazards calculations that are proprietary.
"""

from typing import Dict, Any, Optional
import math


class GailModelBreastCancerRiskCalculator:
    """Calculator for Gail Model Breast Cancer Risk Assessment"""
    
    def __init__(self):
        # Simplified relative risk factors based on literature
        # Note: These are representative values, not the exact NCI coefficients
        
        # Age-specific baseline risks (per 100,000 women per year)
        self.BASELINE_RISKS = {
            (35, 39): 0.00088,
            (40, 44): 0.00152,
            (45, 49): 0.00231,
            (50, 54): 0.00262,
            (55, 59): 0.00346,
            (60, 64): 0.00412,
            (65, 69): 0.00453,
            (70, 74): 0.00455,
            (75, 79): 0.00433,
            (80, 85): 0.00386
        }
        
        # Relative risks for age at menarche
        self.MENARCHE_RR = {
            "7_to_11": 1.21,
            "12_to_13": 1.10,
            "over_13": 1.00,
            "unknown": 1.00
        }
        
        # Relative risks for age at first birth
        self.FIRST_BIRTH_RR = {
            "no_births": 1.24,
            "under_20": 1.00,
            "20_to_24": 1.10,
            "25_to_29": 1.25,
            "30_or_over": 1.62,
            "unknown": 1.13
        }
        
        # Relative risks for family history
        self.FAMILY_HISTORY_RR = {
            "0": 1.00,
            "1": 2.30,
            "more_than_1": 4.30,
            "unknown": 1.15
        }
        
        # Relative risks for previous biopsies
        self.BIOPSIES_RR = {
            "0": 1.00,
            "1": 1.70,
            "more_than_1": 2.88,
            "unknown": 1.00
        }
        
        # Additional risk for atypical hyperplasia
        self.ATYPICAL_HYPERPLASIA_MULTIPLIER = {
            "yes": 4.17,
            "no": 1.00,
            "unknown": 1.00
        }
        
        # Race/ethnicity adjustment factors
        self.RACE_ADJUSTMENT = {
            "white": 1.00,
            "african_american": 0.78,
            "hispanic": 0.73,
            "asian_american": 0.50,
            "american_indian_alaskan_native": 0.85,
            "unknown": 1.00
        }
    
    def calculate(self, age: int, age_at_menarche: str, age_at_first_birth: str,
                  relatives_with_breast_cancer: str, previous_biopsies: str,
                  atypical_hyperplasia: str, race_ethnicity: str,
                  asian_subrace: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates Gail Model breast cancer risk assessment
        
        Args:
            age (int): Current age (35-85)
            age_at_menarche (str): Age at first menstrual period
            age_at_first_birth (str): Age at first live birth or nulliparous
            relatives_with_breast_cancer (str): Number of first-degree relatives with breast cancer
            previous_biopsies (str): Number of previous breast biopsies
            atypical_hyperplasia (str): History of atypical hyperplasia
            race_ethnicity (str): Race/ethnicity
            asian_subrace (str, optional): Asian sub-race if applicable
            
        Returns:
            Dict with 5-year breast cancer risk and interpretation
        """
        
        # Validations
        self._validate_inputs(age, age_at_menarche, age_at_first_birth,
                            relatives_with_breast_cancer, previous_biopsies,
                            atypical_hyperplasia, race_ethnicity, asian_subrace)
        
        # Calculate relative risk
        relative_risk = self._calculate_relative_risk(
            age, age_at_menarche, age_at_first_birth,
            relatives_with_breast_cancer, previous_biopsies,
            atypical_hyperplasia, race_ethnicity, asian_subrace
        )
        
        # Calculate 5-year absolute risk
        five_year_risk = self._calculate_absolute_risk(age, relative_risk)
        
        # Get interpretation
        interpretation = self._get_interpretation(five_year_risk)
        
        return {
            "result": round(five_year_risk, 2),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, age_at_menarche: str, age_at_first_birth: str,
                        relatives_with_breast_cancer: str, previous_biopsies: str,
                        atypical_hyperplasia: str, race_ethnicity: str,
                        asian_subrace: Optional[str]):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 35 or age > 85:
            raise ValueError("Age must be an integer between 35 and 85")
        
        valid_menarche = ["unknown", "7_to_11", "12_to_13", "over_13"]
        if age_at_menarche not in valid_menarche:
            raise ValueError(f"Invalid age_at_menarche: {age_at_menarche}")
        
        valid_first_birth = ["unknown", "no_births", "under_20", "20_to_24", "25_to_29", "30_or_over"]
        if age_at_first_birth not in valid_first_birth:
            raise ValueError(f"Invalid age_at_first_birth: {age_at_first_birth}")
        
        valid_relatives = ["unknown", "0", "1", "more_than_1"]
        if relatives_with_breast_cancer not in valid_relatives:
            raise ValueError(f"Invalid relatives_with_breast_cancer: {relatives_with_breast_cancer}")
        
        valid_biopsies = ["unknown", "0", "1", "more_than_1"]
        if previous_biopsies not in valid_biopsies:
            raise ValueError(f"Invalid previous_biopsies: {previous_biopsies}")
        
        valid_hyperplasia = ["unknown", "no", "yes"]
        if atypical_hyperplasia not in valid_hyperplasia:
            raise ValueError(f"Invalid atypical_hyperplasia: {atypical_hyperplasia}")
        
        valid_race = ["white", "african_american", "hispanic", "asian_american", 
                      "american_indian_alaskan_native", "unknown"]
        if race_ethnicity not in valid_race:
            raise ValueError(f"Invalid race_ethnicity: {race_ethnicity}")
        
        if race_ethnicity == "asian_american" and asian_subrace:
            valid_subrace = ["chinese", "japanese", "filipino", "hawaiian", "pacific_islander"]
            if asian_subrace not in valid_subrace:
                raise ValueError(f"Invalid asian_subrace: {asian_subrace}")
    
    def _calculate_relative_risk(self, age: int, age_at_menarche: str, age_at_first_birth: str,
                                relatives_with_breast_cancer: str, previous_biopsies: str,
                                atypical_hyperplasia: str, race_ethnicity: str,
                                asian_subrace: Optional[str]) -> float:
        """Calculates the composite relative risk"""
        
        # Base relative risk
        rr = 1.0
        
        # Apply age at menarche risk
        rr *= self.MENARCHE_RR[age_at_menarche]
        
        # Apply age at first birth risk
        rr *= self.FIRST_BIRTH_RR[age_at_first_birth]
        
        # Apply family history risk
        rr *= self.FAMILY_HISTORY_RR[relatives_with_breast_cancer]
        
        # Apply biopsy history risk
        rr *= self.BIOPSIES_RR[previous_biopsies]
        
        # Apply atypical hyperplasia multiplier (only if previous biopsies)
        if previous_biopsies in ["1", "more_than_1"]:
            rr *= self.ATYPICAL_HYPERPLASIA_MULTIPLIER[atypical_hyperplasia]
        
        # Apply race/ethnicity adjustment
        rr *= self.RACE_ADJUSTMENT[race_ethnicity]
        
        # Additional Asian subrace adjustments (simplified)
        if race_ethnicity == "asian_american" and asian_subrace:
            asian_adjustments = {
                "chinese": 0.9,
                "japanese": 1.1,
                "filipino": 1.2,
                "hawaiian": 1.3,
                "pacific_islander": 1.1
            }
            rr *= asian_adjustments.get(asian_subrace, 1.0)
        
        return rr
    
    def _calculate_absolute_risk(self, age: int, relative_risk: float) -> float:
        """Converts relative risk to 5-year absolute risk"""
        
        # Find appropriate age bracket for baseline risk
        baseline_risk = 0.003  # Default baseline
        for (min_age, max_age), risk in self.BASELINE_RISKS.items():
            if min_age <= age <= max_age:
                baseline_risk = risk
                break
        
        # Calculate 5-year cumulative risk
        # Simplified formula: not accounting for competing hazards
        five_year_baseline = 5 * baseline_risk
        five_year_risk = five_year_baseline * relative_risk
        
        # Convert to percentage and cap at reasonable maximum
        five_year_risk_percent = min(five_year_risk * 100, 50.0)
        
        return five_year_risk_percent
    
    def _get_age_bracket(self, age: int) -> tuple:
        """Helper to get age bracket for baseline risk lookup"""
        if age < 40:
            return (35, 39)
        elif age < 45:
            return (40, 44)
        elif age < 50:
            return (45, 49)
        elif age < 55:
            return (50, 54)
        elif age < 60:
            return (55, 59)
        elif age < 65:
            return (60, 64)
        elif age < 70:
            return (65, 69)
        elif age < 75:
            return (70, 74)
        elif age < 80:
            return (75, 79)
        else:
            return (80, 85)
    
    def _get_interpretation(self, five_year_risk: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on 5-year risk
        
        Args:
            five_year_risk (float): 5-year absolute risk percentage
            
        Returns:
            Dict with interpretation
        """
        
        if five_year_risk < 1.67:
            return {
                "stage": "Low Risk",
                "description": "Low risk for breast cancer",
                "interpretation": (f"5-year breast cancer risk of {five_year_risk}% is below the 1.67% threshold "
                                f"for chemoprevention consideration. Continue routine screening mammography according "
                                f"to guidelines. Discuss general risk reduction strategies including maintaining healthy "
                                f"weight, regular physical activity, limiting alcohol consumption, and avoiding "
                                f"unnecessary hormone therapy. Consider lifestyle modifications and routine surveillance.")
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk for breast cancer",
                "interpretation": (f"5-year breast cancer risk of {five_year_risk}% meets or exceeds the 1.67% threshold. "
                                f"Consider discussing chemoprevention options (tamoxifen, raloxifene, or aromatase inhibitors) "
                                f"with patient after evaluating benefits and risks. Enhanced screening strategies may be "
                                f"appropriate including earlier screening initiation, shorter screening intervals, or "
                                f"consideration of breast MRI. Genetic counseling may be considered if family history "
                                f"is significant. Discuss risk-benefit ratio of preventive interventions.")
            }


def calculate_gail_model_breast_cancer_risk(age: int, age_at_menarche: str, age_at_first_birth: str,
                                          relatives_with_breast_cancer: str, previous_biopsies: str,
                                          atypical_hyperplasia: str, race_ethnicity: str,
                                          asian_subrace: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gail_model_breast_cancer_risk pattern
    """
    calculator = GailModelBreastCancerRiskCalculator()
    return calculator.calculate(
        age, age_at_menarche, age_at_first_birth,
        relatives_with_breast_cancer, previous_biopsies,
        atypical_hyperplasia, race_ethnicity, asian_subrace
    )