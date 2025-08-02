"""
Immune-Related Adverse Events for Lung Toxicity - Pneumonitis Models

Request and response models for immune-related adverse events lung pneumonitis grading.

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

3. Nishino M, Giobbie-Hurder A, Hatabu H, Ramaiya NH, Hodi FS. Incidence of 
   Programmed Cell Death 1 Inhibitor-Related Pneumonitis in Patients With Advanced 
   Cancer: A Systematic Review and Meta-analysis. JAMA Oncol. 2016 Dec 1;2(12):1607-1616. 
   doi: 10.1001/jamaoncol.2016.2453.

4. Naidoo J, Wang X, Woo KM, Iyriboz T, Halpenny D, Cunningham J, et al. Pneumonitis 
   in Patients Treated With Anti-Programmed Death-1/Programmed Death Ligand 1 Therapy. 
   J Clin Oncol. 2017 Mar 10;35(7):709-717. doi: 10.1200/JCO.2016.68.2005.

The immune-related adverse events (irAE) grading system for lung toxicity specifically 
addresses pneumonitis induced by immune checkpoint inhibitors (ICPi). This grading system 
is based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 and 
provides standardized criteria for assessing pneumonitis severity and guiding clinical 
management decisions. ICPi-induced pneumonitis has an incidence of 2.7% for all-grade 
and 0.8% for high-grade pneumonitis in single-agent therapy, with onset typically 
occurring 2-24 weeks after treatment initiation, requiring immediate recognition and 
appropriate management to prevent life-threatening respiratory complications.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsLungPneumonitisRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for Lung Toxicity - Pneumonitis
    
    This grading system evaluates pneumonitis severity in patients receiving immune 
    checkpoint inhibitor therapy based on respiratory symptoms, functional impact, 
    oxygen requirements, and radiographic findings:
    
    Grading Criteria (CTCAE v5.0):
    - Grade 1: Asymptomatic; clinical or diagnostic observations only - Continue ICPi with monitoring
    - Grade 2: Symptomatic; limiting instrumental ADLs - Hold ICPi, start steroids
    - Grade 3: Severe symptoms; limiting self-care ADLs; oxygen indicated - Permanently discontinue ICPi
    - Grade 4: Life-threatening respiratory compromise - Immediate ICU admission
    
    Clinical Context:
    - ICPi-induced pneumonitis incidence: 2.7% all-grade, 0.8% high-grade
    - Higher incidence with combination vs single-agent therapy
    - Onset typically 2-24 weeks after treatment initiation (median 2.8 months)
    - Four main radiographic patterns: COP, NSIP, HP, AIP/ARDS
    - CT chest more sensitive than chest X-ray for detection
    
    Management Principles:
    - Grade 1: Continue ICPi, close monitoring, repeat imaging in 3-4 weeks
    - Grade 2: Hold ICPi, corticosteroids (1 mg/kg/day), pulmonology consultation
    - Grade 3-4: Permanently discontinue ICPi, high-dose steroids (2-4 mg/kg/day), hospitalization
    - Bronchoscopy to rule out infection before immunosuppression
    
    Assessment Parameters:
    - Respiratory symptoms: dyspnea, cough, chest pain severity
    - Functional impact: ability to perform daily activities
    - Oxygen requirements: room air to mechanical ventilation
    - Radiographic extent: percentage of lung involvement on CT
    - Hospitalization needs: clinical indication for inpatient monitoring
    
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
    3. Nishino M, Giobbie-Hurder A, Hatabu H, Ramaiya NH, Hodi FS. Incidence of 
    Programmed Cell Death 1 Inhibitor-Related Pneumonitis in Patients With Advanced 
    Cancer: A Systematic Review and Meta-analysis. JAMA Oncol. 2016 Dec 1;2(12):1607-1616. 
    doi: 10.1001/jamaoncol.2016.2453.
    4. Naidoo J, Wang X, Woo KM, Iyriboz T, Halpenny D, Cunningham J, et al. Pneumonitis 
    in Patients Treated With Anti-Programmed Death-1/Programmed Death Ligand 1 Therapy. 
    J Clin Oncol. 2017 Mar 10;35(7):709-717. doi: 10.1200/JCO.2016.68.2005.
    """
    
    respiratory_symptoms: Literal["asymptomatic", "mild", "moderate", "severe"] = Field(
        ...,
        description="Presence and severity of respiratory symptoms including dyspnea, cough, chest pain. Asymptomatic indicates radiographic changes only without symptoms. Mild symptoms allow normal daily activities. Moderate symptoms limit some activities. Severe symptoms significantly limit activities",
        example="moderate"
    )
    
    functional_impact: Literal["none", "limiting_instrumental_adls", "limiting_self_care_adls", "life_threatening"] = Field(
        ...,
        description="Impact on activities of daily living and functional status. None: normal activities maintained. Limiting instrumental ADLs: some limitation in complex activities (shopping, cooking, managing finances). Limiting self-care ADLs: unable to perform basic self-care activities (bathing, dressing, eating). Life-threatening: requires urgent intervention",
        example="limiting_instrumental_adls"
    )
    
    oxygen_requirement: Literal["room_air", "low_flow_oxygen", "high_flow_oxygen", "mechanical_ventilation"] = Field(
        ...,
        description="Need for supplemental oxygen or respiratory support. Room air: no oxygen needed. Low-flow oxygen: nasal cannula ≤4L/min or simple face mask. High-flow oxygen: >4L/min, non-rebreather mask, or high-flow nasal cannula. Mechanical ventilation: intubation or non-invasive positive pressure ventilation required",
        example="room_air"
    )
    
    radiographic_findings: Literal["normal", "minimal", "moderate", "extensive"] = Field(
        ...,
        description="Extent of radiographic involvement on chest imaging (CT preferred over chest X-ray). Normal: no findings. Minimal: <25% lung involvement, focal ground-glass opacities. Moderate: 25-50% lung involvement, multifocal changes. Extensive: >50% lung involvement or diffuse bilateral involvement",
        example="minimal"
    )
    
    hospitalization_indicated: Literal["yes", "no"] = Field(
        ...,
        description="Clinical indication for hospitalization based on severity, oxygen requirements, complications, or need for close monitoring. Indicates at least Grade 2 severity. Consider for respiratory distress, hypoxemia, inability to maintain oral intake, or concern for rapid progression",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "respiratory_symptoms": "moderate",
                "functional_impact": "limiting_instrumental_adls",
                "oxygen_requirement": "room_air",
                "radiographic_findings": "minimal",
                "hospitalization_indicated": "no"
            }
        }


class ImmuneRelatedAdverseEventsLungPneumonitisResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for Lung Toxicity - Pneumonitis
    
    The irAE grading system provides standardized assessment of pneumonitis severity 
    and evidence-based management recommendations for immune checkpoint inhibitor-induced 
    pulmonary toxicity:
    
    Grade 1 (Mild): Continue ICPi with close monitoring and repeat imaging in 3-4 weeks
    Grade 2 (Moderate): Hold ICPi, corticosteroids, pulmonology consultation
    Grade 3 (Severe): Permanently discontinue ICPi, high-dose steroids, hospitalization
    Grade 4 (Life-threatening): Immediate ICU admission, high-dose IV steroids, critical care consultation
    
    Clinical Implications:
    - Grade 2+ requires holding ICPi and pulmonology consultation
    - Grade 3-4 requires permanent ICPi discontinuation
    - Bronchoscopy recommended to rule out infection before immunosuppression
    - Second-line agents for steroid-refractory cases: infliximab, mycophenolate mofetil, cyclophosphamide
    - Monitor for opportunistic infections during immunosuppressive treatment
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="irAE grade for lung pneumonitis based on CTCAE v5.0 criteria (range: 1-4)",
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
        description="Clinical interpretation with detailed management recommendations including ICPi therapy decisions, corticosteroid treatment, pulmonology consultation needs, and monitoring for respiratory complications",
        example="Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain pulmonology consultation. Rule out infectious causes with bronchoscopy if indicated. Consider hospitalization for close monitoring. Repeat chest imaging in 3-5 days. Resume ICPi when grade ≤1 and steroids tapered."
    )
    
    stage: str = Field(
        ...,
        description="irAE grade classification with severity descriptor",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade severity and clinical criteria",
        example="Moderate - Symptomatic; limiting instrumental ADLs"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (prednisone 1 mg/kg/day or equivalent). Obtain pulmonology consultation. Rule out infectious causes with bronchoscopy if indicated. Consider hospitalization for close monitoring. Repeat chest imaging in 3-5 days. Resume ICPi when grade ≤1 and steroids tapered.",
                "stage": "Grade 2",
                "stage_description": "Moderate - Symptomatic; limiting instrumental ADLs"
            }
        }