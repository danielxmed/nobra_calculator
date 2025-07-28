"""ACEF II Risk Score Calculator

Calculates predicted operative mortality risk after cardiac surgery
based on age, ejection fraction, serum creatinine, emergency status,
and pre-operative anemia.

Reference: Ranucci M et al. Eur Heart J. 2018;39(23):2183-2189.
"""

from typing import Dict, Any


class AcefIiCalculator:
    """Calculator for ACEF II Risk Score"""

    def calculate(self, age: int, ejection_fraction: float, serum_creatinine: float,
                 emergency_surgery: bool, hematocrit: float) -> Dict[str, Any]:
        self._validate_inputs(age, ejection_fraction, serum_creatinine, hematocrit)

        score = age / ejection_fraction

        if serum_creatinine > 2:
            score += 2

        if emergency_surgery:
            score += 3

        if hematocrit < 36:
            score += 0.2 * (36 - hematocrit)

        score = round(score, 2)

        interpretation = self._get_interpretation(score)

        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
        }

    def _validate_inputs(self, age: int, ef: float, creat: float, hct: float):
        if not 18 <= age <= 100:
            raise ValueError("Age must be between 18 and 100 years")
        if not 10 <= ef <= 80:
            raise ValueError("Ejection fraction must be between 10 and 80%")
        if creat <= 0 or creat > 20:
            raise ValueError("Serum creatinine must be between 0 and 20 mg/dL")
        if not 15 <= hct <= 60:
            raise ValueError("Hematocrit must be between 15 and 60%")

    def _get_interpretation(self, score: float) -> Dict[str, str]:
        if score < 2:
            return {
                "stage": "Low Risk",
                "description": "Estimated mortality <2%",
                "interpretation": "Standard perioperative management.",
            }
        elif score < 3:
            return {
                "stage": "Intermediate Risk",
                "description": "Estimated mortality 2-5%",
                "interpretation": "Optimize comorbidities and monitor carefully.",
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Estimated mortality >5%",
                "interpretation": "Enhanced monitoring and risk-benefit discussion recommended.",
            }


def calculate_acef_ii(age: int, ejection_fraction: float, serum_creatinine: float,
                      emergency_surgery: bool, hematocrit: float) -> Dict[str, Any]:
    """Convenience wrapper for dynamic loader"""
    calc = AcefIiCalculator()
    return calc.calculate(age, ejection_fraction, serum_creatinine, emergency_surgery, hematocrit)
