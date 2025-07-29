"""
ASCOD Algorithm for Ischemic Stroke Models

Request and response models for ASCOD Algorithm calculation.

References (Vancouver style):
1. Amarenco P, Bogousslavsky J, Caplan LR, Donnan GA, Wolf ME, Hennerici MG. 
   The ASCOD phenotyping of ischemic stroke (Updated ASCO phenotyping). 
   Cerebrovasc Dis. 2013;36(1):1-5. doi: 10.1159/000352050.
2. Sirimarco G, Lavallée PC, Labreuche J, Meseguer E, Cabrejo L, Guidoux C, et al. 
   Overlap of diseases underlying ischemic stroke: the ASCOD phenotyping. 
   Stroke. 2013 Dec;44(12):3427-33. doi: 10.1161/STROKEAHA.113.001363.
3. Radu RA, Terecoasă EO, Băjenaru OA, Tiu C. Etiologic classification of ischemic stroke: 
   Where do we stand? Clin Neurol Neurosurg. 2017 Aug;159:93-106. doi: 10.1016/j.clineuro.2017.05.019.

The ASCOD Algorithm is a comprehensive stroke classification system that evaluates five main 
etiologic categories to assign phenotypes in patients with ischemic stroke of uncertain causes. 
Unlike traditional classification systems, ASCOD allows for multiple overlapping mechanisms 
and provides a nuanced assessment of stroke etiology to guide secondary prevention strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AscodAlgorithmRequest(BaseModel):
    """
    Request model for ASCOD Algorithm for Ischemic Stroke
    
    The ASCOD Algorithm evaluates five main etiologic categories, each with specific causality grades:
    
    Categories:
    - A: Atherothrombosis (large artery atherosclerosis)
    - S: Small-vessel disease (lacunar stroke mechanisms)  
    - C: Cardiac pathology (cardioembolic sources)
    - O: Other causes (vasculitis, coagulopathy, drug-related, etc.)
    - D: Dissection (arterial dissection)
    
    Causality Grades (for each category):
    - 0: No disease detected in this category
    - 1: Potentially causal - direct relationship to stroke likely
    - 2: Causal link uncertain - mechanism present but relationship unclear
    - 3: Causal link unlikely but disease present - condition exists but not stroke-causative
    - 9: Incomplete workup - further evaluation needed for this category
    
    Clinical Assessment Guidelines:
    
    Atherothrombosis (A):
    - Grade 1: ≥50% stenosis or occlusion of relevant artery with clinical/imaging correlation
    - Grade 2: <50% stenosis in relevant artery or atherosclerosis without clear correlation
    - Grade 3: Atherosclerosis present but in non-relevant territory
    - Grade 0: No atherosclerosis detected
    - Grade 9: Incomplete vascular imaging
    
    Small-vessel disease (S):
    - Grade 1: Lacunar syndrome with compatible imaging (small subcortical infarct <15mm)
    - Grade 2: Lacunar syndrome without compatible imaging or imaging without syndrome
    - Grade 3: Leukoaraiosis or old lacunes without acute correlation
    - Grade 0: No small vessel disease
    - Grade 9: Incomplete assessment (no brain imaging or clinical evaluation)
    
    Cardiac pathology (C):
    - Grade 1: High-risk cardioembolic source (e.g., atrial fibrillation, mechanical valve)
    - Grade 2: Medium-risk source (e.g., patent foramen ovale, atrial septal aneurysm)
    - Grade 3: Low-risk cardiac abnormality (e.g., mitral valve prolapse)
    - Grade 0: No cardiac pathology detected
    - Grade 9: Incomplete cardiac evaluation
    
    Other causes (O):
    - Grade 1: Definite other cause (e.g., confirmed vasculitis, hypercoagulable state)
    - Grade 2: Possible other cause requiring further evaluation
    - Grade 3: Condition present but unlikely causative
    - Grade 0: No other causes identified
    - Grade 9: Incomplete evaluation for other causes
    
    Dissection (D):
    - Grade 1: Definite arterial dissection with stroke correlation
    - Grade 2: Possible dissection requiring further imaging
    - Grade 3: Old or non-relevant dissection
    - Grade 0: No dissection detected
    - Grade 9: Incomplete vascular imaging for dissection assessment

    References (Vancouver style):
    1. Amarenco P, Bogousslavsky J, Caplan LR, Donnan GA, Wolf ME, Hennerici MG. 
       The ASCOD phenotyping of ischemic stroke (Updated ASCO phenotyping). 
       Cerebrovasc Dis. 2013;36(1):1-5. doi: 10.1159/000352050.
    2. Sirimarco G, Lavallée PC, Labreuche J, Meseguer E, Cabrejo L, Guidoux C, et al. 
       Overlap of diseases underlying ischemic stroke: the ASCOD phenotyping. 
       Stroke. 2013 Dec;44(12):3427-33. doi: 10.1161/STROKEAHA.113.001363.
    3. Radu RA, Terecoasă EO, Băjenaru OA, Tiu C. Etiologic classification of ischemic stroke: 
       Where do we stand? Clin Neurol Neurosurg. 2017 Aug;159:93-106. doi: 10.1016/j.clineuro.2017.05.019.
    """
    
    atherosclerosis: Literal["grade_9", "grade_1", "grade_2", "grade_3", "grade_0"] = Field(
        ...,
        description="Atherosclerosis grade. Grade 1: Ipsilateral stenosis 50-99% supplying area of ischemia. Grade 2: Ipsilateral stenosis 30-49%. Grade 3: Plaque without stenosis or <30% in any territory. Grade 0: No atherosclerotic disease. Grade 9: Incomplete workup",
        example="grade_1"
    )
    
    small_vessel_disease: Literal["grade_9", "grade_1", "grade_2", "grade_3", "grade_0"] = Field(
        ...,
        description="Small vessel disease grade. Grade 1: Lacunar syndrome with relevant subcortical infarct <15mm. Grade 2: Incomplete lacunar syndrome or infarct 15-20mm. Grade 3: WMH/microbleeds without qualifying syndrome. Grade 0: No SVD. Grade 9: Incomplete workup",
        example="grade_0"
    )
    
    cardiac_pathology: Literal["grade_9", "grade_1", "grade_2", "grade_3", "grade_0"] = Field(
        ...,
        description="Cardiac pathology grade. Grade 1: High-risk sources (AF, mitral stenosis, recent MI, endocarditis). Grade 2: Low/uncertain risk (PFO with ASA). Grade 3: Minor-risk sources. Grade 0: No cardiac pathology. Grade 9: Incomplete workup",
        example="grade_2"
    )
    
    other_causes: Literal["grade_9", "grade_1", "grade_2", "grade_3", "grade_0"] = Field(
        ...,
        description="Other causes grade (vasculitis, hematologic disorders, genetic conditions). Grade 1: Disease directly causing stroke. Grade 2: Disease present, causal link uncertain. Grade 3: Disease present, unlikely related. Grade 0: No other causes. Grade 9: Incomplete workup",
        example="grade_0"
    )
    
    dissection: Literal["grade_9", "grade_1", "grade_2", "grade_3", "grade_0"] = Field(
        ...,
        description="Dissection grade. Grade 1: Dissection demonstrated in relevant artery. Grade 2: Imaging suggestive but not diagnostic. Grade 3: Dissection in non-relevant artery. Grade 0: No dissection. Grade 9: Incomplete workup",
        example="grade_0"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "atherosclerosis": "grade_1",
                "small_vessel_disease": "grade_0",
                "cardiac_pathology": "grade_2",
                "other_causes": "grade_0",
                "dissection": "grade_0"
            }
        }


class AscodAlgorithmResponse(BaseModel):
    """
    Response model for ASCOD Algorithm for Ischemic Stroke
    
    The ASCOD phenotype is expressed as a 5-digit code (A-S-C-O-D) where each digit 
    represents the causality grade for the corresponding category. This allows for 
    comprehensive stroke classification that captures overlapping mechanisms and 
    guides targeted secondary prevention strategies.
    
    Example phenotypes:
    - "1-0-0-0-0": Potentially causal atherothrombosis only
    - "1-1-2-0-0": Potentially causal atherothrombosis and small vessel disease, uncertain cardiac pathology
    - "0-0-0-0-0": No identifiable mechanisms (cryptogenic stroke)
    - "9-9-9-9-9": Completely incomplete workup
    
    Reference: Amarenco P, et al. Cerebrovasc Dis. 2013;36(1):1-5.
    """
    
    result: str = Field(
        ...,
        description="ASCOD phenotype classification as 5-digit code (A-S-C-O-D format)",
        example="A1-S0-C2-O0-D0"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="phenotype"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the ASCOD phenotype",
        example="Potentially causal mechanism(s) identified: Atherothrombosis. Consider targeted secondary prevention specific to this mechanism. Consider: antiplatelet therapy and statin."
    )
    
    stage: str = Field(
        ...,
        description="Primary classification category based on highest causality grade",
        example="Potentially Causal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification stage",
        example="At least one potentially causal mechanism identified"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "A1-S0-C2-O0-D0",
                "unit": "phenotype",
                "interpretation": "Potentially causal mechanism(s) identified: Atherothrombosis. Consider targeted secondary prevention specific to this mechanism. Consider: antiplatelet therapy and statin.",
                "stage": "Potentially Causal",
                "stage_description": "At least one potentially causal mechanism identified"
            }
        }