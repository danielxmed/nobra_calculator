"""
Villalta Score for Post-thrombotic Syndrome (PTS) Calculator

Diagnoses and stratifies severity of post-thrombotic syndrome in patients with history 
of deep venous thrombosis (DVT).

References:
1. Villalta S, Bagatella P, Piccioli A, et al. Assessment of validity and reproducibility 
   of a clinical scale for the post-thrombotic syndrome. Haemostasis. 1994;24(4):158a.
2. Kahn SR, Partsch H, Vedantham S, et al. Definition of post-thrombotic syndrome of the 
   leg for use in clinical investigations: a recommendation for standardization. 
   J Thromb Haemost. 2009;7(5):879-883.
3. Soosainathan A, Moore HM, Gohel MS, et al. Scoring systems for the post-thrombotic 
   syndrome. J Vasc Surg. 2013;57(1):254-261.
"""

from typing import Dict, Any


class VillaltaScoreCalculator:
    """Calculator for Villalta Score for Post-thrombotic Syndrome"""
    
    def __init__(self):
        # Villalta Score parameters
        self.SYMPTOMS = ["pain", "cramps", "heaviness", "paresthesia", "pruritus"]
        self.CLINICAL_SIGNS = ["pretibial_edema", "skin_induration", "hyperpigmentation", 
                              "redness", "venous_ectasia", "calf_compression_pain"]
        
        # Severity thresholds
        self.SEVERITY_THRESHOLDS = {
            (0, 4): ("PTS Absent", "No post-thrombotic syndrome"),
            (5, 9): ("Mild PTS", "Mild post-thrombotic syndrome"),
            (10, 14): ("Moderate PTS", "Moderate post-thrombotic syndrome"),
            (15, 33): ("Severe PTS", "Severe post-thrombotic syndrome")
        }
    
    def calculate(self, pain: int, cramps: int, heaviness: int, paresthesia: int, 
                 pruritus: int, pretibial_edema: int, skin_induration: int,
                 hyperpigmentation: int, redness: int, venous_ectasia: int,
                 calf_compression_pain: int, venous_ulcer_present: str) -> Dict[str, Any]:
        """
        Calculates the Villalta Score for Post-thrombotic Syndrome
        
        Args:
            pain (int): Patient-reported pain severity (0-3)
            cramps (int): Patient-reported cramping severity (0-3)
            heaviness (int): Patient-reported heaviness severity (0-3)
            paresthesia (int): Patient-reported paresthesia severity (0-3)
            pruritus (int): Patient-reported itching severity (0-3)
            pretibial_edema (int): Physician-assessed pretibial edema (0-3)
            skin_induration (int): Physician-assessed skin induration (0-3)
            hyperpigmentation (int): Physician-assessed hyperpigmentation (0-3)
            redness (int): Physician-assessed redness (0-3)
            venous_ectasia (int): Physician-assessed venous ectasia (0-3)
            calf_compression_pain (int): Physician-assessed calf compression pain (0-3)
            venous_ulcer_present (str): Presence of venous ulcer ("yes"/"no")
            
        Returns:
            Dict with Villalta score, PTS severity, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pain, cramps, heaviness, paresthesia, pruritus,
                            pretibial_edema, skin_induration, hyperpigmentation,
                            redness, venous_ectasia, calf_compression_pain,
                            venous_ulcer_present)
        
        # Calculate symptom score (patient-reported)
        symptom_score = pain + cramps + heaviness + paresthesia + pruritus
        
        # Calculate clinical sign score (physician-assessed)
        sign_score = (pretibial_edema + skin_induration + hyperpigmentation + 
                     redness + venous_ectasia + calf_compression_pain)
        
        # Calculate total score
        total_score = symptom_score + sign_score
        
        # Apply venous ulcer rule (if present, automatically severe PTS)
        if venous_ulcer_present.lower() == "yes" and total_score < 15:
            total_score = 15
            ulcer_adjustment = True
        else:
            ulcer_adjustment = False
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, ulcer_adjustment)
        
        # Create component breakdown
        component_breakdown = {
            "symptom_score": symptom_score,
            "sign_score": sign_score,
            "venous_ulcer_present": venous_ulcer_present.lower() == "yes",
            "ulcer_adjustment_applied": ulcer_adjustment,
            "symptoms": {
                "pain": pain,
                "cramps": cramps,
                "heaviness": heaviness,
                "paresthesia": paresthesia,
                "pruritus": pruritus
            },
            "clinical_signs": {
                "pretibial_edema": pretibial_edema,
                "skin_induration": skin_induration,
                "hyperpigmentation": hyperpigmentation,
                "redness": redness,
                "venous_ectasia": venous_ectasia,
                "calf_compression_pain": calf_compression_pain
            }
        }
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_breakdown": component_breakdown
        }
    
    def _validate_inputs(self, pain: int, cramps: int, heaviness: int, paresthesia: int,
                        pruritus: int, pretibial_edema: int, skin_induration: int,
                        hyperpigmentation: int, redness: int, venous_ectasia: int,
                        calf_compression_pain: int, venous_ulcer_present: str):
        """Validates input parameters"""
        
        # List of all score parameters for validation
        score_params = [
            ("pain", pain), ("cramps", cramps), ("heaviness", heaviness),
            ("paresthesia", paresthesia), ("pruritus", pruritus),
            ("pretibial_edema", pretibial_edema), ("skin_induration", skin_induration),
            ("hyperpigmentation", hyperpigmentation), ("redness", redness),
            ("venous_ectasia", venous_ectasia), ("calf_compression_pain", calf_compression_pain)
        ]
        
        # Validate each score parameter (0-3 range)
        for param_name, param_value in score_params:
            if not isinstance(param_value, int) or param_value < 0 or param_value > 3:
                raise ValueError(f"{param_name} must be an integer between 0 and 3")
        
        # Validate venous ulcer parameter
        if venous_ulcer_present.lower() not in ["yes", "no"]:
            raise ValueError("venous_ulcer_present must be 'yes' or 'no'")
    
    def _get_interpretation(self, total_score: int, ulcer_adjustment: bool) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Villalta score
        
        Args:
            total_score (int): Calculated Villalta score
            ulcer_adjustment (bool): Whether score was adjusted due to venous ulcer
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine severity category
        stage, description = None, None
        for (min_score, max_score), (severity, desc) in self.SEVERITY_THRESHOLDS.items():
            if min_score <= total_score <= max_score:
                stage = severity
                description = desc
                break
        
        # Generate detailed interpretation
        ulcer_note = ""
        if ulcer_adjustment:
            ulcer_note = " Score adjusted to 15 due to presence of venous ulcer (automatic severe PTS classification)."
        
        if stage == "PTS Absent":
            interpretation = (f"Villalta score of {total_score} indicates absence of post-thrombotic syndrome. "
                            f"Continue routine follow-up for DVT patients. Monitor for development of PTS symptoms "
                            f"over time, as PTS can develop months to years after initial DVT. Encourage leg "
                            f"elevation, exercise, and compression stockings for prevention.{ulcer_note}")
        
        elif stage == "Mild PTS":
            interpretation = (f"Villalta score of {total_score} indicates mild post-thrombotic syndrome. "
                            f"Initiate conservative management including compression therapy (20-30 mmHg), "
                            f"leg elevation, regular exercise, weight management, and patient education about "
                            f"PTS. Regular follow-up to monitor progression and symptom response to treatment.{ulcer_note}")
        
        elif stage == "Moderate PTS":
            interpretation = (f"Villalta score of {total_score} indicates moderate post-thrombotic syndrome. "
                            f"Intensify conservative management with higher-grade compression stockings (30-40 mmHg), "
                            f"structured exercise programs, weight management, and skin care. Consider referral to "
                            f"vascular specialist for evaluation of additional interventions. Monitor quality of life impact.{ulcer_note}")
        
        else:  # Severe PTS
            interpretation = (f"Villalta score of {total_score} indicates severe post-thrombotic syndrome. "
                            f"Requires intensive management and specialist referral to vascular surgery or "
                            f"interventional radiology. Consider advanced therapies including intermittent pneumatic "
                            f"compression, venous stenting/angioplasty, and comprehensive ulcer care if present. "
                            f"Significant impact on quality of life requiring multidisciplinary approach.{ulcer_note}")
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }


def calculate_villalta_score(pain: int, cramps: int, heaviness: int, paresthesia: int,
                           pruritus: int, pretibial_edema: int, skin_induration: int,
                           hyperpigmentation: int, redness: int, venous_ectasia: int,
                           calf_compression_pain: int, venous_ulcer_present: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_villalta_score pattern
    """
    calculator = VillaltaScoreCalculator()
    return calculator.calculate(pain, cramps, heaviness, paresthesia, pruritus,
                              pretibial_edema, skin_induration, hyperpigmentation,
                              redness, venous_ectasia, calf_compression_pain,
                              venous_ulcer_present)