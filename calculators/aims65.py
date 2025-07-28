"""
AIMS65 Score for Upper GI Bleeding Mortality Calculator

Predicts in-hospital mortality in patients with acute upper gastrointestinal bleeding 
using 5 simple clinical variables that can be assessed early in the emergency department.

The AIMS65 score is a simple, non-endoscopic risk stratification tool that has been 
validated in multiple studies and shown to be superior to other scoring systems in 
predicting in-hospital mortality from upper GI bleeding.

References:
- Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk score 
  accurately predicts in-hospital mortality, length of stay, and cost in acute upper 
  GI bleeding. Gastrointest Endosc. 2011;74(6):1215-24.
- Hyett BH, Abougergi MS, Charpentier JP, et al. The AIMS65 score compared with the 
  Glasgow-Blatchford score in predicting outcomes in upper GI bleeding. Gastrointest 
  Endosc. 2013;77(4):551-7.
"""

from typing import Dict, Any


class Aims65Calculator:
    """Calculator for AIMS65 Score for Upper GI Bleeding Mortality"""
    
    def __init__(self):
        # Mortality rates by score from validation studies
        self.MORTALITY_RATES = {
            0: 0.3,   # 0.3% mortality
            1: 7.8,   # 7.8% mortality  
            2: 20.0,  # 20% mortality
            3: 36.0,  # 36% mortality
            4: 40.0,  # 40% mortality
            5: 50.0   # 50% mortality (extrapolated)
        }
        
        # Risk categories
        self.RISK_CATEGORIES = {
            "Low Risk": (0, 1),
            "Moderate Risk": (2, 2),
            "High Risk": (3, 5)
        }
    
    def calculate(self, albumin: float, inr: float, mental_status_altered: str, 
                 systolic_bp: int, age: int) -> Dict[str, Any]:
        """
        Calculates AIMS65 score using the provided parameters
        
        Args:
            albumin (float): Serum albumin level in g/dL
            inr (float): International Normalized Ratio
            mental_status_altered (str): "yes" or "no" for altered mental status
            systolic_bp (int): Systolic blood pressure in mmHg
            age (int): Patient age in years
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(albumin, inr, mental_status_altered, systolic_bp, age)
        
        # Calculate individual components
        components = self._calculate_components(albumin, inr, mental_status_altered, systolic_bp, age)
        
        # Calculate total score
        total_score = sum(components.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, components)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "components": components,
            "mortality_risk": self.MORTALITY_RATES.get(total_score, 50.0),
            "risk_category": interpretation["risk_category"]
        }
    
    def _validate_inputs(self, albumin: float, inr: float, mental_status_altered: str, 
                        systolic_bp: int, age: int):
        """Validates input parameters"""
        
        # Validate albumin
        if not isinstance(albumin, (int, float)):
            raise ValueError("Albumin must be a number")
        
        if albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be between 1.0 and 6.0 g/dL")
        
        # Validate INR
        if not isinstance(inr, (int, float)):
            raise ValueError("INR must be a number")
        
        if inr < 0.5 or inr > 10.0:
            raise ValueError("INR must be between 0.5 and 10.0")
        
        # Validate mental status
        if not isinstance(mental_status_altered, str):
            raise ValueError("Mental status altered must be a string")
        
        if mental_status_altered.lower() not in ['yes', 'no']:
            raise ValueError("Mental status altered must be 'yes' or 'no'")
        
        # Validate systolic BP
        if not isinstance(systolic_bp, int):
            raise ValueError("Systolic BP must be an integer")
        
        if systolic_bp < 50 or systolic_bp > 250:
            raise ValueError("Systolic BP must be between 50 and 250 mmHg")
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
    
    def _calculate_components(self, albumin: float, inr: float, mental_status_altered: str, 
                            systolic_bp: int, age: int) -> Dict[str, int]:
        """Calculates individual AIMS65 components"""
        
        components = {}
        
        # A: Albumin <3.0 g/dL
        components["albumin_low"] = 1 if albumin < 3.0 else 0
        
        # I: INR >1.5
        components["inr_elevated"] = 1 if inr > 1.5 else 0
        
        # M: Mental status altered
        components["mental_status_altered"] = 1 if mental_status_altered.lower() == 'yes' else 0
        
        # S: Systolic BP ≤90 mmHg
        components["systolic_bp_low"] = 1 if systolic_bp <= 90 else 0
        
        # 65: Age ≥65 years
        components["age_65_or_older"] = 1 if age >= 65 else 0
        
        return components
    
    def _get_interpretation(self, score: int, components: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the AIMS65 score
        
        Args:
            score (int): Total AIMS65 score
            components (Dict): Individual component scores
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine risk category
        risk_category = "Unknown"
        for category, (min_score, max_score) in self.RISK_CATEGORIES.items():
            if min_score <= score <= max_score:
                risk_category = category
                break
        
        # Get mortality rate
        mortality_rate = self.MORTALITY_RATES.get(score, 50.0)
        
        # Build interpretation text
        interpretation_parts = []
        
        # Score and risk level
        interpretation_parts.append(f"AIMS65 score: {score}/5 points ({risk_category}).")
        
        # Mortality risk
        interpretation_parts.append(f"Estimated in-hospital mortality risk: {mortality_rate}%.")
        
        # Component breakdown
        positive_components = []
        if components["albumin_low"]:
            positive_components.append("Albumin <3.0 g/dL")
        if components["inr_elevated"]:
            positive_components.append("INR >1.5")
        if components["mental_status_altered"]:
            positive_components.append("Mental status altered")
        if components["systolic_bp_low"]:
            positive_components.append("Systolic BP ≤90 mmHg")
        if components["age_65_or_older"]:
            positive_components.append("Age ≥65 years")
        
        if positive_components:
            interpretation_parts.append(f"Positive criteria: {', '.join(positive_components)}.")
        else:
            interpretation_parts.append("No positive criteria present.")
        
        # Clinical recommendations
        if score <= 1:
            interpretation_parts.append(
                "LOW RISK: Consider outpatient management or early discharge for stable patients. "
                "Routine monitoring may be sufficient."
            )
            stage = "Low Risk"
            description = "Low mortality risk"
        elif score == 2:
            interpretation_parts.append(
                "MODERATE RISK: Consider inpatient monitoring and early endoscopy. "
                "Increased vigilance and prompt intervention if clinical deterioration."
            )
            stage = "Moderate Risk"
            description = "Moderate mortality risk"
        else:  # score >= 3
            interpretation_parts.append(
                "HIGH RISK: Requires intensive monitoring, urgent endoscopy, and aggressive management. "
                "Consider ICU admission and multidisciplinary care."
            )
            stage = "High Risk"
            description = "High mortality risk"
        
        # Additional clinical context
        interpretation_parts.append(
            "AIMS65 score helps guide triage decisions and resource allocation in upper GI bleeding."
        )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": " ".join(interpretation_parts),
            "risk_category": risk_category
        }


def calculate_aims65(albumin: float, inr: float, mental_status_altered: str,
                    systolic_bp: int, age: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_aims65 pattern
    """
    calculator = Aims65Calculator()
    return calculator.calculate(
        albumin=albumin,
        inr=inr,
        mental_status_altered=mental_status_altered,
        systolic_bp=systolic_bp,
        age=age
    )