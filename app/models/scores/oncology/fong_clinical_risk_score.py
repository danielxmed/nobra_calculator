"""
Fong Clinical Risk Score for Colorectal Cancer Recurrence Models

Request and response models for Fong Clinical Risk Score calculation.

References (Vancouver style):
1. Fong Y, Fortner J, Sun RL, Brennan MF, Blumgart LH. Clinical score for predicting recurrence 
   after hepatic resection for metastatic colorectal cancer: analysis of 1001 consecutive cases. 
   Ann Surg. 1999;230(3):309-318. doi: 10.1097/00000658-199909000-00004.
2. Mala T, Bohler G, Mathisen O, Bergan A, Soreide O. Hepatic resection for colorectal metastases: 
   can preoperative scoring predict patient outcome? World J Surg. 2002;26(11):1348-1353. 
   doi: 10.1007/s00268-002-6231-x.
3. Mann CD, Metcalfe MS, Leopardi LN, Maddern GJ. The clinical risk score: emerging as a reliable 
   preoperative prognostic index in hepatectomy for colorectal metastases. Arch Surg. 
   2004;139(11):1168-1172. doi: 10.1001/archsurg.139.11.1168.
4. Nordlinger B, Guiguet M, Vaillant JC, et al. Surgical resection of colorectal carcinoma 
   metastases to the liver. A prognostic scoring system to improve case selection, based on 
   1568 patients. Cancer. 1996;77(7):1254-1262.

The Fong Clinical Risk Score was developed at Memorial Sloan-Kettering Cancer Center from 
analysis of 1,001 consecutive patients undergoing hepatic resection for colorectal liver 
metastases between 1985-1998. This simple 5-parameter scoring system predicts both overall 
survival and disease-free survival after liver resection.

The score identifies five independent prognostic factors:
1. Node-positive primary tumor (N1-N2 vs N0)
2. Disease-free interval <12 months from primary to liver metastasis
3. Multiple (>1) liver metastases 
4. Preoperative CEA level >200 ng/mL
5. Largest liver metastasis >5 cm

Clinical Application:
- Risk stratification for surgical planning
- Patient counseling regarding prognosis
- Selection for adjuvant therapy trials
- Postoperative surveillance planning
- Not intended to exclude patients from surgery
"""

from pydantic import BaseModel, Field
from typing import Literal


class FongClinicalRiskScoreRequest(BaseModel):
    """
    Request model for Fong Clinical Risk Score for Colorectal Cancer Recurrence
    
    The Fong Clinical Risk Score uses five clinical parameters to predict survival after 
    hepatic resection for colorectal liver metastases. Each parameter contributes 1 point:
    
    **Scoring Parameters (1 point each):**
    
    1. **Node-positive primary tumor**: Lymph node involvement (N1 or N2) at the primary 
       colorectal cancer site indicates more aggressive disease biology
    
    2. **Disease-free interval <12 months**: Short interval between primary resection and 
       liver metastasis detection suggests rapid disease progression
    
    3. **Multiple liver tumors**: Presence of >1 liver metastasis indicates more extensive 
       hepatic disease burden
    
    4. **Preoperative CEA >200 ng/mL**: Elevated carcinoembryonic antigen reflects high 
       tumor burden and aggressive disease
    
    5. **Largest tumor >5 cm**: Large tumor size correlates with advanced local disease 
       and potential for micrometastases
    
    **Score Interpretation:**
    - Score 0-2: Favorable prognosis (5-year survival 30-60%)
    - Score 3-5: Poor prognosis (5-year survival 11-16%)
    - Patients with scores ≥3 should be considered for adjuvant therapy

    References (Vancouver style):
    1. Fong Y, Fortner J, Sun RL, Brennan MF, Blumgart LH. Clinical score for predicting recurrence 
       after hepatic resection for metastatic colorectal cancer: analysis of 1001 consecutive cases. 
       Ann Surg. 1999;230(3):309-318. doi: 10.1097/00000658-199909000-00004.
    2. Mala T, Bohler G, Mathisen O, Bergan A, Soreide O. Hepatic resection for colorectal metastases: 
       can preoperative scoring predict patient outcome? World J Surg. 2002;26(11):1348-1353. 
       doi: 10.1007/s00268-002-6231-x.
    3. Mann CD, Metcalfe MS, Leopardi LN, Maddern GJ. The clinical risk score: emerging as a reliable 
       preoperative prognostic index in hepatectomy for colorectal metastases. Arch Surg. 
       2004;139(11):1168-1172. doi: 10.1001/archsurg.139.11.1168.
    """
    
    node_positive_primary: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Lymph node involvement at primary colorectal cancer site. "
            "Node-positive disease (N1 or N2) scores 1 point. "
            "Indicates more aggressive tumor biology and higher recurrence risk."
        ),
        example="no"
    )
    
    disease_free_interval: Literal["less_than_12_months", "12_months_or_more"] = Field(
        ...,
        description=(
            "Time interval from primary tumor resection to liver metastasis detection. "
            "Interval <12 months scores 1 point. "
            "Short interval suggests rapid disease progression and worse prognosis."
        ),
        example="12_months_or_more"
    )
    
    number_of_tumors: Literal["single", "multiple"] = Field(
        ...,
        description=(
            "Number of liver metastases present. "
            "Multiple (>1) tumors score 1 point. "
            "Multiple lesions indicate more extensive hepatic disease burden."
        ),
        example="single"
    )
    
    cea_level: Literal["200_or_less", "greater_than_200"] = Field(
        ...,
        description=(
            "Preoperative carcinoembryonic antigen (CEA) level in ng/mL. "
            "CEA >200 ng/mL scores 1 point. "
            "Elevated CEA reflects high tumor burden and aggressive disease biology."
        ),
        example="200_or_less"
    )
    
    largest_tumor_size: Literal["5_cm_or_less", "greater_than_5_cm"] = Field(
        ...,
        description=(
            "Size of the largest liver metastasis in centimeters. "
            "Largest tumor >5 cm scores 1 point. "
            "Large tumors correlate with advanced disease and potential micrometastases."
        ),
        example="5_cm_or_less"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "node_positive_primary": "no",
                "disease_free_interval": "12_months_or_more",
                "number_of_tumors": "single",
                "cea_level": "200_or_less",
                "largest_tumor_size": "5_cm_or_less"
            }
        }


class FongClinicalRiskScoreResponse(BaseModel):
    """
    Response model for Fong Clinical Risk Score for Colorectal Cancer Recurrence
    
    The Fong Clinical Risk Score ranges from 0-5 points and provides prognostic information 
    for patients undergoing hepatic resection for colorectal liver metastases.
    
    **Score Interpretation:**
    - **Score 0**: Excellent prognosis (5-year survival ~60%)
    - **Score 1**: Good prognosis (5-year survival ~44%)
    - **Score 2**: Moderate prognosis (5-year survival ~30%)
    - **Score 3**: Poor prognosis (5-year survival ~16%)
    - **Score 4**: Very poor prognosis (5-year survival ~11%)
    - **Score 5**: Extremely poor prognosis (5-year survival ~14%)
    
    **Clinical Applications:**
    - Risk stratification for surgical planning
    - Patient counseling regarding expected outcomes
    - Selection criteria for adjuvant therapy trials
    - Postoperative surveillance intensity planning
    
    **Treatment Implications:**
    - Scores 0-2: Favorable outcome expected, proceed with resection
    - Scores 3-5: Consider adjuvant therapy or alternative treatment strategies
    - High scores may benefit from neoadjuvant chemotherapy before resection
    
    Reference: Fong Y, et al. Ann Surg. 1999;230(3):309-318.
    """
    
    result: int = Field(
        ...,
        description="Fong Clinical Risk Score calculated from the five clinical parameters (range: 0-5 points)",
        ge=0,
        le=5,
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including prognosis, survival estimate, and treatment recommendations",
        example="5-year survival rate approximately 44%. Favorable outcome expected after hepatic resection. Good candidate for surgical intervention with acceptable long-term survival."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category based on the calculated score",
        example="Score 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Good prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "5-year survival rate approximately 44%. Favorable outcome expected after hepatic resection. Good candidate for surgical intervention with acceptable long-term survival.",
                "stage": "Score 1",
                "stage_description": "Good prognosis"
            }
        }