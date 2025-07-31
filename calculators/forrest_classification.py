"""
Forrest Classification of Upper GI Bleeding Calculator

Stratifies severity of upper GI bleeding according to endoscopic findings. Helps prognosticate 
and risk stratify patients, guides endoscopic therapeutic decisions, and assists in determining 
discharge versus inpatient monitoring.

References:
1. Forrest JA, Finlayson ND, Shearman DJ. Endoscopy in gastrointestinal bleeding. 
   Lancet. 1974;2(7877):394-7.
2. Laine L, Peterson WL. Bleeding peptic ulcer. N Engl J Med. 1994;331(11):717-27.
3. Rockall TA, Logan RF, Devlin HB, Northfield TC. Risk assessment after acute upper 
   gastrointestinal haemorrhage. Gut. 1996;38(3):316-21.
4. Sung JJ, Tsoi KK, Ma TK, Yung MY, Lau JY, Chiu PW. Causes of mortality in patients 
   with peptic ulcer bleeding: a prospective cohort study of 10,428 cases. 
   Am J Gastroenterol. 2010;105(1):84-9.
"""

from typing import Dict, Any


class ForrestClassificationCalculator:
    """Calculator for Forrest Classification of Upper GI Bleeding"""
    
    def __init__(self):
        # Classification mapping with risk data
        self.CLASSIFICATIONS = {
            "active_spurting": {
                "class": "Class 1A",
                "description": "Active spurting bleeding",
                "rebleeding_risk": 55,
                "mortality_risk": 11,
                "intervention": "immediate",
                "therapy": "injection, thermal coagulation, or mechanical therapy"
            },
            "active_oozing": {
                "class": "Class 1B", 
                "description": "Active oozing bleeding",
                "rebleeding_risk": 55,
                "mortality_risk": 11,
                "intervention": "immediate",
                "therapy": "injection or thermal coagulation"
            },
            "nonbleeding_visible_vessel": {
                "class": "Class 2A",
                "description": "Non-bleeding visible vessel",
                "rebleeding_risk": 43,
                "mortality_risk": 11,
                "intervention": "recommended",
                "therapy": "endoscopic therapy to prevent rebleeding"
            },
            "adherent_clot": {
                "class": "Class 2B",
                "description": "Adherent clot",
                "rebleeding_risk": 22,
                "mortality_risk": 7,
                "intervention": "consider",
                "therapy": "clot removal with endoscopic therapy or close monitoring"
            },
            "flat_pigmented_spot": {
                "class": "Class 2C",
                "description": "Flat pigmented spot",
                "rebleeding_risk": 10,
                "mortality_risk": 3,
                "intervention": "usually_not_required",
                "therapy": "medical therapy, early discharge may be appropriate"
            },
            "clean_ulcer_base": {
                "class": "Class 3",
                "description": "Clean ulcer base",
                "rebleeding_risk": 5,
                "mortality_risk": 2,
                "intervention": "not_required",
                "therapy": "medical therapy, early discharge appropriate"
            }
        }
    
    def calculate(self, endoscopic_finding: str) -> Dict[str, Any]:
        """
        Classifies upper GI bleeding based on endoscopic findings
        
        Args:
            endoscopic_finding (str): Endoscopic appearance of the bleeding peptic ulcer
            
        Returns:
            Dict with the Forrest classification and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(endoscopic_finding)
        
        # Get classification data
        classification_data = self.CLASSIFICATIONS[endoscopic_finding]
        
        # Generate interpretation
        interpretation = self._get_interpretation(classification_data)
        
        return {
            "result": classification_data["class"],
            "unit": "class",
            "interpretation": interpretation["interpretation"],
            "stage": classification_data["class"],
            "stage_description": classification_data["description"]
        }
    
    def _validate_inputs(self, endoscopic_finding: str):
        """Validates input parameters"""
        
        valid_findings = list(self.CLASSIFICATIONS.keys())
        if endoscopic_finding not in valid_findings:
            raise ValueError(f"Endoscopic finding must be one of: {valid_findings}")
    
    def _get_interpretation(self, classification_data: Dict) -> Dict[str, str]:
        """
        Generates clinical interpretation based on classification
        
        Args:
            classification_data (Dict): Classification data with risks and recommendations
            
        Returns:
            Dict with detailed clinical interpretation
        """
        
        class_name = classification_data["class"]
        description = classification_data["description"]
        rebleeding_risk = classification_data["rebleeding_risk"]
        mortality_risk = classification_data["mortality_risk"]
        intervention = classification_data["intervention"]
        therapy = classification_data["therapy"]
        
        # Generate risk-based interpretation
        if class_name in ["Class 1A", "Class 1B"]:
            # Active bleeding - highest risk
            interpretation = (
                f"{description}. Highest risk category requiring immediate endoscopic intervention. "
                f"Rebleeding risk: {rebleeding_risk}%, mortality risk: {mortality_risk}%. "
                f"Emergency endoscopic therapy with {therapy} indicated."
            )
        elif class_name == "Class 2A":
            # Non-bleeding visible vessel - high risk
            interpretation = (
                f"{description}. High risk of rebleeding. "
                f"Rebleeding risk: {rebleeding_risk}%, mortality risk: {mortality_risk}%. "
                f"Endoscopic therapy strongly recommended to prevent rebleeding."
            )
        elif class_name == "Class 2B":
            # Adherent clot - intermediate risk
            interpretation = (
                f"{description}. Intermediate risk of rebleeding. "
                f"Rebleeding risk: {rebleeding_risk}%, mortality risk: {mortality_risk}%. "
                f"Consider endoscopic therapy after clot removal or close monitoring with early intervention if rebleeding occurs."
            )
        elif class_name == "Class 2C":
            # Flat pigmented spot - low risk
            interpretation = (
                f"{description}. Low risk of rebleeding. "
                f"Rebleeding risk: {rebleeding_risk}%, mortality risk: {mortality_risk}%. "
                f"Endoscopic therapy generally not required. Medical therapy and early discharge may be appropriate."
            )
        else:  # Class 3
            # Clean ulcer base - lowest risk
            interpretation = (
                f"{description}. Lowest risk category. "
                f"Rebleeding risk: {rebleeding_risk}%, mortality risk: {mortality_risk}%. "
                f"No endoscopic therapy required. Early discharge appropriate with medical therapy."
            )
        
        return {
            "interpretation": interpretation
        }


def calculate_forrest_classification(endoscopic_finding: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_forrest_classification pattern
    """
    calculator = ForrestClassificationCalculator()
    return calculator.calculate(endoscopic_finding)