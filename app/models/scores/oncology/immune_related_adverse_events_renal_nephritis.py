"""
Immune-Related Adverse Events for Renal Toxicities - Nephritis Models

Request and response models for immune-related nephritis grading.

References (Vancouver style):
1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
   Management of Immune-Related Adverse Events in Patients Treated With Immune 
   Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
   Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
   doi: 10.1200/JCO.2017.77.6385.
2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
   NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
   Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
   doi: 10.6004/jnccn.2020.0012.
3. Cortazar FB, Marrone KA, Troxel AB, Ralto KM, Hoenig MP, Brahmer JR, et al. 
   Clinicopathological features of acute kidney injury associated with immune 
   checkpoint inhibitors. Kidney Int. 2016 Sep;90(3):638-47. 
   doi: 10.1016/j.kint.2016.04.008.
4. Shirali AC, Perazella MA, Gettinger S. Association of Acute Interstitial 
   Nephritis With Programmed Cell Death 1 Inhibitor Therapy in Lung Cancer Patients. 
   Am J Kidney Dis. 2016 Aug;68(2):287-91. doi: 10.1053/j.ajkd.2016.02.057.

The immune-related nephritis grading system is based on CTCAE Version 5.0 criteria
and helps determine the severity of nephritis secondary to immune checkpoint inhibitor
therapy. This standardized grading evaluates serum creatinine fold increase over baseline
along with clinical symptoms to guide treatment decisions including ICPi therapy
continuation, corticosteroid treatment, and nephrology consultation needs. ICPi-induced
nephritis has an incidence of 1-2% in single-agent therapy and 4.5% in combination
therapy, with median onset at 14 weeks.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsRenalNephritisRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for Renal Toxicities - Nephritis
    
    Grades severity of nephritis secondary to immune checkpoint inhibitor (ICPi) therapy
    based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 criteria.
    
    CTCAE Grading Criteria:
    - Grade 1: Creatinine increase 1.5-2× baseline
    - Grade 2: Creatinine increase 2-3× baseline
    - Grade 3: Creatinine increase >3-6× baseline
    - Grade 4: Creatinine increase >6× baseline OR dialysis required
    
    Clinical Parameters:
    - Baseline and current creatinine levels (mg/dL)
    - Proteinuria presence (may indicate glomerular involvement)
    - Hematuria presence (suggests more severe nephritis)
    - Clinical symptoms severity (asymptomatic to severe)
    - Fluid retention evidence (edema, weight gain, volume overload)
    - Dialysis requirement (automatic Grade 4)
    
    ICPi-induced nephritis typically presents as acute tubulointerstitial nephritis (AIN)
    with median onset at 14 weeks. Early recognition and grading are essential for
    appropriate management decisions including ICPi continuation, corticosteroid
    initiation, and nephrology consultation.

    References (Vancouver style):
    1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
       Management of Immune-Related Adverse Events in Patients Treated With Immune 
       Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
       Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
       doi: 10.1200/JCO.2017.77.6385.
    2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
       NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
       Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
       doi: 10.6004/jnccn.2020.0012.
    3. Cortazar FB, Marrone KA, Troxel AB, Ralto KM, Hoenig MP, Brahmer JR, et al. 
       Clinicopathological features of acute kidney injury associated with immune 
       checkpoint inhibitors. Kidney Int. 2016 Sep;90(3):638-47. 
       doi: 10.1016/j.kint.2016.04.008.
    """
    
    baseline_creatinine: float = Field(
        ...,
        description="Baseline serum creatinine level in mg/dL before ICPi therapy initiation. Essential reference point for calculating fold increase. Normal range typically 0.6-1.2 mg/dL but varies by age, sex, muscle mass, and laboratory",
        example=1.0,
        ge=0.3,
        le=15.0
    )
    
    current_creatinine: float = Field(
        ...,
        description="Current serum creatinine level in mg/dL. Used to calculate fold increase over baseline for CTCAE grading. Significant elevation indicates renal impairment and possible nephritis",
        example=2.5,
        ge=0.3,
        le=30.0
    )
    
    proteinuria_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of proteinuria on urinalysis or urine protein/creatinine ratio. May indicate glomerular involvement in addition to interstitial nephritis. Important for differential diagnosis and prognosis",
        example="yes"
    )
    
    hematuria_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of hematuria (blood in urine) on urinalysis. May suggest glomerular disease or more severe nephritis. Important for determining need for kidney biopsy and management approach",
        example="no"
    )
    
    clinical_symptoms: Literal["asymptomatic", "mild", "moderate", "severe"] = Field(
        ...,
        description="Presence of clinical symptoms related to nephritis. Asymptomatic: no symptoms, lab changes only. Mild: minimal symptoms not affecting daily activities. Moderate: symptoms interfering with daily activities. Severe: significant symptoms limiting self-care",
        example="mild"
    )
    
    fluid_retention: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of fluid retention including edema, weight gain, or volume overload. May manifest as facial, abdominal, or extremity edema, sudden weight gain, or hypertension. Indicates more severe nephritis",
        example="no"
    )
    
    dialysis_required: Literal["yes", "no"] = Field(
        ...,
        description="Need for renal replacement therapy (hemodialysis, peritoneal dialysis, or continuous renal replacement therapy). Indicates Grade 4 severity regardless of other parameters. Life-threatening complication",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "baseline_creatinine": 1.0,
                "current_creatinine": 2.5,
                "proteinuria_present": "yes",
                "hematuria_present": "no",
                "clinical_symptoms": "mild",
                "fluid_retention": "no",
                "dialysis_required": "no"
            }
        }


class ImmuneRelatedAdverseEventsRenalNephritisResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for Renal Toxicities - Nephritis
    
    Returns the CTCAE grade (1-4) for immune-related nephritis with clinical interpretation
    and management recommendations. Grading is primarily based on serum creatinine fold
    increase over baseline with additional consideration of clinical factors.
    
    Grade Categories:
    - Grade 1 (Mild): Creatinine 1.5-2× baseline - Continue ICPi with monitoring
    - Grade 2 (Moderate): Creatinine 2-3× baseline - Hold ICPi, start corticosteroids
    - Grade 3 (Severe): Creatinine >3-6× baseline - Permanently discontinue ICPi
    - Grade 4 (Life-threatening): Creatinine >6× baseline or dialysis - Emergency management
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="CTCAE grade for immune-related nephritis (1-4) based on creatinine fold increase and clinical factors",
        example=2,
        ge=1,
        le=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grade",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and evidence-based management recommendations based on the grade",
        example="Hold ICPi until creatinine improves to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain nephrology consultation. Rule out infectious and obstructive causes. Consider kidney biopsy if diagnosis unclear or no improvement. Monitor creatinine closely. Resume ICPi when grade ≤1 and steroids tapered."
    )
    
    stage: str = Field(
        ...,
        description="CTCAE grade category (Grade 1, Grade 2, Grade 3, or Grade 4)",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="Moderate - Creatinine 2-3× baseline"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Hold ICPi until creatinine improves to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain nephrology consultation. Rule out infectious and obstructive causes. Consider kidney biopsy if diagnosis unclear or no improvement. Monitor creatinine closely. Resume ICPi when grade ≤1 and steroids tapered.",
                "stage": "Grade 2",
                "stage_description": "Moderate - Creatinine 2-3× baseline"
            }
        }