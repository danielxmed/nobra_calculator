"""
CIWA-Ar for Alcohol Withdrawal Calculator

Objectifies severity of alcohol withdrawal symptoms and guides treatment decisions.
The Clinical Institute Withdrawal Assessment for Alcohol, Revised (CIWA-Ar) is a 
validated instrument for monitoring withdrawal symptoms and medication dosing.

References:
1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of alcohol 
   withdrawal: the revised clinical institute withdrawal assessment for alcohol scale 
   (CIWA-Ar). Br J Addict. 1989 Nov;84(11):1353-7.
2. Mayo-Smith MF, Beecher LH, Fischer TL, Gorelick DA, Guillaume JL, Hill A, et al. 
   Management of alcohol withdrawal delirium. An evidence-based practice guideline. 
   Arch Intern Med. 2004 Jul 12;164(13):1405-12.
3. Holbrook AM, Crowther R, Lotter A, Cheng C, King D. Meta-analysis of benzodiazepine 
   use in the treatment of acute alcohol withdrawal. CMAJ. 1999 Mar 23;160(6):649-55.
"""

from typing import Dict, Any


class CiwaArAlcoholWithdrawalCalculator:
    """Calculator for CIWA-Ar Alcohol Withdrawal Assessment"""
    
    def __init__(self):
        # Component descriptions for detailed scoring
        self.components = {
            "nausea_vomiting": {
                "name": "Nausea and Vomiting",
                "descriptions": {
                    0: "None",
                    1: "Mild nausea with no vomiting", 
                    2: "",
                    3: "",
                    4: "Intermittent nausea with dry heaves",
                    5: "",
                    6: "",
                    7: "Constant nausea, frequent dry heaves and vomiting"
                }
            },
            "tremor": {
                "name": "Tremor",
                "descriptions": {
                    0: "No tremor",
                    1: "Not visible, but can be felt fingertip to fingertip",
                    2: "",
                    3: "",
                    4: "Moderate, with patient's arms extended",
                    5: "",
                    6: "",
                    7: "Severe, even with arms not extended"
                }
            },
            "paroxysmal_sweats": {
                "name": "Paroxysmal Sweats",
                "descriptions": {
                    0: "No sweat visible",
                    1: "Barely perceptible sweating, palms moist",
                    2: "",
                    3: "",
                    4: "Beads of sweat obvious on forehead",
                    5: "",
                    6: "",
                    7: "Drenching sweats"
                }
            },
            "anxiety": {
                "name": "Anxiety",
                "descriptions": {
                    0: "None, at ease",
                    1: "Mildly anxious",
                    2: "",
                    3: "",
                    4: "Moderately anxious, or guarded, so anxiety is inferred",
                    5: "",
                    6: "",
                    7: "Equivalent to acute panic states as seen in severe delirium or acute schizophrenic reactions"
                }
            },
            "agitation": {
                "name": "Agitation",
                "descriptions": {
                    0: "Normal activity",
                    1: "Somewhat more than normal activity",
                    2: "",
                    3: "",
                    4: "Moderately fidgety and restless",
                    5: "",
                    6: "",
                    7: "Paces back and forth during most of the interview, or constantly thrashes about"
                }
            },
            "tactile_disturbances": {
                "name": "Tactile Disturbances",
                "descriptions": {
                    0: "None",
                    1: "Very mild itching, pins and needles, burning or numbness",
                    2: "Mild itching, pins and needles, burning or numbness",
                    3: "Moderate itching, pins and needles, burning or numbness",
                    4: "Moderately severe hallucinations",
                    5: "Severe hallucinations",
                    6: "Extremely severe hallucinations",
                    7: "Continuous hallucinations"
                }
            },
            "auditory_disturbances": {
                "name": "Auditory Disturbances",
                "descriptions": {
                    0: "Not present",
                    1: "Very mild harshness or ability to frighten",
                    2: "Mild harshness or ability to frighten",
                    3: "Moderate harshness or ability to frighten",
                    4: "Moderately severe hallucinations",
                    5: "Severe hallucinations",
                    6: "Extremely severe hallucinations",
                    7: "Continuous hallucinations"
                }
            },
            "visual_disturbances": {
                "name": "Visual Disturbances",
                "descriptions": {
                    0: "Not present",
                    1: "Very mild sensitivity",
                    2: "Mild sensitivity",
                    3: "Moderate sensitivity",
                    4: "Moderately severe hallucinations",
                    5: "Severe hallucinations",
                    6: "Extremely severe hallucinations",
                    7: "Continuous hallucinations"
                }
            },
            "headache": {
                "name": "Headache, Fullness in Head",
                "descriptions": {
                    0: "Not present",
                    1: "Very mild",
                    2: "Mild",
                    3: "Moderate",
                    4: "Moderately severe", 
                    5: "Severe",
                    6: "Very severe",
                    7: "Extremely severe"
                }
            },
            "orientation": {
                "name": "Orientation and Clouding of Sensorium",
                "descriptions": {
                    0: "Oriented and can do serial additions",
                    1: "Cannot do serial additions or is uncertain about date",
                    2: "Disoriented for date by no more than 2 calendar days",
                    3: "Disoriented for date by more than 2 calendar days",
                    4: "Disoriented for place/or person"
                }
            }
        }
        
        # Treatment recommendations
        self.treatment_guidelines = {
            "minimal": {
                "range": "0-8",
                "medication": "Usually none required",
                "monitoring": "Monitor every 4-8 hours",
                "considerations": "Supportive care, hydration, vitamins"
            },
            "mild_moderate": {
                "range": "9-19", 
                "medication": "Consider benzodiazepines (lorazepam 1-2mg PO/IV q1-2h PRN)",
                "monitoring": "Monitor every 1-2 hours",
                "considerations": "Symptom-triggered therapy preferred"
            },
            "severe": {
                "range": "≥20",
                "medication": "Aggressive benzodiazepines (lorazepam 2-4mg IV q15-30min PRN)",
                "monitoring": "Continuous monitoring, consider ICU",
                "considerations": "High risk for seizures and delirium tremens"
            }
        }
    
    def calculate(
        self,
        nausea_vomiting: int,
        tremor: int,
        paroxysmal_sweats: int,
        anxiety: int,
        agitation: int,
        tactile_disturbances: int,
        auditory_disturbances: int,
        visual_disturbances: int,
        headache: int,
        orientation: int
    ) -> Dict[str, Any]:
        """
        Calculates CIWA-Ar score for alcohol withdrawal assessment
        
        Args:
            nausea_vomiting: Nausea and vomiting severity (0-7)
            tremor: Tremor severity (0-7)
            paroxysmal_sweats: Sweating severity (0-7)
            anxiety: Anxiety level (0-7)
            agitation: Agitation level (0-7)
            tactile_disturbances: Tactile hallucinations/disturbances (0-7)
            auditory_disturbances: Auditory hallucinations/disturbances (0-7)
            visual_disturbances: Visual hallucinations/disturbances (0-7)
            headache: Headache severity (0-7)
            orientation: Orientation and sensorium (0-4)
            
        Returns:
            Dict with CIWA-Ar score, severity assessment, and treatment recommendations
        """
        
        # Validate inputs
        self._validate_inputs(nausea_vomiting, tremor, paroxysmal_sweats, anxiety, agitation,
                            tactile_disturbances, auditory_disturbances, visual_disturbances,
                            headache, orientation)
        
        # Calculate total score
        total_score = (nausea_vomiting + tremor + paroxysmal_sweats + anxiety + agitation + 
                      tactile_disturbances + auditory_disturbances + visual_disturbances + 
                      headache + orientation)
        
        # Get severity assessment
        severity_assessment = self._get_severity_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            nausea_vomiting, tremor, paroxysmal_sweats, anxiety, agitation,
            tactile_disturbances, auditory_disturbances, visual_disturbances,
            headache, orientation, total_score
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": severity_assessment["interpretation"],
            "stage": severity_assessment["stage"],
            "stage_description": severity_assessment["description"],
            "scoring_breakdown": scoring_breakdown
        }
    
    def _validate_inputs(self, nausea_vomiting, tremor, paroxysmal_sweats, anxiety, agitation,
                        tactile_disturbances, auditory_disturbances, visual_disturbances,
                        headache, orientation):
        """Validates input parameters for CIWA-Ar components"""
        
        # Standard 0-7 components
        standard_components = [
            ("nausea_vomiting", nausea_vomiting),
            ("tremor", tremor),
            ("paroxysmal_sweats", paroxysmal_sweats),
            ("anxiety", anxiety),
            ("agitation", agitation),
            ("tactile_disturbances", tactile_disturbances),
            ("auditory_disturbances", auditory_disturbances),
            ("visual_disturbances", visual_disturbances),
            ("headache", headache)
        ]
        
        for name, value in standard_components:
            if not isinstance(value, int) or value < 0 or value > 7:
                raise ValueError(f"{name} must be an integer between 0 and 7")
        
        # Orientation has different range (0-4)
        if not isinstance(orientation, int) or orientation < 0 or orientation > 4:
            raise ValueError("Orientation must be an integer between 0 and 4")
    
    def _get_severity_assessment(self, score: int) -> Dict[str, str]:
        """
        Determines withdrawal severity and treatment recommendations based on CIWA-Ar score
        
        Args:
            score: Total CIWA-Ar score
            
        Returns:
            Dict with severity assessment and clinical recommendations
        """
        
        if score <= 8:
            stage = "Minimal"
            description = "Absent or minimal withdrawal"
            interpretation = f"CIWA-Ar Score {score}: Minimal withdrawal symptoms. No pharmacological treatment typically required. Monitor every 4-8 hours. Provide supportive care including hydration and thiamine."
            
        elif score <= 19:
            stage = "Mild to Moderate"
            description = "Mild to moderate withdrawal"
            interpretation = f"CIWA-Ar Score {score}: Mild to moderate withdrawal symptoms. Consider symptom-triggered benzodiazepine therapy. Monitor every 1-2 hours. Typical dose: lorazepam 1-2mg PO/IV q1-2h PRN."
            
        else:  # score >= 20
            stage = "Severe"
            description = "Severe withdrawal"
            interpretation = f"CIWA-Ar Score {score}: Severe withdrawal symptoms with high risk for delirium tremens and seizures. Requires immediate aggressive treatment with benzodiazepines. Consider ICU monitoring. Typical dose: lorazepam 2-4mg IV q15-30min PRN."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, nausea_vomiting, tremor, paroxysmal_sweats, anxiety, agitation,
                             tactile_disturbances, auditory_disturbances, visual_disturbances,
                             headache, orientation, total_score) -> Dict[str, Any]:
        """Provides detailed scoring breakdown with clinical context"""
        
        # Component scores with descriptions
        component_scores = {}
        
        for param_name, value in [
            ("nausea_vomiting", nausea_vomiting),
            ("tremor", tremor), 
            ("paroxysmal_sweats", paroxysmal_sweats),
            ("anxiety", anxiety),
            ("agitation", agitation),
            ("tactile_disturbances", tactile_disturbances),
            ("auditory_disturbances", auditory_disturbances),
            ("visual_disturbances", visual_disturbances),
            ("headache", headache),
            ("orientation", orientation)
        ]:
            component_info = self.components[param_name]
            max_score = 4 if param_name == "orientation" else 7
            
            component_scores[param_name] = {
                "name": component_info["name"],
                "score": value,
                "max_score": max_score,
                "description": component_info["descriptions"].get(value, ""),
                "clinical_significance": self._get_component_significance(param_name, value)
            }
        
        # Treatment recommendations based on total score
        if total_score <= 8:
            treatment_rec = self.treatment_guidelines["minimal"]
        elif total_score <= 19:
            treatment_rec = self.treatment_guidelines["mild_moderate"]
        else:
            treatment_rec = self.treatment_guidelines["severe"]
        
        breakdown = {
            "component_scores": component_scores,
            "score_summary": {
                "total_score": total_score,
                "max_possible_score": 67,
                "severity_category": self._get_severity_category(total_score),
                "risk_level": self._get_risk_level(total_score)
            },
            "treatment_recommendations": {
                "score_range": treatment_rec["range"],
                "medication": treatment_rec["medication"],
                "monitoring": treatment_rec["monitoring"],
                "considerations": treatment_rec["considerations"]
            },
            "clinical_context": {
                "assessment_frequency": "Every 1-2 hours during active withdrawal",
                "duration": "Typically peaks 24-72 hours after last drink",
                "complications_to_monitor": [
                    "Delirium tremens (mortality 5-25% if untreated)",
                    "Withdrawal seizures (usually within 48 hours)",
                    "Cardiovascular instability",
                    "Hyperthermia and dehydration"
                ],
                "contraindications": [
                    "Not suitable for intubated patients",
                    "Not reliable in heavily sedated patients",
                    "Requires patient cooperation for accurate assessment"
                ]
            },
            "additional_considerations": {
                "thiamine_supplementation": "Thiamine 100mg daily recommended for all patients",
                "folate_supplementation": "Folate 1mg daily recommended",
                "fluid_electrolyte_monitoring": "Monitor for hyponatremia, hypokalemia, hypomagnesemia",
                "comorbidity_assessment": "Screen for concurrent medical and psychiatric conditions"
            }
        }
        
        return breakdown
    
    def _get_component_significance(self, component: str, score: int) -> str:
        """Gets clinical significance of individual component scores"""
        
        significance_map = {
            "nausea_vomiting": "GI symptoms often early sign of withdrawal",
            "tremor": "Classic withdrawal sign, often most noticeable",
            "paroxysmal_sweats": "Autonomic instability indicator",
            "anxiety": "Psychological component, may persist longer",
            "agitation": "Motor restlessness, risk for injury",
            "tactile_disturbances": "May progress to tactile hallucinations",
            "auditory_disturbances": "May progress to auditory hallucinations", 
            "visual_disturbances": "May progress to visual hallucinations",
            "headache": "Often accompanies other withdrawal symptoms",
            "orientation": "Cognitive impairment, risk for delirium"
        }
        
        base_significance = significance_map.get(component, "")
        
        if score >= 4 and component != "orientation":
            return f"{base_significance} - Moderate to severe symptoms present"
        elif score >= 2 and component == "orientation":
            return f"{base_significance} - Cognitive impairment present"
        elif score > 0:
            return f"{base_significance} - Mild symptoms present"
        else:
            return f"{base_significance} - No symptoms"
    
    def _get_severity_category(self, score: int) -> str:
        """Returns severity category for scoring summary"""
        if score <= 8:
            return "Minimal withdrawal"
        elif score <= 19:
            return "Mild to moderate withdrawal"
        else:
            return "Severe withdrawal"
    
    def _get_risk_level(self, score: int) -> str:
        """Returns risk level assessment"""
        if score <= 8:
            return "Low risk for complications"
        elif score <= 19:
            return "Moderate risk, requires monitoring"
        else:
            return "High risk for delirium tremens and seizures"


def calculate_ciwa_ar_alcohol_withdrawal(
    nausea_vomiting: int,
    tremor: int,
    paroxysmal_sweats: int,
    anxiety: int,
    agitation: int,
    tactile_disturbances: int,
    auditory_disturbances: int,
    visual_disturbances: int,
    headache: int,
    orientation: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CiwaArAlcoholWithdrawalCalculator()
    return calculator.calculate(
        nausea_vomiting=nausea_vomiting,
        tremor=tremor,
        paroxysmal_sweats=paroxysmal_sweats,
        anxiety=anxiety,
        agitation=agitation,
        tactile_disturbances=tactile_disturbances,
        auditory_disturbances=auditory_disturbances,
        visual_disturbances=visual_disturbances,
        headache=headache,
        orientation=orientation
    )