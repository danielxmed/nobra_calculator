"""
Wells' Criteria for Pulmonary Embolism Calculator

Clinical pretest probability score for pulmonary embolism using seven bedside criteria.

References (Vancouver style):
1. Wells PS, Anderson DR, Rodger M, et al. Excluding pulmonary embolism at the bedside without
   diagnostic imaging: management of patients with suspected pulmonary embolism presenting to the
   emergency department by using a simple clinical model and D-dimer. Ann Intern Med. 2001;135(2):98-107.
2. van Belle A, Büller HR, Huisman MV, et al. Effectiveness of managing suspected pulmonary embolism
   using an algorithm combining clinical probability, D-dimer testing, and computed tomography. JAMA.
   2006;295(2):172-179.
3. Konstantinides SV, Meyer G, Becattini C, et al. 2019 ESC Guidelines for the diagnosis and management
   of acute pulmonary embolism. Eur Heart J. 2020;41(4):543-603.
"""

from typing import Dict, Any


class WellsCriteriaPeCalculator:
    """Calculator for Wells' Criteria for Pulmonary Embolism"""

    def __init__(self):
        # Point values per item (floats due to 1.5-point items)
        self.ITEM_POINTS: Dict[str, float] = {
            "clinical_signs_dvt": 3.0,
            "pe_most_likely": 3.0,
            "heart_rate_over_100": 1.5,
            "immobilization_surgery_recent": 1.5,
            "previous_dvt_pe": 1.5,
            "hemoptysis": 1.0,
            "active_malignancy": 1.0,
        }

        # 3-tier interpretation boundaries
        self.THREE_TIER = [
            {"min": 0.0, "max": 1.0, "stage": "Low Risk", "description": "Low clinical probability of PE"},
            {"min": 2.0, "max": 6.0, "stage": "Intermediate Risk", "description": "Intermediate clinical probability of PE"},
            {"min": 6.5, "max": 12.5, "stage": "High Risk", "description": "High clinical probability of PE"},
        ]

        # 2-tier threshold
        self.TWO_TIER_THRESHOLD = 4.0  # ≤4: PE unlikely; >4: PE likely

    def calculate(
        self,
        clinical_signs_dvt: str,
        pe_most_likely: str,
        heart_rate_over_100: str,
        immobilization_surgery_recent: str,
        previous_dvt_pe: str,
        hemoptysis: str,
        active_malignancy: str,
    ) -> Dict[str, Any]:
        """
        Calculates the Wells' PE score and provides clinical interpretation.

        Args:
            clinical_signs_dvt (str): Clinical signs and symptoms of DVT (yes/no)
            pe_most_likely (str): PE is the most likely diagnosis (yes/no)
            heart_rate_over_100 (str): Heart rate >100 bpm (yes/no)
            immobilization_surgery_recent (str): Immobilization ≥3 days or surgery within 4 weeks (yes/no)
            previous_dvt_pe (str): Previous DVT or PE (yes/no)
            hemoptysis (str): Hemoptysis (yes/no)
            active_malignancy (str): Active cancer (yes/no)

        Returns:
            Dict with result in points and evidence-based interpretation (3-tier plus 2-tier label)
        """

        params = {
            "clinical_signs_dvt": clinical_signs_dvt,
            "pe_most_likely": pe_most_likely,
            "heart_rate_over_100": heart_rate_over_100,
            "immobilization_surgery_recent": immobilization_surgery_recent,
            "previous_dvt_pe": previous_dvt_pe,
            "hemoptysis": hemoptysis,
            "active_malignancy": active_malignancy,
        }

        self._validate_inputs(params)

        score = self._compute_score(params)
        three_tier = self._three_tier_interpretation(score, params)
        two_tier_label = self._two_tier_label(score)

        # Compose an interpretation text consistent with existing style
        interpretation_text = (
            f"Wells' Criteria: {score:.1f} points. {three_tier['risk_factors']}"
            f"{three_tier['base_interpretation']} "
            f"Two-tier classification: {two_tier_label}. "
            f"Management: {three_tier['management']}"
        )

        return {
            "result": round(score, 1),
            "unit": "points",
            "interpretation": interpretation_text,
            "stage": three_tier["stage"],
            "stage_description": three_tier["description"],
            "two_tier": two_tier_label,
        }

    def _validate_inputs(self, params: Dict[str, str]) -> None:
        valid = {"yes", "no"}
        for key, val in params.items():
            if val not in valid:
                raise ValueError(f"{key} must be 'yes' or 'no'")

    def _compute_score(self, params: Dict[str, str]) -> float:
        total = 0.0
        for key, pts in self.ITEM_POINTS.items():
            if params.get(key) == "yes":
                total += pts
        return total

    def _three_tier_interpretation(self, score: float, params: Dict[str, str]) -> Dict[str, str]:
        # Build risk factor summary
        names = {
            "clinical_signs_dvt": "clinical signs of DVT (3.0)",
            "pe_most_likely": "PE most likely diagnosis (3.0)",
            "heart_rate_over_100": "heart rate >100 bpm (1.5)",
            "immobilization_surgery_recent": "immobilization ≥3 days or recent surgery (1.5)",
            "previous_dvt_pe": "previous DVT/PE (1.5)",
            "hemoptysis": "hemoptysis (1.0)",
            "active_malignancy": "active malignancy (1.0)",
        }
        present = [desc for key, desc in names.items() if params.get(key) == "yes"]
        risk_factors = (
            f"Present risk factors: {', '.join(present)}. " if present else "No positive Wells items. "
        )

        # Determine 3-tier stage
        for bucket in self.THREE_TIER:
            if score >= bucket["min"] and score <= bucket["max"]:
                stage = bucket["stage"]
                description = bucket["description"]
                break
        else:
            # Fallback, though score should always be within defined range
            stage = "Intermediate Risk"
            description = "Intermediate clinical probability of PE"

        if stage == "Low Risk":
            base = (
                "Low clinical probability of pulmonary embolism. Recommend D-dimer testing; "
                "if negative, PE is effectively ruled out; if positive, proceed to CT pulmonary angiography (CT-PA)."
            )
            management = (
                "Order D-dimer first. If negative, no imaging needed. If positive, obtain CT-PA. "
                "Consider age-adjusted D-dimer in patients >50 years."
            )
        elif stage == "Intermediate Risk":
            base = (
                "Intermediate clinical probability of pulmonary embolism. D-dimer testing recommended; "
                "if negative, PE is unlikely; if positive, CT-PA is recommended."
            )
            management = (
                "Obtain D-dimer; if positive, proceed to CT-PA. Interpret in clinical context; consider alternatives if negative."
            )
        else:
            base = (
                "High clinical probability of pulmonary embolism. Proceed directly to definitive imaging. "
                "D-dimer testing is not necessary at high pretest probability."
            )
            management = (
                "Obtain urgent CT-PA. If CT-PA contraindicated, consider V/Q scan. Consider empiric anticoagulation if bleeding risk is low."
            )

        return {
            "stage": stage,
            "description": description,
            "risk_factors": risk_factors,
            "base_interpretation": base,
            "management": management,
        }

    def _two_tier_label(self, score: float) -> str:
        return "PE Unlikely" if score <= self.TWO_TIER_THRESHOLD else "PE Likely"


def calculate_wells_criteria_pe(
    clinical_signs_dvt: str,
    pe_most_likely: str,
    heart_rate_over_100: str,
    immobilization_surgery_recent: str,
    previous_dvt_pe: str,
    hemoptysis: str,
    active_malignancy: str,
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system

    IMPORTANT: This function must follow the calculate_wells_criteria_pe pattern
    """
    calculator = WellsCriteriaPeCalculator()
    return calculator.calculate(
        clinical_signs_dvt,
        pe_most_likely,
        heart_rate_over_100,
        immobilization_surgery_recent,
        previous_dvt_pe,
        hemoptysis,
        active_malignancy,
    )

