"""
Morphine Milligram Equivalents (MME) Calculator

Calculates total daily morphine milligram equivalents to assess opioid dosing,
guide safe prescribing practices, and evaluate overdose risk.

References:
1. Dowell D, et al. JAMA. 2016;315(15):1624-45.
2. CDC Clinical Practice Guideline for Prescribing Opioids for Pain — United States, 2022.
3. Nielsen S, et al. Pharmacoepidemiol Drug Saf. 2016;25(6):733-7.
"""

import json
from typing import Dict, Any, List


class MmeCalculator:
    """Calculator for Morphine Milligram Equivalents (MME)"""
    
    def __init__(self):
        # CDC 2022 Conversion Factors (oral morphine equivalents)
        self.CONVERSION_FACTORS = {
            # Opioid name: conversion factor to oral morphine
            "morphine_oral": 1.0,
            "morphine_iv": 3.0,  # IV morphine to oral morphine equivalent
            "oxycodone": 1.5,
            "hydrocodone": 1.0,
            "codeine": 0.15,
            "fentanyl_patch": 2.4,  # mcg/hr to mg/day oral morphine
            "fentanyl_oral": 0.13,  # Oral transmucosal fentanyl
            "hydromorphone_oral": 4.0,
            "hydromorphone_iv": 20.0,
            "oxymorphone_oral": 3.0,
            "oxymorphone_iv": 10.0,
            "methadone_1_20": 4.0,    # 1-20 mg/day
            "methadone_21_40": 8.0,   # 21-40 mg/day
            "methadone_41_60": 10.0,  # 41-60 mg/day
            "methadone_61_plus": 12.0, # >60 mg/day
            "tramadol": 0.1,
            "tapentadol": 0.4,
            "buprenorphine_patch": 12.6,  # mcg/hr to mg/day oral morphine
            "buprenorphine_sublingual": 30.0,
            "meperidine": 0.1,
            "pentazocine": 0.37
        }
        
        # Alternative medication names mapping
        self.MEDICATION_ALIASES = {
            "morphine": "morphine_oral",
            "ms_contin": "morphine_oral",
            "oxycontin": "oxycodone",
            "percocet": "oxycodone",
            "vicodin": "hydrocodone",
            "norco": "hydrocodone",
            "tylenol_3": "codeine",
            "duragesic": "fentanyl_patch",
            "dilaudid": "hydromorphone_oral",
            "opana": "oxymorphone_oral",
            "ultram": "tramadol",
            "nucynta": "tapentadol",
            "suboxone": "buprenorphine_sublingual",
            "butrans": "buprenorphine_patch",
            "demerol": "meperidine",
            "talwin": "pentazocine"
        }
    
    def calculate(self, opioid_medications: str) -> Dict[str, Any]:
        """
        Calculates total daily MME from multiple opioid medications
        
        Args:
            opioid_medications (str): JSON string of medication list
            
        Returns:
            Dict with total MME and risk interpretation
        """
        
        # Parse and validate medication list
        medications = self._parse_medications(opioid_medications)
        
        # Calculate MME for each medication
        total_mme = 0.0
        medication_details = []
        
        for med in medications:
            med_mme = self._calculate_single_mme(med)
            total_mme += med_mme
            
            medication_details.append({
                "medication": med["medication"],
                "dose": med["dose"],
                "frequency": med["frequency_per_day"],
                "route": med.get("route", "oral"),
                "daily_dose": med["dose"] * med["frequency_per_day"],
                "mme_contribution": med_mme
            })
        
        # Get risk interpretation
        interpretation = self._get_interpretation(total_mme, medication_details)
        
        return {
            "result": round(total_mme, 1),
            "unit": "mg/day morphine equivalents",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _parse_medications(self, medications_json: str) -> List[Dict]:
        """Parses and validates medication JSON input"""
        
        try:
            medications = json.loads(medications_json)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for opioid medications")
        
        if not isinstance(medications, list):
            raise ValueError("Medications must be provided as a JSON array")
        
        if not medications:
            raise ValueError("At least one opioid medication must be provided")
        
        # Validate each medication entry
        for i, med in enumerate(medications):
            if not isinstance(med, dict):
                raise ValueError(f"Medication {i+1} must be an object")
            
            required_fields = ["medication", "dose", "frequency_per_day"]
            for field in required_fields:
                if field not in med:
                    raise ValueError(f"Medication {i+1} missing required field: {field}")
            
            # Validate dose and frequency
            if not isinstance(med["dose"], (int, float)) or med["dose"] <= 0:
                raise ValueError(f"Medication {i+1} dose must be a positive number")
            
            if not isinstance(med["frequency_per_day"], (int, float)) or med["frequency_per_day"] <= 0:
                raise ValueError(f"Medication {i+1} frequency must be a positive number")
            
            # Normalize medication name
            med_name = med["medication"].lower().replace(" ", "_").replace("-", "_")
            if med_name in self.MEDICATION_ALIASES:
                med["medication"] = self.MEDICATION_ALIASES[med_name]
            else:
                med["medication"] = med_name
        
        return medications
    
    def _calculate_single_mme(self, medication: Dict) -> float:
        """Calculates MME for a single medication"""
        
        med_name = medication["medication"]
        dose = medication["dose"]
        frequency = medication["frequency_per_day"]
        route = medication.get("route", "oral").lower()
        
        # Handle special cases
        if med_name.startswith("methadone"):
            # Methadone has dose-dependent conversion factors
            daily_dose = dose * frequency
            if daily_dose <= 20:
                conversion_factor = self.CONVERSION_FACTORS["methadone_1_20"]
            elif daily_dose <= 40:
                conversion_factor = self.CONVERSION_FACTORS["methadone_21_40"]
            elif daily_dose <= 60:
                conversion_factor = self.CONVERSION_FACTORS["methadone_41_60"]
            else:
                conversion_factor = self.CONVERSION_FACTORS["methadone_61_plus"]
        
        elif med_name == "fentanyl_patch":
            # Fentanyl patch is dosed in mcg/hr, frequency should be 1 for 72-hour patch
            # Dose represents mcg/hr strength of patch
            conversion_factor = self.CONVERSION_FACTORS["fentanyl_patch"]
            # Don't multiply by frequency for patches (already continuous)
            return dose * conversion_factor
        
        elif med_name == "buprenorphine_patch":
            # Buprenorphine patch similar to fentanyl
            conversion_factor = self.CONVERSION_FACTORS["buprenorphine_patch"]
            return dose * conversion_factor
        
        else:
            # Handle route variations
            if route == "iv" or route == "intravenous":
                iv_med_name = f"{med_name.split('_')[0]}_iv"
                if iv_med_name in self.CONVERSION_FACTORS:
                    conversion_factor = self.CONVERSION_FACTORS[iv_med_name]
                else:
                    conversion_factor = self.CONVERSION_FACTORS.get(med_name, 1.0)
            else:
                conversion_factor = self.CONVERSION_FACTORS.get(med_name, 1.0)
        
        # Calculate daily MME
        daily_dose = dose * frequency
        mme = daily_dose * conversion_factor
        
        return mme
    
    def _get_interpretation(self, total_mme: float, med_details: List[Dict]) -> Dict[str, str]:
        """
        Provides risk interpretation based on total MME
        
        Args:
            total_mme (float): Total daily MME
            med_details (list): List of medication details
            
        Returns:
            Dict with interpretation details
        """
        
        # Create medication summary
        med_summary = ", ".join([
            f"{med['medication']} {med['daily_dose']}{med.get('unit', 'mg')}/day (MME: {med['mme_contribution']:.1f})"
            for med in med_details
        ])
        
        if total_mme < 50:
            return {
                "stage": "Low Risk",
                "description": "Standard monitoring recommended",
                "interpretation": (f"Total MME: {total_mme:.1f} mg/day. Low-risk opioid dosing. "
                                f"Medications: {med_summary}. Standard monitoring and counseling on opioid safety "
                                f"recommended. Educate patient on proper storage, disposal, and signs of overdose. "
                                f"Consider non-opioid and non-pharmacologic therapies. Regular assessment of "
                                f"pain and function is important. Avoid concurrent benzodiazepines or alcohol. "
                                f"Review goals of therapy and continue to monitor for effectiveness and adverse effects. "
                                f"CDC guidelines recommend caution when increasing doses and considering the "
                                f"benefits and risks of continued opioid therapy.")
            }
        elif total_mme < 90:
            return {
                "stage": "Moderate Risk",
                "description": "Increased monitoring recommended",
                "interpretation": (f"Total MME: {total_mme:.1f} mg/day. Moderate-risk opioid dosing. "
                                f"Medications: {med_summary}. Increased monitoring recommended. Consider tapering "
                                f"to lower doses if pain and function goals are not being met. Careful review of "
                                f"benefits versus risks is essential. Naloxone prescription strongly recommended. "
                                f"Avoid concurrent benzodiazepines, alcohol, and other CNS depressants. More frequent "
                                f"monitoring for signs of opioid use disorder, oversedation, and respiratory depression. "
                                f"Consider consultation with pain management specialist. Document rationale for "
                                f"continued therapy at this dose level. Patient education on overdose risks and "
                                f"naloxone use is critical.")
            }
        else:  # total_mme >= 90
            return {
                "stage": "High Risk",
                "description": "High-risk dosing requiring careful evaluation",
                "interpretation": (f"Total MME: {total_mme:.1f} mg/day. High-risk opioid dosing. "
                                f"Medications: {med_summary}. Careful evaluation of benefits versus risks is "
                                f"essential. Strong consideration for tapering to lower doses unless there are "
                                f"compelling reasons to continue at current doses. Naloxone prescription is "
                                f"essential. Frequent monitoring required with close assessment for signs of "
                                f"opioid use disorder, oversedation, and respiratory depression. Avoid all "
                                f"concurrent CNS depressants including benzodiazepines and alcohol. Consider "
                                f"consultation with or referral to pain management specialist or addiction "
                                f"medicine specialist. Document detailed rationale for continued high-dose "
                                f"therapy. Implement safety measures including frequent follow-ups, urine drug "
                                f"testing, and prescription drug monitoring program review.")
            }


def calculate_mme_calculator(opioid_medications: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MmeCalculator()
    return calculator.calculate(opioid_medications)