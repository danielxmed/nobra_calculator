"""
Montreal Classification for Inflammatory Bowel Disease (IBD) Calculator

Classifies phenotype and severity of Crohn's disease and ulcerative colitis
to guide treatment decisions and predict disease course.

References:
1. Silverberg MS, et al. Can J Gastroenterol. 2005;19 Suppl A:5A-36A.
2. Satsangi J, et al. Gut. 2006;55(6):749-53.
3. Thia KT, et al. Gastroenterology. 2010;139(4):1147-55.
"""

from typing import Dict, Any, Optional


class MontrealClassificationIbdCalculator:
    """Calculator for Montreal Classification for Inflammatory Bowel Disease (IBD)"""
    
    def __init__(self):
        # Age classification thresholds
        self.AGE_THRESHOLDS = {
            "A1": (0, 16),     # <17 years
            "A2": (17, 40),    # 17-40 years  
            "A3": (41, 120)    # >40 years
        }
        
        # Classification codes and descriptions
        self.LOCATION_CODES = {
            "L1_ileal": ("L1", "Ileal (terminal ileum ± cecum)"),
            "L2_colonic": ("L2", "Colonic (any colonic location between cecum and rectum)"),
            "L3_ileocolonic": ("L3", "Ileocolonic (terminal ileum + any colonic location)"),
            "L4_upper_gi": ("L4", "Upper gastrointestinal (proximal to terminal ileum)")
        }
        
        self.BEHAVIOR_CODES = {
            "B1_inflammatory": ("B1", "Inflammatory (non-stricturing, non-penetrating)"),
            "B2_stricturing": ("B2", "Stricturing (intestinal stenosis)"),
            "B3_penetrating": ("B3", "Penetrating (fistula, abscess, perforation)")
        }
        
        self.EXTENT_CODES = {
            "E1_proctitis": ("E1", "Proctitis (rectum only)"),
            "E2_left_sided": ("E2", "Left-sided colitis (distal to splenic flexure)"),
            "E3_extensive": ("E3", "Extensive colitis (proximal to splenic flexure)")
        }
        
        self.SEVERITY_CODES = {
            "S0_remission": ("S0", "Clinical remission"),
            "S1_mild": ("S1", "Mild activity"),
            "S2_moderate": ("S2", "Moderate activity"),
            "S3_severe": ("S3", "Severe activity")
        }
    
    def calculate(self, disease_type: str, age_at_diagnosis: int, 
                  crohns_location: Optional[str] = None,
                  crohns_behavior: Optional[str] = None,
                  perianal_disease: Optional[str] = None,
                  uc_extent: Optional[str] = None,
                  uc_severity: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates the Montreal Classification for IBD
        
        Args:
            disease_type (str): Type of IBD (crohns_disease or ulcerative_colitis)
            age_at_diagnosis (int): Age at diagnosis in years
            crohns_location (str, optional): Location for Crohn's disease
            crohns_behavior (str, optional): Behavior for Crohn's disease
            perianal_disease (str, optional): Perianal disease presence
            uc_extent (str, optional): Extent for ulcerative colitis
            uc_severity (str, optional): Severity for ulcerative colitis
            
        Returns:
            Dict with Montreal Classification and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(disease_type, age_at_diagnosis, crohns_location,
                             crohns_behavior, perianal_disease, uc_extent, uc_severity)
        
        # Determine age classification
        age_code = self._get_age_classification(age_at_diagnosis)
        
        # Generate classification based on disease type
        if disease_type == "crohns_disease":
            classification = self._classify_crohns(age_code, crohns_location, 
                                                 crohns_behavior, perianal_disease)
        else:  # ulcerative_colitis
            classification = self._classify_uc(age_code, uc_extent, uc_severity)
        
        return classification
    
    def _validate_inputs(self, disease_type: str, age_at_diagnosis: int,
                        crohns_location: Optional[str], crohns_behavior: Optional[str],
                        perianal_disease: Optional[str], uc_extent: Optional[str],
                        uc_severity: Optional[str]):
        """Validates input parameters"""
        
        if disease_type not in ["crohns_disease", "ulcerative_colitis"]:
            raise ValueError("Disease type must be 'crohns_disease' or 'ulcerative_colitis'")
        
        if not isinstance(age_at_diagnosis, int) or age_at_diagnosis < 0 or age_at_diagnosis > 120:
            raise ValueError("Age at diagnosis must be between 0 and 120 years")
        
        if disease_type == "crohns_disease":
            if not crohns_location or not crohns_behavior:
                raise ValueError("Crohn's disease requires location and behavior parameters")
            
            if crohns_location not in self.LOCATION_CODES:
                raise ValueError(f"Invalid Crohn's location: {crohns_location}")
            
            if crohns_behavior not in self.BEHAVIOR_CODES:
                raise ValueError(f"Invalid Crohn's behavior: {crohns_behavior}")
            
            if perianal_disease and perianal_disease not in ["yes", "no"]:
                raise ValueError("Perianal disease must be 'yes' or 'no'")
        
        elif disease_type == "ulcerative_colitis":
            if not uc_extent or not uc_severity:
                raise ValueError("Ulcerative colitis requires extent and severity parameters")
            
            if uc_extent not in self.EXTENT_CODES:
                raise ValueError(f"Invalid UC extent: {uc_extent}")
            
            if uc_severity not in self.SEVERITY_CODES:
                raise ValueError(f"Invalid UC severity: {uc_severity}")
    
    def _get_age_classification(self, age: int) -> str:
        """Determines Montreal age classification"""
        
        if age <= 16:
            return "A1"
        elif age <= 40:
            return "A2"
        else:
            return "A3"
    
    def _classify_crohns(self, age_code: str, location: str, behavior: str,
                        perianal: Optional[str]) -> Dict[str, Any]:
        """Classifies Crohn's disease according to Montreal Classification"""
        
        location_code, location_desc = self.LOCATION_CODES[location]
        behavior_code, behavior_desc = self.BEHAVIOR_CODES[behavior]
        
        # Build classification code
        classification_code = f"{age_code}{location_code}{behavior_code}"
        
        # Add perianal modifier if present
        if perianal == "yes":
            classification_code += "p"
            perianal_text = " with perianal disease"
        else:
            perianal_text = ""
        
        # Age description
        age_desc = self._get_age_description(age_code)
        
        # Build full description
        full_description = f"Crohn's Disease: {age_desc}, {location_desc}, {behavior_desc}{perianal_text}"
        
        # Clinical interpretation
        interpretation = self._get_crohns_interpretation(location_code, behavior_code, perianal == "yes")
        
        return {
            "result": classification_code,
            "unit": "Montreal Classification",
            "interpretation": interpretation,
            "stage": "Crohn's Disease Classification",
            "stage_description": full_description
        }
    
    def _classify_uc(self, age_code: str, extent: str, severity: str) -> Dict[str, Any]:
        """Classifies ulcerative colitis according to Montreal Classification"""
        
        extent_code, extent_desc = self.EXTENT_CODES[extent]
        severity_code, severity_desc = self.SEVERITY_CODES[severity]
        
        # Build classification code
        classification_code = f"{age_code}{extent_code}{severity_code}"
        
        # Age description
        age_desc = self._get_age_description(age_code)
        
        # Build full description
        full_description = f"Ulcerative Colitis: {age_desc}, {extent_desc}, {severity_desc}"
        
        # Clinical interpretation
        interpretation = self._get_uc_interpretation(extent_code, severity_code)
        
        return {
            "result": classification_code,
            "unit": "Montreal Classification",
            "interpretation": interpretation,
            "stage": "Ulcerative Colitis Classification",
            "stage_description": full_description
        }
    
    def _get_age_description(self, age_code: str) -> str:
        """Returns age category description"""
        
        age_descriptions = {
            "A1": "Pediatric onset (<17 years)",
            "A2": "Young adult onset (17-40 years)", 
            "A3": "Older adult onset (>40 years)"
        }
        return age_descriptions[age_code]
    
    def _get_crohns_interpretation(self, location: str, behavior: str, perianal: bool) -> str:
        """Provides clinical interpretation for Crohn's disease classification"""
        
        interpretation = f"Montreal Classification {location}{behavior}"
        if perianal:
            interpretation += "p"
        
        interpretation += ". "
        
        # Location-specific guidance
        location_guidance = {
            "L1": "Ileal disease may require surveillance for small bowel complications. Consider nutritional assessment.",
            "L2": "Colonic disease may present with bloody diarrhea. Colonoscopic surveillance recommended.",
            "L3": "Ileocolonic disease has highest risk for surgical complications. Close monitoring needed.",
            "L4": "Upper GI involvement may cause growth retardation in pediatric patients. Nutritional support important."
        }
        
        # Behavior-specific guidance
        behavior_guidance = {
            "B1": "Inflammatory behavior may respond well to medical therapy. Monitor for disease progression.",
            "B2": "Stricturing behavior may require endoscopic or surgical intervention. Assess for obstruction.",
            "B3": "Penetrating behavior requires aggressive management. Screen for abscesses and fistulas."
        }
        
        interpretation += location_guidance[location] + " " + behavior_guidance[behavior]
        
        if perianal:
            interpretation += " Perianal disease modifier indicates need for specialized management and MRI assessment."
        
        interpretation += " This classification helps predict disease course and guide therapeutic decisions."
        
        return interpretation
    
    def _get_uc_interpretation(self, extent: str, severity: str) -> str:
        """Provides clinical interpretation for ulcerative colitis classification"""
        
        interpretation = f"Montreal Classification {extent}{severity}. "
        
        # Extent-specific guidance
        extent_guidance = {
            "E1": "Proctitis has excellent prognosis with topical therapy often sufficient. Low cancer risk.",
            "E2": "Left-sided colitis may require combination oral and topical therapy. Moderate cancer risk after 15-20 years.",
            "E3": "Extensive colitis requires systemic therapy. Highest cancer risk - surveillance colonoscopy recommended."
        }
        
        # Severity-specific guidance
        severity_guidance = {
            "S0": "Clinical remission - maintain with appropriate therapy and monitor for relapse.",
            "S1": "Mild activity may respond to topical or mild systemic therapy. Monitor closely.",
            "S2": "Moderate activity requires systemic therapy. Consider hospitalization if poor response.",
            "S3": "Severe activity requires hospitalization and intensive medical therapy. Consider surgery if refractory."
        }
        
        interpretation += extent_guidance[extent] + " " + severity_guidance[severity]
        interpretation += " This classification guides treatment intensity and surveillance strategies."
        
        return interpretation


def calculate_montreal_classification_ibd(disease_type: str, age_at_diagnosis: int,
                                        crohns_location: Optional[str] = None,
                                        crohns_behavior: Optional[str] = None,
                                        perianal_disease: Optional[str] = None,
                                        uc_extent: Optional[str] = None,
                                        uc_severity: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MontrealClassificationIbdCalculator()
    return calculator.calculate(disease_type, age_at_diagnosis, crohns_location,
                               crohns_behavior, perianal_disease, uc_extent, uc_severity)