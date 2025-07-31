"""
GWTG-Heart Failure Risk Score Calculator

The GWTG-Heart Failure Risk Score predicts all-cause in-hospital mortality in 
admitted patients with heart failure. This validated tool was developed using 
the American Heart Association Get With The Guidelines-Heart Failure (GWTG-HF) 
program data and demonstrates good discriminative ability with a C-index of 0.75.

The calculator helps clinicians identify heart failure patients at highest risk 
of in-hospital mortality, enabling targeted interventions, appropriate care 
intensity decisions, and informed discussions with patients and families.

Clinical Applications:
- Risk stratification for hospitalized heart failure patients
- Patient and family counseling about prognosis
- Decision-making for intensity of monitoring and care
- Resource allocation and care planning
- Quality improvement and outcome prediction

References (Vancouver style):
1. Peterson PN, Rumsfeld JS, Liang L, et al. A validated risk score for in-hospital 
   mortality in patients with heart failure from the American Heart Association get 
   with the guidelines program. Circ Cardiovasc Qual Outcomes. 2010;3(1):25-32. 
   doi: 10.1161/CIRCOUTCOMES.109.854877
2. Fonarow GC, Adams KF Jr, Abraham WT, Yancy CW, Boscardin WJ; ADHERE Scientific 
   Advisory Committee, Study Group, and Investigators. Risk stratification for 
   in-hospital mortality in acutely decompensated heart failure: classification 
   and regression tree analysis. JAMA. 2005;293(5):572-580.
3. American Heart Association Get With The Guidelines - Heart Failure Program. 
   https://www.heart.org/en/professional/quality-improvement/get-with-the-guidelines
"""

import math
from typing import Dict, Any


class GwtgHeartFailureRiskScoreCalculator:
    """Calculator for GWTG-Heart Failure Risk Score"""
    
    def __init__(self):
        # Age scoring (points per year increment)
        self.AGE_COEFFICIENT = 0.7
        
        # Systolic BP scoring (protective when higher)
        self.SYSTOLIC_BP_COEFFICIENT = -0.08
        
        # BUN scoring (risk increases with higher values)
        self.BUN_COEFFICIENT = 0.3
        
        # Heart rate scoring (risk increases with higher rates)
        self.HEART_RATE_COEFFICIENT = 0.08
        
        # Sodium scoring (protective when higher)
        self.SODIUM_COEFFICIENT = -0.5
        
        # COPD points
        self.COPD_POINTS = {
            "no": 0,
            "yes": 2
        }
        
        # Race points (black race is protective)
        self.RACE_POINTS = {
            "no": 4,    # Non-black
            "yes": 1    # Black race (protective)
        }
        
        # Risk interpretation thresholds based on score ranges
        self.RISK_THRESHOLDS = [
            {"min": 0, "max": 33, "mortality": 1.0, "level": "Very Low Risk", "description": "Minimal mortality risk"},
            {"min": 34, "max": 50, "mortality": 3.0, "level": "Low Risk", "description": "Low mortality risk"},
            {"min": 51, "max": 57, "mortality": 7.5, "level": "Moderate Risk", "description": "Moderate mortality risk"},
            {"min": 58, "max": 61, "mortality": 12.5, "level": "High Risk", "description": "High mortality risk"},
            {"min": 62, "max": 65, "mortality": 17.5, "level": "High Risk", "description": "High mortality risk"},
            {"min": 66, "max": 70, "mortality": 25.0, "level": "Very High Risk", "description": "Very high mortality risk"},
            {"min": 71, "max": 74, "mortality": 35.0, "level": "Very High Risk", "description": "Very high mortality risk"},
            {"min": 75, "max": 78, "mortality": 45.0, "level": "Very High Risk", "description": "Very high mortality risk"},
            {"min": 79, "max": 100, "mortality": 55.0, "level": "Very High Risk", "description": "Very high mortality risk"}
        ]
    
    def calculate(self, age: int, systolic_bp: int, bun: int, heart_rate: int,
                 sodium: int, copd: str, black_race: str) -> Dict[str, Any]:
        """
        Calculates GWTG-Heart Failure Risk Score
        
        Args:
            age (int): Patient age in years
            systolic_bp (int): Systolic blood pressure in mmHg
            bun (int): Blood urea nitrogen in mg/dL
            heart_rate (int): Heart rate in bpm
            sodium (int): Serum sodium in mEq/L
            copd (str): History of COPD (no, yes)
            black_race (str): Black race (no, yes)
            
        Returns:
            Dict with mortality risk percentage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, systolic_bp, bun, heart_rate, sodium, copd, black_race)
        
        # Calculate score components
        age_points = (age - 65) * self.AGE_COEFFICIENT if age > 65 else 0
        systolic_points = (140 - systolic_bp) * self.SYSTOLIC_BP_COEFFICIENT if systolic_bp < 140 else 0
        bun_points = (bun - 20) * self.BUN_COEFFICIENT if bun > 20 else 0
        hr_points = (heart_rate - 70) * self.HEART_RATE_COEFFICIENT if heart_rate > 70 else 0
        sodium_points = (140 - sodium) * self.SODIUM_COEFFICIENT if sodium < 140 else 0
        copd_points = self.COPD_POINTS[copd]
        race_points = self.RACE_POINTS[black_race]
        
        # Calculate total score (0-100 range)
        total_score = max(0, min(100, 
            25 + age_points + abs(systolic_points) + bun_points + 
            hr_points + abs(sodium_points) + copd_points + race_points
        ))
        
        # Get risk interpretation
        interpretation = self._get_interpretation(total_score, age, systolic_bp, bun,
                                                heart_rate, sodium, copd, black_race)
        
        return {
            "result": round(interpretation["mortality"], 1),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["level"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, systolic_bp: int, bun: int, heart_rate: int,
                        sodium: int, copd: str, black_race: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 50 or systolic_bp > 300:
            raise ValueError("Systolic BP must be an integer between 50 and 300 mmHg")
        
        if not isinstance(bun, int) or bun < 5 or bun > 200:
            raise ValueError("BUN must be an integer between 5 and 200 mg/dL")
        
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 200:
            raise ValueError("Heart rate must be an integer between 30 and 200 bpm")
        
        if not isinstance(sodium, int) or sodium < 110 or sodium > 160:
            raise ValueError("Sodium must be an integer between 110 and 160 mEq/L")
        
        if copd not in self.COPD_POINTS:
            raise ValueError(f"COPD must be one of: {list(self.COPD_POINTS.keys())}")
        
        if black_race not in self.RACE_POINTS:
            raise ValueError(f"Black race must be one of: {list(self.RACE_POINTS.keys())}")
    
    def _get_interpretation(self, score: float, age: int, systolic_bp: int, bun: int,
                          heart_rate: int, sodium: int, copd: str, black_race: str) -> Dict[str, Any]:
        """
        Provides clinical interpretation based on GWTG-HF risk score
        
        Returns:
            Dict with risk level, mortality percentage, and clinical recommendations
        """
        
        # Find appropriate risk category
        risk_category = None
        for threshold in self.RISK_THRESHOLDS:
            if threshold["min"] <= score <= threshold["max"]:
                risk_category = threshold
                break
        
        if risk_category is None:
            risk_category = self.RISK_THRESHOLDS[-1]  # Default to highest risk
        
        # Build parameter summary
        copd_desc = "COPD present" if copd == "yes" else "no COPD"
        race_desc = "Black race" if black_race == "yes" else "non-Black race"
        
        parameter_summary = (
            f"Patient characteristics: {age} years old, systolic BP {systolic_bp} mmHg, "
            f"BUN {bun} mg/dL, heart rate {heart_rate} bpm, sodium {sodium} mEq/L, "
            f"{copd_desc}, {race_desc}. GWTG-HF Score: {score:.0f} points. "
        )
        
        # Generate risk-specific recommendations
        mortality_risk = risk_category["mortality"]
        
        if mortality_risk < 1.0:  # Very Low Risk
            recommendations = (
                "Very low risk of in-hospital mortality (<1%). Standard heart failure care "
                "protocols are appropriate. Continue evidence-based heart failure medications, "
                "monitor fluid status, and provide standard discharge planning with follow-up "
                "within 7-14 days of discharge."
            )
        elif mortality_risk < 5.0:  # Low Risk
            recommendations = (
                "Low risk of in-hospital mortality (1-5%). Standard care with attention to "
                "optimization of heart failure therapy. Ensure guideline-directed medical therapy "
                "is maximized, provide patient education, and consider cardiology follow-up "
                "within 1-2 weeks of discharge."
            )
        elif mortality_risk < 15.0:  # Moderate Risk
            recommendations = (
                "Moderate risk of in-hospital mortality (5-15%). Consider enhanced monitoring "
                "and aggressive heart failure management. Optimize diuretics, vasodilators, and "
                "neurohormonal blockade. Consider cardiology consultation, advanced heart failure "
                "evaluation, and closer outpatient follow-up within 3-7 days."
            )
        elif mortality_risk < 30.0:  # High Risk
            recommendations = (
                "High risk of in-hospital mortality (15-30%). Implement intensive monitoring "
                "and consider advanced therapies. Evaluate for advanced heart failure interventions "
                "including mechanical circulatory support, heart transplantation evaluation, or "
                "specialized heart failure care. Initiate palliative care discussions if appropriate."
            )
        else:  # Very High Risk
            recommendations = (
                "Very high risk of in-hospital mortality (>30%). Intensive care management "
                "with advanced heart failure therapies and end-of-life care planning discussions "
                "recommended. Consider ICU-level monitoring, inotropic support, mechanical "
                "circulatory support evaluation, and comprehensive palliative care involvement."
            )
        
        # Add important clinical considerations
        clinical_considerations = (
            "Important considerations: The GWTG-HF risk score provides validated in-hospital "
            "mortality prediction for heart failure patients. This score is applicable to patients "
            "with both preserved and reduced ejection fraction. Use in conjunction with clinical "
            "judgment for comprehensive heart failure management, advanced therapy consideration, "
            "and care planning discussions with patients and families."
        )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}Predicted in-hospital mortality risk: {mortality_risk:.1f}%. "
            f"Risk Category: {risk_category['level']} ({risk_category['description']}). "
            f"Clinical recommendations: {recommendations} {clinical_considerations}"
        )
        
        return {
            "level": risk_category["level"],
            "description": risk_category["description"],
            "mortality": mortality_risk,
            "interpretation": interpretation
        }


def calculate_gwtg_heart_failure_risk_score(age: int, systolic_bp: int, bun: int, 
                                          heart_rate: int, sodium: int, copd: str, 
                                          black_race: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gwtg_heart_failure_risk_score pattern
    """
    calculator = GwtgHeartFailureRiskScoreCalculator()
    return calculator.calculate(age, systolic_bp, bun, heart_rate, sodium, copd, black_race)