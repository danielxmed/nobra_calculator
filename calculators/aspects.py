"""
Alberta Stroke Program Early CT Score (ASPECTS) Calculator

Quantifies early ischemic changes in middle cerebral artery (MCA) territory on 
non-contrast CT to predict stroke outcome and guide treatment decisions.

The ASPECTS score is a 10-point quantitative topographic CT scan score that 
evaluates 10 specific brain regions for early ischemic changes. It's widely 
used in acute stroke management for prognostication and treatment selection.

References:
- Barber PA, Demchuk AM, Zhang J, Buchan AM. Validity and reliability of a 
  quantitative computed tomography score in predicting outcome of hyperacute 
  stroke before thrombolytic therapy. ASPECTS Study Group. Alberta Stroke 
  Programme Early CT Score. Lancet. 2000;355(9216):1670-4.
- Pexman JH, Barber PA, Hill MD, et al. Use of the Alberta Stroke Program 
  Early CT Score (ASPECTS) for assessing CT scans in patients with acute stroke. 
  AJNR Am J Neuroradiol. 2001;22(8):1534-42.
"""

from typing import Dict, Any


class AspectsCalculator:
    """Calculator for Alberta Stroke Program Early CT Score (ASPECTS)"""
    
    def __init__(self):
        # Brain regions evaluated in ASPECTS
        self.REGIONS = {
            'caudate': 'Caudate nucleus',
            'lentiform': 'Lentiform nucleus', 
            'internal_capsule': 'Internal capsule',
            'insular_ribbon': 'Insular ribbon/cortex',
            'm1': 'M1 - Anterior MCA cortex',
            'm2': 'M2 - MCA cortex lateral to insular ribbon',
            'm3': 'M3 - Posterior MCA cortex',
            'm4': 'M4 - Anterior MCA cortex (superior)',
            'm5': 'M5 - Lateral MCA cortex (superior)',
            'm6': 'M6 - Posterior MCA cortex (superior)'
        }
        
        # Prognostic categories
        self.PROGNOSIS_CATEGORIES = {
            (0, 4): {
                "category": "Extensive Infarction",
                "description": "Extensive MCA territory involvement",
                "prognosis": "Very poor",
                "hemorrhage_risk": "Very high",
                "treatment_recommendation": "Consider palliative care discussions"
            },
            (5, 7): {
                "category": "Large Infarction", 
                "description": "Large MCA territory involvement",
                "prognosis": "Poor",
                "hemorrhage_risk": "High (14% with IV tPA)",
                "treatment_recommendation": "Mechanical thrombectomy may be considered if ≥6"
            },
            (8, 10): {
                "category": "Favorable",
                "description": "Limited MCA territory involvement", 
                "prognosis": "Good",
                "hemorrhage_risk": "Low",
                "treatment_recommendation": "Good candidate for reperfusion therapy"
            }
        }
    
    def calculate(self, caudate: str, lentiform: str, internal_capsule: str, 
                 insular_ribbon: str, m1: str, m2: str, m3: str, m4: str, 
                 m5: str, m6: str) -> Dict[str, Any]:
        """
        Calculates ASPECTS score using the provided parameters
        
        Args:
            caudate (str): "normal" or "abnormal"
            lentiform (str): "normal" or "abnormal"
            internal_capsule (str): "normal" or "abnormal"
            insular_ribbon (str): "normal" or "abnormal"
            m1 (str): "normal" or "abnormal"
            m2 (str): "normal" or "abnormal"
            m3 (str): "normal" or "abnormal"
            m4 (str): "normal" or "abnormal"
            m5 (str): "normal" or "abnormal"
            m6 (str): "normal" or "abnormal"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        region_values = {
            'caudate': caudate,
            'lentiform': lentiform,
            'internal_capsule': internal_capsule,
            'insular_ribbon': insular_ribbon,
            'm1': m1,
            'm2': m2,
            'm3': m3,
            'm4': m4,
            'm5': m5,
            'm6': m6
        }
        
        self._validate_inputs(region_values)
        
        # Calculate score (start with 10, subtract 1 for each abnormal region)
        score = 10
        abnormal_regions = []
        
        for region, value in region_values.items():
            if value.lower() == 'abnormal':
                score -= 1
                abnormal_regions.append(self.REGIONS[region])
        
        # Get interpretation
        interpretation = self._get_interpretation(score, abnormal_regions)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "abnormal_regions": abnormal_regions,
            "prognosis": interpretation["prognosis"],
            "hemorrhage_risk": interpretation["hemorrhage_risk"],
            "treatment_recommendation": interpretation["treatment_recommendation"]
        }
    
    def _validate_inputs(self, region_values: Dict[str, str]):
        """Validates input parameters"""
        
        for region, value in region_values.items():
            if not isinstance(value, str):
                raise ValueError(f"{region} must be a string")
            
            if value.lower() not in ['normal', 'abnormal']:
                raise ValueError(f"{region} must be 'normal' or 'abnormal'")
    
    def _get_interpretation(self, score: int, abnormal_regions: list) -> Dict[str, str]:
        """
        Determines the interpretation based on the ASPECTS score
        
        Args:
            score (int): ASPECTS score (0-10)
            abnormal_regions (list): List of abnormal regions
            
        Returns:
            Dict with interpretation details
        """
        
        # Find the appropriate category
        category_info = None
        for (min_score, max_score), info in self.PROGNOSIS_CATEGORIES.items():
            if min_score <= score <= max_score:
                category_info = info
                break
        
        if category_info is None:
            category_info = self.PROGNOSIS_CATEGORIES[(8, 10)]  # Default to favorable
        
        interpretation_parts = []
        
        # Score and category
        interpretation_parts.append(f"ASPECTS score: {score}/10 points ({category_info['category']}).")
        
        # Abnormal regions
        if abnormal_regions:
            interpretation_parts.append(f"Abnormal regions: {', '.join(abnormal_regions)}.")
        else:
            interpretation_parts.append("All regions appear normal on CT.")
        
        # Prognosis and risk assessment
        interpretation_parts.append(f"Prognosis: {category_info['prognosis']}.")
        interpretation_parts.append(f"Hemorrhage risk: {category_info['hemorrhage_risk']}.")
        
        # Treatment recommendations based on score
        if score <= 4:
            interpretation_parts.append(
                "TREATMENT: Extensive infarction present. Very poor prognosis expected. "
                "High risk of symptomatic hemorrhage with thrombolysis. Consider palliative "
                "care discussions and comfort measures."
            )
        elif score <= 7:
            interpretation_parts.append(
                "TREATMENT: Large infarction present. Poor functional outcome likely. "
                "High risk (14%) of symptomatic ICH with IV thrombolysis. Mechanical "
                "thrombectomy may still be considered if ASPECTS ≥6 and within time window."
            )
        else:  # score >= 8
            interpretation_parts.append(
                "TREATMENT: Limited early ischemic changes. Good candidate for reperfusion "
                "therapy. Lower risk of symptomatic hemorrhage. Greater benefit from IV "
                "thrombolysis expected. Consider mechanical thrombectomy if large vessel occlusion."
            )
        
        # Clinical context
        interpretation_parts.append(
            "CLINICAL CONTEXT: ASPECTS correlates inversely with NIHSS score and stroke "
            "severity. Score predicts 3-month functional outcome and symptomatic ICH risk. "
            "Use with clinical assessment, time from onset, and other imaging findings."
        )
        
        # Additional notes
        interpretation_parts.append(
            "IMPORTANT: ASPECTS should be evaluated on all axial CT cuts, not just two "
            "standardized levels. Requires assessment for ≥1/3 area involvement in each region. "
            "Consider stroke team consultation for treatment decisions."
        )
        
        return {
            "stage": category_info["category"],
            "description": category_info["description"],
            "interpretation": " ".join(interpretation_parts),
            "prognosis": category_info["prognosis"],
            "hemorrhage_risk": category_info["hemorrhage_risk"],
            "treatment_recommendation": category_info["treatment_recommendation"]
        }


def calculate_aspects(caudate: str, lentiform: str, internal_capsule: str,
                     insular_ribbon: str, m1: str, m2: str, m3: str, m4: str,
                     m5: str, m6: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_aspects pattern
    """
    calculator = AspectsCalculator()
    return calculator.calculate(
        caudate=caudate,
        lentiform=lentiform,
        internal_capsule=internal_capsule,
        insular_ribbon=insular_ribbon,
        m1=m1,
        m2=m2,
        m3=m3,
        m4=m4,
        m5=m5,
        m6=m6
    )