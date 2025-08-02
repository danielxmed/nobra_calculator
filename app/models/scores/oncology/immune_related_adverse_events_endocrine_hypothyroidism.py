"""
Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism Models

Request and response models for immune-related adverse events endocrine hypothyroidism grading.

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

3. Faje AT, Sullivan R, Lawrence D, Trombetta M, Fadden R, Klibanski A, et al. 
   Ipilimumab-induced hypophysitis: a detailed longitudinal analysis in a large 
   cohort of patients with metastatic melanoma. J Clin Endocrinol Metab. 
   2014 Nov;99(11):4078-85. doi: 10.1210/jc.2014-2306.

4. Barroso-Sousa R, Barry WT, Garrido-Castro AC, Hodi FS, Min Y, Krop IE, et al. 
   Incidence of Endocrine Dysfunction Following the Use of Different Immune 
   Checkpoint Inhibitor Regimens: A Systematic Review and Meta-analysis. 
   JAMA Oncol. 2018 Feb 1;4(2):173-182. doi: 10.1001/jamaoncol.2017.3064.

The immune-related adverse events (irAE) grading system for endocrine toxicities 
specifically addresses hypothyroidism induced by immune checkpoint inhibitors (ICPi). 
This grading system is based on Common Terminology Criteria for Adverse Events (CTCAE) 
Version 5.0 and provides standardized criteria for assessing hypothyroidism severity 
and guiding clinical management decisions. ICPi-induced hypothyroidism is more common 
with anti-PD-1/PD-L1 agents than anti-CTLA-4 therapy and can occur at any time during 
treatment, often requiring lifelong thyroid hormone replacement therapy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsEndocrineHypothyroidismRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism
    
    This grading system evaluates hypothyroidism severity in patients receiving immune 
    checkpoint inhibitor therapy based on three key clinical parameters:
    
    Grading Criteria:
    - Grade 1: TSH <10 mIU/L, asymptomatic - Continue ICPi with monitoring
    - Grade 2: TSH >10 mIU/L OR moderate symptoms with ADL preservation - May hold ICPi, consider hormone replacement
    - Grade 3: Severe symptoms, unable to perform ADLs - Hold ICPi, urgent endocrinology consultation
    - Grade 4: Myxedema coma or life-threatening complications - Immediate hospitalization, IV hormone replacement
    
    Clinical Context:
    - More common with anti-PD-1/PD-L1 agents (pembrolizumab, nivolumab) than anti-CTLA-4
    - Can occur at any time during ICPi treatment, often irreversible
    - TSH elevation may precede clinical symptoms by weeks to months
    - Normal TSH range typically 0.4-4.0 mIU/L (varies by laboratory)
    - Most patients require lifelong thyroid hormone replacement
    
    Management Principles:
    - Grade 1: Continue ICPi, monitor TSH/free T4 every 4-6 weeks
    - Grade 2: Consider endocrinology consultation, thyroid hormone supplementation
    - Grade 3-4: Hold ICPi, urgent consultation, immediate hormone replacement
    
    Monitoring Parameters:
    - TSH and free thyroxine (T4) levels
    - Thyroid peroxidase (TPO) and thyroglobulin antibodies
    - Screen for concurrent adrenal insufficiency (up to 50% association)
    - Distinguish primary from secondary hypothyroidism
    
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
    3. Faje AT, Sullivan R, Lawrence D, Trombetta M, Fadden R, Klibanski A, et al. 
    Ipilimumab-induced hypophysitis: a detailed longitudinal analysis in a large 
    cohort of patients with metastatic melanoma. J Clin Endocrinol Metab. 
    2014 Nov;99(11):4078-85. doi: 10.1210/jc.2014-2306.
    4. Barroso-Sousa R, Barry WT, Garrido-Castro AC, Hodi FS, Min Y, Krop IE, et al. 
    Incidence of Endocrine Dysfunction Following the Use of Different Immune 
    Checkpoint Inhibitor Regimens: A Systematic Review and Meta-analysis. 
    JAMA Oncol. 2018 Feb 1;4(2):173-182. doi: 10.1001/jamaoncol.2017.3064.
    """
    
    tsh_miu_l: float = Field(
        ...,
        description="Thyroid-stimulating hormone (TSH) level in mIU/L. Normal range typically 0.4-4.0 mIU/L (varies by laboratory). Key threshold: TSH >10 mIU/L warrants at least Grade 2 classification. Elevated TSH indicates primary hypothyroidism from thyroid gland dysfunction",
        example=15.2,
        ge=0.01,
        le=100.0
    )
    
    symptom_severity: Literal["asymptomatic", "moderate_able_adls", "severe_unable_adls"] = Field(
        ...,
        description="Patient symptom severity and functional status assessment. Asymptomatic: no clinical symptoms despite TSH elevation. Moderate (able ADLs): symptoms like fatigue, cold intolerance, weight gain, but can perform daily activities. Severe (unable ADLs): significant symptoms preventing normal activities, may include bradycardia, cognitive impairment, severe fatigue",
        example="moderate_able_adls"
    )
    
    myxedema_signs: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of myxedema coma or life-threatening hypothyroid complications. Includes: altered mental status, hypothermia (<95°F), bradycardia, hypotension, hyponatremia, respiratory depression, or coma. Myxedema coma has 20-60% mortality rate and requires immediate intensive care",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tsh_miu_l": 15.2,
                "symptom_severity": "moderate_able_adls",
                "myxedema_signs": "no"
            }
        }


class ImmuneRelatedAdverseEventsEndocrineHypothyroidismResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for Endocrine Toxicities - Hypothyroidism
    
    The irAE grading system provides standardized assessment of hypothyroidism severity 
    and evidence-based management recommendations for immune checkpoint inhibitor-induced 
    thyroid dysfunction:
    
    Grade 1 (Mild): Continue ICPi with close monitoring
    Grade 2 (Moderate): May hold ICPi, consider hormone replacement
    Grade 3 (Severe): Hold ICPi, urgent endocrinology consultation
    Grade 4 (Life-threatening): Immediate hospitalization, IV hormone replacement
    
    Clinical Implications:
    - Grade 2+ typically requires endocrinology consultation and hormone replacement
    - Most patients require lifelong thyroid hormone replacement therapy
    - ICPi therapy can often be resumed after hormone replacement initiated
    - Monitor for concurrent adrenal insufficiency in up to 50% of cases
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="irAE grade for endocrine hypothyroidism based on CTCAE v5.0 criteria (range: 1-4)",
        example=2,
        ge=1,
        le=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grading system",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed management recommendations including ICPi therapy decisions, hormone replacement needs, monitoring requirements, and consultation recommendations",
        example="May hold ICPi until symptoms resolve. Consider endocrinology consultation for thyroid hormone replacement therapy. Consider thyroid hormone supplementation with levothyroxine. Monitor TSH every 6-8 weeks. Use free thyroxine monitoring short-term if needed. Resume ICPi when symptoms controlled."
    )
    
    stage: str = Field(
        ...,
        description="irAE grade classification with severity descriptor",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade severity and clinical presentation",
        example="Moderate - Moderate symptoms, able to perform ADLs, TSH >10 mIU/L"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "May hold ICPi until symptoms resolve. Consider endocrinology consultation for thyroid hormone replacement therapy. Consider thyroid hormone supplementation with levothyroxine. Monitor TSH every 6-8 weeks. Use free thyroxine monitoring short-term if needed. Resume ICPi when symptoms controlled.",
                "stage": "Grade 2",
                "stage_description": "Moderate - Moderate symptoms, able to perform ADLs, TSH >10 mIU/L"
            }
        }