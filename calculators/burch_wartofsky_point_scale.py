"""
Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis Calculator

Predicts likelihood that biochemical thyrotoxicosis is thyroid storm by evaluating 
clinical symptoms and precipitating factors. This empirically derived scoring system 
assesses multiple organ decompensation including thermoregulatory dysfunction, 
cardiovascular symptoms, neurological changes, and gastrointestinal symptoms.

References:
- Burch HB, Wartofsky L. Life-threatening thyrotoxicosis. Thyroid storm. 
  Endocrinology and Metabolism Clinics of North America. 1993;22(2):263-277.
- Akamizu T, et al. Diagnostic criteria, clinical features, and incidence of 
  thyroid storm based on nationwide surveys. Thyroid. 2012;22(7):661-679.
"""

from typing import Dict, Any


class BurchWartofskypointScaleCalculator:
    """Calculator for Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis"""
    
    def __init__(self):
        # Scoring systems for each parameter
        self.temperature_scores = {
            "99_100": 5,    # 99-100°F
            "100_101": 10,  # 100-101°F
            "101_102": 15,  # 101-102°F
            "102_103": 20,  # 102-103°F
            "103_104": 25,  # 103-104°F
            "over_104": 30  # >104°F
        }
        
        self.cns_scores = {
            "absent": 0,
            "mild_agitation": 10,
            "moderate_delirium_psychosis_extreme_lethargy": 20,
            "severe_coma_seizure": 30
        }
        
        self.gi_hepatic_scores = {
            "absent": 0,
            "moderate_diarrhea_nausea_vomiting_abdominal_pain": 10,
            "severe_unexplained_jaundice": 20
        }
        
        self.cardiovascular_scores = {
            "absent": 0,
            "moderate_chf_pedal_edema_pulmonary_edema": 5,
            "severe_pulmonary_edema": 15
        }
        
        self.tachycardia_scores = {
            "90_109": 5,    # 90-109 bpm
            "110_119": 10,  # 110-119 bpm
            "120_129": 15,  # 120-129 bpm
            "130_139": 20,  # 130-139 bpm
            "over_140": 25  # >140 bpm
        }
        
        self.atrial_fibrillation_scores = {
            "absent": 0,
            "present": 10
        }
        
        self.precipitant_scores = {
            "absent": 0,
            "present": 10
        }
        
        # Interpretation thresholds
        self.UNLIKELY_THRESHOLD = 25
        self.IMPENDING_THRESHOLD = 45
    
    def calculate(self, temperature: str, cns_effects: str, gi_hepatic_dysfunction: str, 
                  cardiovascular_dysfunction: str, tachycardia: str, atrial_fibrillation: str, 
                  precipitant_history: str) -> Dict[str, Any]:
        """
        Calculates the BWPS score for thyrotoxicosis
        
        Args:
            temperature (str): Body temperature range
            cns_effects (str): Central nervous system effects
            gi_hepatic_dysfunction (str): GI-hepatic dysfunction severity
            cardiovascular_dysfunction (str): Cardiovascular dysfunction severity
            tachycardia (str): Heart rate range
            atrial_fibrillation (str): Presence of atrial fibrillation
            precipitant_history (str): History of precipitating event
            
        Returns:
            Dict with the score result and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(temperature, cns_effects, gi_hepatic_dysfunction, 
                             cardiovascular_dysfunction, tachycardia, atrial_fibrillation, 
                             precipitant_history)
        
        # Calculate total score
        total_score = self._calculate_total_score(
            temperature, cns_effects, gi_hepatic_dysfunction, 
            cardiovascular_dysfunction, tachycardia, atrial_fibrillation, 
            precipitant_history
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(total_score)
        
        # Get score breakdown
        score_breakdown = self._get_score_breakdown(
            temperature, cns_effects, gi_hepatic_dysfunction, 
            cardiovascular_dysfunction, tachycardia, atrial_fibrillation, 
            precipitant_history
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "clinical_recommendations": recommendations,
            "score_breakdown": score_breakdown
        }
    
    def _validate_inputs(self, temperature: str, cns_effects: str, gi_hepatic_dysfunction: str, 
                        cardiovascular_dysfunction: str, tachycardia: str, atrial_fibrillation: str, 
                        precipitant_history: str):
        """Validates input parameters"""
        
        if temperature not in self.temperature_scores:
            raise ValueError(f"Invalid temperature range: {temperature}")
        
        if cns_effects not in self.cns_scores:
            raise ValueError(f"Invalid CNS effects: {cns_effects}")
        
        if gi_hepatic_dysfunction not in self.gi_hepatic_scores:
            raise ValueError(f"Invalid GI-hepatic dysfunction: {gi_hepatic_dysfunction}")
        
        if cardiovascular_dysfunction not in self.cardiovascular_scores:
            raise ValueError(f"Invalid cardiovascular dysfunction: {cardiovascular_dysfunction}")
        
        if tachycardia not in self.tachycardia_scores:
            raise ValueError(f"Invalid tachycardia range: {tachycardia}")
        
        if atrial_fibrillation not in self.atrial_fibrillation_scores:
            raise ValueError(f"Invalid atrial fibrillation status: {atrial_fibrillation}")
        
        if precipitant_history not in self.precipitant_scores:
            raise ValueError(f"Invalid precipitant history: {precipitant_history}")
    
    def _calculate_total_score(self, temperature: str, cns_effects: str, gi_hepatic_dysfunction: str, 
                              cardiovascular_dysfunction: str, tachycardia: str, atrial_fibrillation: str, 
                              precipitant_history: str) -> int:
        """Calculates the total BWPS score"""
        
        total_score = (
            self.temperature_scores[temperature] +
            self.cns_scores[cns_effects] +
            self.gi_hepatic_scores[gi_hepatic_dysfunction] +
            self.cardiovascular_scores[cardiovascular_dysfunction] +
            self.tachycardia_scores[tachycardia] +
            self.atrial_fibrillation_scores[atrial_fibrillation] +
            self.precipitant_scores[precipitant_history]
        )
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the score
        
        Args:
            score (int): Calculated BWPS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.UNLIKELY_THRESHOLD:
            return {
                "stage": "Unlikely_TS",
                "description": "Thyroid storm unlikely",
                "interpretation": "Score <25 suggests thyroid storm is unlikely. Continue monitoring but thyroid storm diagnosis is not supported by current clinical findings. Consider alternative diagnoses for thyrotoxic symptoms."
            }
        elif score < self.IMPENDING_THRESHOLD:
            return {
                "stage": "Impending_TS",
                "description": "Impending thyroid storm",
                "interpretation": "Score 25-44 suggests impending thyroid storm. High clinical suspicion warranted. Consider immediate treatment while monitoring for progression to overt thyroid storm. Close observation and supportive care recommended."
            }
        else:
            return {
                "stage": "Highly_Suggestive_TS",
                "description": "Thyroid storm highly suggestive",
                "interpretation": "Score ≥45 is highly suggestive of thyroid storm. This is a life-threatening endocrine emergency requiring immediate aggressive treatment including antithyroid drugs, beta-blockers, iodine, corticosteroids, and supportive care."
            }
    
    def _get_clinical_recommendations(self, score: int) -> Dict[str, list]:
        """
        Provides clinical recommendations based on the score
        
        Args:
            score (int): Calculated BWPS score
            
        Returns:
            Dict with categorized clinical recommendations
        """
        
        recommendations = {
            "immediate_actions": [],
            "monitoring": [],
            "medications": [],
            "supportive_care": [],
            "investigations": []
        }
        
        if score < self.UNLIKELY_THRESHOLD:  # Unlikely TS
            recommendations["monitoring"].extend([
                "Continue routine monitoring of vital signs",
                "Monitor for progression of symptoms",
                "Reassess clinical status regularly"
            ])
            recommendations["investigations"].extend([
                "Consider alternative diagnoses for thyrotoxic symptoms",
                "Review precipitating factors",
                "Monitor thyroid function tests"
            ])
            
        elif score < self.IMPENDING_THRESHOLD:  # Impending TS
            recommendations["immediate_actions"].extend([
                "Initiate close monitoring in appropriate clinical setting",
                "Prepare for potential escalation to thyroid storm treatment",
                "Consider early intervention to prevent progression"
            ])
            recommendations["monitoring"].extend([
                "Continuous cardiac monitoring",
                "Frequent vital sign assessment",
                "Monitor neurological status closely"
            ])
            recommendations["medications"].extend([
                "Consider antithyroid medication if not already started",
                "Beta-blocker for symptom control (propranolol preferred)",
                "Prepare emergency medications for potential escalation"
            ])
            
        else:  # Highly suggestive TS
            recommendations["immediate_actions"].extend([
                "Initiate immediate thyroid storm treatment protocol",
                "Transfer to ICU or high-dependency unit",
                "Multidisciplinary team approach (endocrinology, ICU, pharmacy)"
            ])
            recommendations["medications"].extend([
                "Antithyroid drugs: methimazole 20-30mg q8h OR propylthiouracil 300-400mg q6h",
                "Beta-blocker: propranolol 1-2mg IV q5min or 40-80mg PO q6h",
                "Iodine: SSKI 5 drops PO q6h or sodium iodide 1-2g IV daily",
                "Corticosteroids: hydrocortisone 300mg IV then 100mg q8h"
            ])
            recommendations["supportive_care"].extend([
                "Aggressive cooling measures for hyperthermia",
                "IV fluid resuscitation for dehydration",
                "Electrolyte monitoring and correction",
                "Nutritional support"
            ])
            recommendations["monitoring"].extend([
                "Continuous cardiac and hemodynamic monitoring",
                "Frequent neurological assessments",
                "Monitor for complications (heart failure, arrhythmias)"
            ])
        
        return recommendations
    
    def _get_score_breakdown(self, temperature: str, cns_effects: str, gi_hepatic_dysfunction: str, 
                            cardiovascular_dysfunction: str, tachycardia: str, atrial_fibrillation: str, 
                            precipitant_history: str) -> Dict[str, Dict[str, Any]]:
        """Returns detailed score breakdown for each component"""
        
        return {
            "temperature": {
                "category": self._get_temperature_description(temperature),
                "points": self.temperature_scores[temperature],
                "max_points": 30
            },
            "cns_effects": {
                "category": self._get_cns_description(cns_effects),
                "points": self.cns_scores[cns_effects],
                "max_points": 30
            },
            "gi_hepatic_dysfunction": {
                "category": self._get_gi_description(gi_hepatic_dysfunction),
                "points": self.gi_hepatic_scores[gi_hepatic_dysfunction],
                "max_points": 20
            },
            "cardiovascular_dysfunction": {
                "category": self._get_cv_description(cardiovascular_dysfunction),
                "points": self.cardiovascular_scores[cardiovascular_dysfunction],
                "max_points": 15
            },
            "tachycardia": {
                "category": self._get_tachycardia_description(tachycardia),
                "points": self.tachycardia_scores[tachycardia],
                "max_points": 25
            },
            "atrial_fibrillation": {
                "category": "Present" if atrial_fibrillation == "present" else "Absent",
                "points": self.atrial_fibrillation_scores[atrial_fibrillation],
                "max_points": 10
            },
            "precipitant_history": {
                "category": "Present" if precipitant_history == "present" else "Absent",
                "points": self.precipitant_scores[precipitant_history],
                "max_points": 10
            }
        }
    
    def _get_temperature_description(self, temp: str) -> str:
        """Get temperature range description"""
        temp_map = {
            "99_100": "99-100°F",
            "100_101": "100-101°F",
            "101_102": "101-102°F",
            "102_103": "102-103°F",
            "103_104": "103-104°F",
            "over_104": ">104°F"
        }
        return temp_map.get(temp, temp)
    
    def _get_cns_description(self, cns: str) -> str:
        """Get CNS effects description"""
        cns_map = {
            "absent": "Absent",
            "mild_agitation": "Mild agitation",
            "moderate_delirium_psychosis_extreme_lethargy": "Moderate (delirium, psychosis, extreme lethargy)",
            "severe_coma_seizure": "Severe (coma, seizure)"
        }
        return cns_map.get(cns, cns)
    
    def _get_gi_description(self, gi: str) -> str:
        """Get GI-hepatic dysfunction description"""
        gi_map = {
            "absent": "Absent",
            "moderate_diarrhea_nausea_vomiting_abdominal_pain": "Moderate (diarrhea, nausea, vomiting, abdominal pain)",
            "severe_unexplained_jaundice": "Severe (unexplained jaundice)"
        }
        return gi_map.get(gi, gi)
    
    def _get_cv_description(self, cv: str) -> str:
        """Get cardiovascular dysfunction description"""
        cv_map = {
            "absent": "Absent",
            "moderate_chf_pedal_edema_pulmonary_edema": "Moderate (CHF, pedal edema, pulmonary edema)",
            "severe_pulmonary_edema": "Severe (pulmonary edema)"
        }
        return cv_map.get(cv, cv)
    
    def _get_tachycardia_description(self, tachy: str) -> str:
        """Get tachycardia range description"""
        tachy_map = {
            "90_109": "90-109 bpm",
            "110_119": "110-119 bpm",
            "120_129": "120-129 bpm",
            "130_139": "130-139 bpm",
            "over_140": ">140 bpm"
        }
        return tachy_map.get(tachy, tachy)


def calculate_burch_wartofsky_point_scale(temperature: str, cns_effects: str, gi_hepatic_dysfunction: str, 
                                        cardiovascular_dysfunction: str, tachycardia: str, atrial_fibrillation: str, 
                                        precipitant_history: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BurchWartofskypointScaleCalculator()
    return calculator.calculate(temperature, cns_effects, gi_hepatic_dysfunction, 
                               cardiovascular_dysfunction, tachycardia, atrial_fibrillation, 
                               precipitant_history)