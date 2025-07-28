"""ACEP ED COVID-19 Management Tool Calculator

Simplified implementation of the ACEP Emergency Department COVID-19 Management Tool (Fall 2023).
Determines recommended disposition for adult patients with suspected or confirmed SARS-CoV-2
based on severity, PRIEST score, and risk factor assessment.

Reference: American College of Emergency Physicians. ACEP Emergency Department COVID-19 Management Tool. Fall 2023.
"""

from typing import Dict, Any


class AcepEdCovid19ManagementToolCalculator:
    """Calculator for ACEP ED COVID-19 Management Tool"""

    VALID_SEVERITIES = ["mild", "moderate", "severe", "critical"]

    def calculate(
        self,
        severity: str,
        priest_score: int,
        risk_factors: int,
        imaging_concerning: bool,
        labs_concerning: bool,
        self_care_capable: bool,
    ) -> Dict[str, Any]:
        self._validate_inputs(
            severity,
            priest_score,
            risk_factors,
            imaging_concerning,
            labs_concerning,
            self_care_capable,
        )

        disposition = self._determine_disposition(
            severity,
            priest_score,
            risk_factors,
            imaging_concerning,
            labs_concerning,
            self_care_capable,
        )

        interpretation = self._get_interpretation(disposition)

        return {
            "result": disposition["stage"],
            "unit": "disposition",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
        }

    def _validate_inputs(
        self,
        severity: str,
        priest_score: int,
        risk_factors: int,
        imaging_concerning: bool,
        labs_concerning: bool,
        self_care_capable: bool,
    ) -> None:
        if severity not in self.VALID_SEVERITIES:
            raise ValueError("Severity must be 'mild', 'moderate', 'severe', or 'critical'")
        if not isinstance(priest_score, int) or not 0 <= priest_score <= 30:
            raise ValueError("PRIEST score must be between 0 and 30")
        if not isinstance(risk_factors, int) or not 0 <= risk_factors <= 20:
            raise ValueError("Risk factors must be between 0 and 20")
        if not isinstance(imaging_concerning, bool):
            raise ValueError("imaging_concerning must be boolean")
        if not isinstance(labs_concerning, bool):
            raise ValueError("labs_concerning must be boolean")
        if not isinstance(self_care_capable, bool):
            raise ValueError("self_care_capable must be boolean")

    def _determine_disposition(
        self,
        severity: str,
        priest_score: int,
        risk_factors: int,
        imaging_concerning: bool,
        labs_concerning: bool,
        self_care_capable: bool,
    ) -> Dict[str, str]:
        if severity == "critical":
            return {"stage": "ICU"}
        if severity == "severe":
            return {"stage": "Admission"}

        # mild or moderate
        if (
            severity == "mild"
            and priest_score <= 4
            and risk_factors <= 1
            and not imaging_concerning
            and not labs_concerning
            and self_care_capable
        ):
            return {"stage": "Discharge"}
        return {"stage": "Admission/Observation"}

    def _get_interpretation(self, disposition: Dict[str, str]) -> Dict[str, str]:
        stage = disposition["stage"]
        if stage == "ICU":
            return {
                "stage": "ICU",
                "description": "Critical illness requiring intensive care",
                "interpretation": "Immediate ICU admission. Consider transfer for ECMO or advanced therapies.",
            }
        if stage == "Admission":
            return {
                "stage": "Admission",
                "description": "Severe disease requiring hospitalization",
                "interpretation": "Hospital admission recommended; level of care based on clinical judgment.",
            }
        if stage == "Discharge":
            return {
                "stage": "Discharge",
                "description": "Mild disease with low risk of progression",
                "interpretation": "Safe for discharge with return precautions and follow-up.",
            }
        return {
            "stage": "Admission/Observation",
            "description": "Mild or moderate illness with risk factors",
            "interpretation": "Consider admission or observation depending on risk assessment and resources.",
        }


def calculate_acep_ed_covid19_management_tool(
    severity: str,
    priest_score: int,
    risk_factors: int,
    imaging_concerning: bool,
    labs_concerning: bool,
    self_care_capable: bool,
) -> Dict[str, Any]:
    """Convenience wrapper for dynamic import system"""
    calc = AcepEdCovid19ManagementToolCalculator()
    return calc.calculate(
        severity,
        priest_score,
        risk_factors,
        imaging_concerning,
        labs_concerning,
        self_care_capable,
    )
