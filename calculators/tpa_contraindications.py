"""
tPA Contraindications for Ischemic Stroke Calculator

Evaluates eligibility and contraindications for thrombolytic therapy with IV tPA
in acute ischemic stroke patients based on AHA/ASA guidelines.

References:
1. Powers WJ, et al. 2019 Update to the 2018 Guidelines for the Early Management 
   of Acute Ischemic Stroke. Stroke. 2019;50(12):e344-e418.
2. Hacke W, et al. Thrombolysis with alteplase 3 to 4.5 hours after acute 
   ischemic stroke. N Engl J Med. 2008;359(13):1317-29.
"""

from typing import Dict, Any, List, Tuple


class TpaContraindicationsCalculator:
    """Calculator for tPA contraindications in ischemic stroke"""
    
    def __init__(self):
        # Absolute contraindications that apply regardless of time window
        self.absolute_contraindications_all_times = [
            "ischemic_stroke_within_3_months",
            "severe_head_trauma_within_3_months", 
            "intracranial_surgery_within_3_months",
            "history_intracranial_hemorrhage",
            "subarachnoid_hemorrhage",
            "gi_malignancy_bleeding_21_days",
            "coagulopathy",
            "infective_endocarditis",
            "aortic_dissection",
            "neoplasm_increased_bleeding",
            "ct_ich",
            "sbp_greater_185",
            "dbp_greater_110"
        ]
        
        # Additional absolute contraindications for standard window
        self.absolute_contraindications_standard = [
            "inr_greater_1_7",
            "aptt_greater_40",
            "platelet_count_less_100k",
            "tc_48h_lmwh",
            "thrombin_factor_xa_inhibitors",
            "glucose_less_50"
        ]
        
        # Additional absolute contraindications for extended window (3-4.5h)
        self.absolute_contraindications_extended = [
            "ct_hypodensity_one_third"
        ]
        
        # Relative contraindications
        self.relative_contraindications = [
            "minor_symptoms",
            "symptoms_clearing",
            "pregnancy",
            "seizure_at_onset",
            "major_surgery_14_days",
            "gi_hemorrhage_21_days",
            "mi_within_3_months"
        ]
    
    def calculate(self, **params) -> Dict[str, Any]:
        """
        Evaluates tPA eligibility based on contraindications
        
        Returns:
            Dict with eligibility status and detailed contraindications
        """
        
        # Check time window first
        time_window = params.get("symptom_onset_time")
        if time_window == "over_4_5_hours" or time_window == "unknown":
            return {
                "result": "Absolute Contraindication - Outside Time Window",
                "unit": "",
                "interpretation": "Patient is outside the approved time window for IV tPA (>4.5 hours or unknown time of onset). Consider mechanical thrombectomy if large vessel occlusion is present.",
                "stage": "Absolute Contraindication",
                "stage_description": "Outside therapeutic window",
                "absolute_contraindications": ["Time window >4.5 hours or unknown"],
                "relative_contraindications": []
            }
        
        # Check for absolute contraindications
        absolute_contraindications = self._check_absolute_contraindications(params, time_window)
        
        # Check for relative contraindications
        relative_contraindications = self._check_relative_contraindications(params, time_window)
        
        # Determine eligibility
        eligibility, interpretation = self._determine_eligibility(
            absolute_contraindications, 
            relative_contraindications,
            time_window
        )
        
        return {
            "result": eligibility,
            "unit": "",
            "interpretation": interpretation,
            "stage": self._get_stage(absolute_contraindications, relative_contraindications),
            "stage_description": self._get_stage_description(absolute_contraindications, relative_contraindications),
            "absolute_contraindications": absolute_contraindications,
            "relative_contraindications": relative_contraindications
        }
    
    def _check_absolute_contraindications(self, params: Dict[str, Any], time_window: str) -> List[str]:
        """Check for absolute contraindications based on time window"""
        contraindications = []
        
        # Check contraindications that apply to all time windows
        for param in self.absolute_contraindications_all_times:
            if params.get(param) == "yes":
                contraindications.append(self._format_contraindication(param))
        
        # Check standard window contraindications (0-4.5h)
        for param in self.absolute_contraindications_standard:
            if params.get(param) == "yes":
                contraindications.append(self._format_contraindication(param))
        
        # Additional checks for extended window (3-4.5h)
        if time_window == "3_to_4_5_hours":
            # Age >80 in extended window
            if params.get("age", 0) > 80:
                contraindications.append("Age >80 years (extended window)")
            
            # Additional imaging criteria
            for param in self.absolute_contraindications_extended:
                if params.get(param) == "yes":
                    contraindications.append(self._format_contraindication(param))
        
        return contraindications
    
    def _check_relative_contraindications(self, params: Dict[str, Any], time_window: str) -> List[str]:
        """Check for relative contraindications"""
        contraindications = []
        
        for param in self.relative_contraindications:
            if params.get(param) == "yes":
                contraindications.append(self._format_contraindication(param))
        
        return contraindications
    
    def _determine_eligibility(self, absolute: List[str], relative: List[str], time_window: str) -> Tuple[str, str]:
        """Determine eligibility and provide interpretation"""
        
        if absolute:
            result = f"Absolute Contraindication{'s' if len(absolute) > 1 else ''} Present"
            interpretation = (
                f"IV tPA is contraindicated due to: {', '.join(absolute)}. "
                "These represent unacceptable bleeding risks. Consider mechanical thrombectomy "
                "if large vessel occlusion is present and patient meets criteria."
            )
        elif relative:
            result = f"Relative Contraindication{'s' if len(relative) > 1 else ''} Present"
            interpretation = (
                f"Relative contraindications identified: {', '.join(relative)}. "
                "Carefully weigh risks and benefits. Consider consultation with stroke specialist. "
                "Document thorough informed consent discussion if proceeding with tPA."
            )
        else:
            result = "Eligible for tPA"
            window_text = "within 3 hours" if time_window == "within_3_hours" else "3-4.5 hour window"
            interpretation = (
                f"No contraindications identified for IV tPA administration ({window_text}). "
                "Proceed with standard dosing: 0.9 mg/kg (maximum 90 mg), with 10% as bolus "
                "over 1 minute and remainder infused over 60 minutes. Monitor closely for bleeding."
            )
        
        return result, interpretation
    
    def _get_stage(self, absolute: List[str], relative: List[str]) -> str:
        """Get the stage based on contraindications"""
        if absolute:
            return "Absolute Contraindication"
        elif relative:
            return "Relative Contraindication"
        else:
            return "Eligible"
    
    def _get_stage_description(self, absolute: List[str], relative: List[str]) -> str:
        """Get stage description"""
        if absolute:
            return f"{len(absolute)} absolute contraindication{'s' if len(absolute) > 1 else ''}"
        elif relative:
            return f"{len(relative)} relative contraindication{'s' if len(relative) > 1 else ''}"
        else:
            return "No contraindications"
    
    def _format_contraindication(self, param: str) -> str:
        """Format parameter name into readable contraindication"""
        formatting = {
            "ischemic_stroke_within_3_months": "Ischemic stroke within 3 months",
            "severe_head_trauma_within_3_months": "Severe head trauma within 3 months",
            "intracranial_surgery_within_3_months": "Intracranial/intraspinal surgery within 3 months",
            "history_intracranial_hemorrhage": "History of intracranial hemorrhage",
            "subarachnoid_hemorrhage": "Symptoms of subarachnoid hemorrhage",
            "gi_malignancy_bleeding_21_days": "GI malignancy or bleeding within 21 days",
            "coagulopathy": "Bleeding diathesis or coagulopathy",
            "inr_greater_1_7": "INR >1.7 or PT >15 seconds",
            "aptt_greater_40": "aPTT >40 seconds",
            "platelet_count_less_100k": "Platelet count <100,000/mm³",
            "tc_48h_lmwh": "Treatment dose LMWH within 24 hours",
            "thrombin_factor_xa_inhibitors": "Direct thrombin or factor Xa inhibitors",
            "glucose_less_50": "Blood glucose <50 mg/dL",
            "ct_ich": "CT shows intracranial hemorrhage",
            "ct_hypodensity_one_third": "CT shows multilobar infarction (>1/3 hemisphere)",
            "sbp_greater_185": "Systolic BP >185 mmHg",
            "dbp_greater_110": "Diastolic BP >110 mmHg",
            "infective_endocarditis": "Active infective endocarditis",
            "aortic_dissection": "Known or suspected aortic dissection",
            "neoplasm_increased_bleeding": "Intracranial neoplasm with bleeding risk",
            "minor_symptoms": "Minor and non-disabling symptoms only",
            "symptoms_clearing": "Symptoms clearing spontaneously",
            "pregnancy": "Pregnancy",
            "seizure_at_onset": "Seizure at onset with postictal deficits",
            "major_surgery_14_days": "Major surgery or trauma within 14 days",
            "gi_hemorrhage_21_days": "GI or urinary hemorrhage within 21 days",
            "mi_within_3_months": "Acute MI within 3 months"
        }
        return formatting.get(param, param.replace("_", " ").title())


def calculate_tpa_contraindications(**params) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TpaContraindicationsCalculator()
    return calculator.calculate(**params)