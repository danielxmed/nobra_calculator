"""
FIGO Staging for Ovarian Cancer (2014) Models

Request and response models for FIGO staging calculation.

References (Vancouver style):
1. Prat J; FIGO Committee on Gynecologic Oncology. Staging classification for 
   cancer of the ovary, fallopian tube, and peritoneum. Int J Gynaecol Obstet. 
   2014 Jan;124(1):1-5. doi: 10.1016/j.ijgo.2013.10.001. PMID: 24219974.
2. Mutch DG, Prat J. 2014 FIGO staging for ovarian, fallopian tube and peritoneal 
   cancer. Gynecol Oncol. 2014 Jun;133(3):401-4. doi: 10.1016/j.ygyno.2014.04.013. 
   PMID: 24878391.
3. Berek JS, Kehoe ST, Kumar L, Friedlander M. Cancer of the ovary, fallopian tube, 
   and peritoneum. Int J Gynaecol Obstet. 2018 Oct;143 Suppl 2:59-78. 
   doi: 10.1002/ijgo.12614. PMID: 30306591.

The FIGO 2014 staging system provides a standardized anatomical classification for 
ovarian, fallopian tube, and primary peritoneal cancer. It stratifies patients based 
on the extent of disease spread, which correlates with prognosis and guides treatment 
decisions. The system includes detailed substages that reflect important prognostic 
factors such as surgical spill, capsule rupture, and lymph node size.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FigoStagingOvarianCancer2014Request(BaseModel):
    """
    Request model for FIGO Staging for Ovarian Cancer (2014) calculation
    
    The FIGO staging system classifies ovarian, fallopian tube, and peritoneal cancer 
    based on anatomical spread of disease. Selection is based on surgical and pathological 
    findings at the time of initial diagnosis.
    
    Stage Categories:
    - Stage I: Tumor confined to ovaries or fallopian tubes
    - Stage II: Tumor with pelvic extension
    - Stage III: Tumor with peritoneal spread beyond pelvis or lymph node metastases
    - Stage IV: Distant metastases
    
    Key Staging Considerations:
    - Primary site (ovary, fallopian tube, or peritoneum) must be designated
    - Lymph node involvement must be cytologically or histologically proven
    - Staging is based on findings at laparotomy
    - Pleural effusion requires positive cytology for stage IVA
    - Liver capsule involvement = Stage IIIC; liver parenchymal metastases = Stage IVB
    
    References (Vancouver style):
    1. Prat J; FIGO Committee on Gynecologic Oncology. Int J Gynaecol Obstet. 2014;124(1):1-5.
    2. Mutch DG, Prat J. Gynecol Oncol. 2014;133(3):401-4.
    """
    
    tumor_location: Literal[
        "confined_one_ovary_tube_intact",
        "confined_both_ovaries_tubes_intact",
        "confined_surgical_spill",
        "confined_capsule_rupture_or_surface",
        "confined_positive_washings",
        "pelvic_extension_uterus_tubes_ovaries",
        "pelvic_extension_other_tissues",
        "positive_retroperitoneal_nodes_only_10mm_or_less",
        "positive_retroperitoneal_nodes_only_more_than_10mm",
        "microscopic_extrapelvic_peritoneal",
        "macroscopic_peritoneal_2cm_or_less",
        "macroscopic_peritoneal_more_than_2cm",
        "pleural_effusion_positive_cytology",
        "parenchymal_or_extra_abdominal_metastases"
    ] = Field(
        ...,
        description="""Location and extent of primary tumor. Select the most advanced finding:
        
        STAGE I - Confined to ovaries/tubes:
        • confined_one_ovary_tube_intact: Tumor limited to one ovary/tube, capsule intact, no surface tumor, negative washings (Stage IA)
        • confined_both_ovaries_tubes_intact: Tumor limited to both ovaries/tubes, capsules intact, no surface tumor, negative washings (Stage IB)
        • confined_surgical_spill: Surgical spill intraoperatively (Stage IC1)
        • confined_capsule_rupture_or_surface: Capsule ruptured before surgery OR tumor on ovarian/tubal surface (Stage IC2)
        • confined_positive_washings: Malignant cells in ascites or peritoneal washings (Stage IC3)
        
        STAGE II - Pelvic extension:
        • pelvic_extension_uterus_tubes_ovaries: Extension/implants on uterus and/or tubes/ovaries (Stage IIA)
        • pelvic_extension_other_tissues: Extension to other pelvic intraperitoneal tissues (Stage IIB)
        
        STAGE III - Peritoneal/nodal spread:
        • positive_retroperitoneal_nodes_only_10mm_or_less: Positive retroperitoneal lymph nodes only, ≤10mm (Stage IIIA1(i))
        • positive_retroperitoneal_nodes_only_more_than_10mm: Positive retroperitoneal lymph nodes only, >10mm (Stage IIIA1(ii))
        • microscopic_extrapelvic_peritoneal: Microscopic extrapelvic peritoneal involvement (Stage IIIA2)
        • macroscopic_peritoneal_2cm_or_less: Macroscopic peritoneal metastasis ≤2cm (Stage IIIB)
        • macroscopic_peritoneal_more_than_2cm: Macroscopic peritoneal metastasis >2cm, includes liver/spleen capsule (Stage IIIC)
        
        STAGE IV - Distant metastases:
        • pleural_effusion_positive_cytology: Pleural effusion with positive cytology (Stage IVA)
        • parenchymal_or_extra_abdominal_metastases: Liver/spleen parenchymal metastases, extra-abdominal organs (Stage IVB)""",
        example="confined_positive_washings"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tumor_location": "confined_positive_washings"
            }
        }


class FigoStagingOvarianCancer2014Response(BaseModel):
    """
    Response model for FIGO Staging for Ovarian Cancer (2014) calculation
    
    The FIGO stage provides critical prognostic information:
    
    Survival by Stage:
    - Stage I: 5-year survival 76-90% (IA/IB: 87-98%, IC: 59-78%)
    - Stage II: 5-year survival ~42%
    - Stage III: 5-year survival 21-35%
    - Stage IV: 5-year survival 6-20%
    
    Treatment Implications:
    - Stage I: May allow fertility-sparing surgery in young patients (IA/IB)
    - Stage IC-IV: Require adjuvant platinum-based chemotherapy
    - Stage III-IV: Consider neoadjuvant chemotherapy if optimal debulking unlikely
    - Stage IV: Primary systemic therapy, palliative care considerations
    
    Reference: Prat J, et al. Int J Gynaecol Obstet. 2014;124(1):1-5.
    """
    
    result: str = Field(
        ...,
        description="FIGO stage classification (e.g., IA, IC3, IIIA1(i), IVB)",
        example="IC3"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for staging systems)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including prognosis and treatment recommendations",
        example="FIGO Stage IC3: Malignant cells in ascites or peritoneal washings. Stage I disease is confined to the ovaries or fallopian tubes. Generally has excellent prognosis with appropriate treatment. 5-year survival ~59%, worse prognosis due to positive washings. Consider fertility-sparing surgery in young patients with stage IA/IB. Stage IC requires adjuvant chemotherapy."
    )
    
    stage: str = Field(
        ...,
        description="FIGO stage classification",
        example="IC3"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stage criteria",
        example="Malignant cells in ascites or peritoneal washings"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "IC3",
                "unit": "",
                "interpretation": "FIGO Stage IC3: Malignant cells in ascites or peritoneal washings. Stage I disease is confined to the ovaries or fallopian tubes. Generally has excellent prognosis with appropriate treatment. 5-year survival ~59%, worse prognosis due to positive washings. Consider fertility-sparing surgery in young patients with stage IA/IB. Stage IC requires adjuvant chemotherapy.",
                "stage": "IC3",
                "stage_description": "Malignant cells in ascites or peritoneal washings"
            }
        }