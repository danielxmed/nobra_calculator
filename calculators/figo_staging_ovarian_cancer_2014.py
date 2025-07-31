"""
FIGO Staging for Ovarian Cancer (2014) Calculator

Stages ovarian, fallopian tube, and peritoneal cancer based on anatomical spread of disease.

References:
- Prat J; FIGO Committee on Gynecologic Oncology. Staging classification for cancer 
  of the ovary, fallopian tube, and peritoneum. Int J Gynaecol Obstet. 2014;124(1):1-5.
- Mutch DG, Prat J. 2014 FIGO staging for ovarian, fallopian tube and peritoneal 
  cancer. Gynecol Oncol. 2014;133(3):401-4.
"""

import math
from typing import Dict, Any


class FigoStagingOvarianCancer2014Calculator:
    """Calculator for FIGO Staging for Ovarian Cancer (2014)"""
    
    def __init__(self):
        # Stage mapping based on tumor location
        self.stage_mapping = {
            "confined_one_ovary_tube_intact": {
                "stage": "IA",
                "description": "Tumor limited to one ovary/tube, capsule intact",
                "prognosis": "5-year survival 87-98%, recurrence rate ~11%"
            },
            "confined_both_ovaries_tubes_intact": {
                "stage": "IB",
                "description": "Tumor limited to both ovaries/tubes, capsules intact",
                "prognosis": "5-year survival 87-98%, similar to IA"
            },
            "confined_surgical_spill": {
                "stage": "IC1",
                "description": "Tumor confined with surgical spill",
                "prognosis": "5-year survival ~62%, higher recurrence risk"
            },
            "confined_capsule_rupture_or_surface": {
                "stage": "IC2",
                "description": "Capsule ruptured before surgery or tumor on surface",
                "prognosis": "5-year survival ~78%"
            },
            "confined_positive_washings": {
                "stage": "IC3",
                "description": "Malignant cells in ascites or peritoneal washings",
                "prognosis": "5-year survival ~59%, worse prognosis due to positive washings"
            },
            "pelvic_extension_uterus_tubes_ovaries": {
                "stage": "IIA",
                "description": "Extension to uterus and/or fallopian tubes/ovaries",
                "prognosis": "5-year survival ~42%, requires adjuvant chemotherapy"
            },
            "pelvic_extension_other_tissues": {
                "stage": "IIB",
                "description": "Extension to other pelvic intraperitoneal tissues",
                "prognosis": "5-year survival ~42%, requires adjuvant chemotherapy"
            },
            "positive_retroperitoneal_nodes_only_10mm_or_less": {
                "stage": "IIIA1(i)",
                "description": "Positive retroperitoneal lymph nodes ≤10 mm",
                "prognosis": "Better prognosis when only lymph nodes involved"
            },
            "positive_retroperitoneal_nodes_only_more_than_10mm": {
                "stage": "IIIA1(ii)",
                "description": "Positive retroperitoneal lymph nodes >10 mm",
                "prognosis": "Better prognosis when only lymph nodes involved"
            },
            "microscopic_extrapelvic_peritoneal": {
                "stage": "IIIA2",
                "description": "Microscopic extrapelvic peritoneal involvement",
                "prognosis": "5-year survival 21-35%, depends on residual disease"
            },
            "macroscopic_peritoneal_2cm_or_less": {
                "stage": "IIIB",
                "description": "Macroscopic peritoneal metastasis ≤2 cm",
                "prognosis": "5-year survival 21-35%, depends on residual disease"
            },
            "macroscopic_peritoneal_more_than_2cm": {
                "stage": "IIIC",
                "description": "Macroscopic peritoneal metastasis >2 cm",
                "prognosis": "5-year survival 21-35%, worse with large volume disease"
            },
            "pleural_effusion_positive_cytology": {
                "stage": "IVA",
                "description": "Pleural effusion with positive cytology",
                "prognosis": "5-year survival 6-20%, median survival ~25 months"
            },
            "parenchymal_or_extra_abdominal_metastases": {
                "stage": "IVB",
                "description": "Parenchymal or extra-abdominal metastases",
                "prognosis": "5-year survival 6-20%, median survival ~28 months"
            }
        }
    
    def calculate(self, tumor_location: str) -> Dict[str, Any]:
        """
        Determines the FIGO stage based on tumor location
        
        Args:
            tumor_location (str): Location and extent of primary tumor
            
        Returns:
            Dict with the FIGO stage and interpretation
        """
        
        # Validations
        self._validate_inputs(tumor_location)
        
        # Get stage information
        stage_info = self.stage_mapping[tumor_location]
        
        # Get interpretation
        interpretation = self._get_interpretation(stage_info)
        
        return {
            "result": stage_info["stage"],
            "unit": "",
            "interpretation": interpretation,
            "stage": stage_info["stage"],
            "stage_description": stage_info["description"]
        }
    
    def _validate_inputs(self, tumor_location):
        """Validates input parameters"""
        
        if tumor_location not in self.stage_mapping:
            raise ValueError(f"Invalid tumor location. Must be one of: {', '.join(self.stage_mapping.keys())}")
    
    def _get_interpretation(self, stage_info: Dict[str, str]) -> str:
        """
        Provides comprehensive interpretation based on stage
        
        Args:
            stage_info (Dict): Stage information including stage, description, and prognosis
            
        Returns:
            str: Detailed clinical interpretation
        """
        
        stage = stage_info["stage"]
        description = stage_info["description"]
        prognosis = stage_info["prognosis"]
        
        # Get major stage group for general interpretation
        major_stage = stage[0]  # First character (I, II, III, or IV)
        
        base_interpretations = {
            "I": "Stage I disease is confined to the ovaries or fallopian tubes. Generally has excellent prognosis with appropriate treatment.",
            "II": "Stage II disease involves pelvic extension. Moderate prognosis with adjuvant chemotherapy required.",
            "III": "Stage III disease involves peritoneal spread or lymph node metastases. Advanced disease requiring aggressive treatment.",
            "IV": "Stage IV disease involves distant metastases. Poor prognosis but some patients achieve long-term survival with optimal treatment."
        }
        
        base_interpretation = base_interpretations.get(major_stage, "")
        
        # Combine all information
        interpretation = f"FIGO Stage {stage}: {description}. {base_interpretation} {prognosis}"
        
        # Add specific recommendations based on stage
        if stage.startswith("I"):
            interpretation += " Consider fertility-sparing surgery in young patients with stage IA/IB. Stage IC requires adjuvant chemotherapy."
        elif stage.startswith("II"):
            interpretation += " Complete surgical staging followed by platinum-based chemotherapy is standard."
        elif stage.startswith("III"):
            interpretation += " Optimal cytoreductive surgery followed by platinum/taxane chemotherapy. Consider neoadjuvant chemotherapy if optimal debulking unlikely."
        elif stage.startswith("IV"):
            interpretation += " Systemic chemotherapy is primary treatment. Consider palliative surgery if symptomatic. Clinical trials may offer additional options."
        
        return interpretation


def calculate_figo_staging_ovarian_cancer_2014(tumor_location) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FigoStagingOvarianCancer2014Calculator()
    return calculator.calculate(tumor_location)