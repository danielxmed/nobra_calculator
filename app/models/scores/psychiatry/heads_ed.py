"""
HEADS-ED Models

Request and response models for HEADS-ED (Home, Education, Activities/peers, 
Drugs/alcohol, Suicidality, Emotions/behavior, Discharge resources) calculation.

References (Vancouver style):
1. Cappelli M, Gray C, Zemek R, Cloutier P, Kennedy A, Glennie E, et al. The HEADS-ED: 
   a rapid mental health screening tool for pediatric patients in the emergency 
   department. Pediatrics. 2012 Aug;130(2):e321-7. doi: 10.1542/peds.2011-3798.
2. Cappelli M, Zemek R, Polihronis C, Thibedeau NR, Kennedy A, Gray C, et al. The 
   HEADS-ED: Evaluating the Clinical Use of a Brief, Action-Oriented, Pediatric Mental 
   Health Screening Tool. Pediatr Emerg Care. 2017 May;33(5):316-321. doi: 
   10.1097/PEC.0000000000000803.
3. Newton AS, Soleimani A, Kirkland SW, Gokiert RJ. A Systematic Review of Instruments 
   to Identify Mental Health and Substance Use Problems Among Children in the Emergency 
   Department. Acad Emerg Med. 2017 May;24(5):552-568. doi: 10.1111/acem.13162.

The HEADS-ED is a rapid mental health screening tool designed for pediatric patients 
presenting to the emergency department. It evaluates 7 domains using a 0-2 scoring 
system for each, with higher scores indicating greater mental health needs. A total 
score ≥8 or suicidality score of 2 triggers recommendation for psychiatric consultation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class HeadsEdRequest(BaseModel):
    """
    Request model for HEADS-ED pediatric mental health screening tool
    
    The HEADS-ED evaluates 7 domains of pediatric mental health:
    
    Each domain is scored 0-2:
    - 0: No action needed - indicates no significant concerns in this domain
    - 1: Needs non-urgent action and community resource education
    - 2: Immediate action and referral required
    
    Clinical decision rules:
    - Total score ≥8: Psychiatric consultation recommended
    - Suicidality = 2: Immediate psychiatric consultation required regardless of total
    - Higher scores correlate with increased likelihood of admission
    
    Validated for pediatric patients (ages 0-17) in emergency department settings.
    
    References (Vancouver style):
    1. Cappelli M, Gray C, Zemek R, Cloutier P, Kennedy A, Glennie E, et al. The HEADS-ED: 
       a rapid mental health screening tool for pediatric patients in the emergency 
       department. Pediatrics. 2012 Aug;130(2):e321-7. doi: 10.1542/peds.2011-3798.
    2. Cappelli M, Zemek R, Polihronis C, Thibedeau NR, Kennedy A, Gray C, et al. The 
       HEADS-ED: Evaluating the Clinical Use of a Brief, Action-Oriented, Pediatric Mental 
       Health Screening Tool. Pediatr Emerg Care. 2017 May;33(5):316-321. doi: 
       10.1097/PEC.0000000000000803.
    """
    
    home: int = Field(
        ...,
        ge=0,
        le=2,
        description="Home environment assessment. 0 = Supportive family environment (no concerns), "
                    "1 = Family conflicts (moderate concerns requiring resources), "
                    "2 = Chaotic/dysfunctional home (immediate intervention needed)",
        example=1
    )
    
    education: int = Field(
        ...,
        ge=0,
        le=2,
        description="Education/employment status. 0 = On track (attending regularly, passing), "
                    "1 = Grades dropping or absenteeism (needs support), "
                    "2 = Failing/not attending (immediate educational intervention needed)",
        example=1
    )
    
    activities: int = Field(
        ...,
        ge=0,
        le=2,
        description="Activities and peer relationships. 0 = No change in social interactions, "
                    "1 = Reduction in activities/increased peer conflicts, "
                    "2 = Increasingly withdrawn/significant peer conflicts",
        example=0
    )
    
    drugs: int = Field(
        ...,
        ge=0,
        le=2,
        description="Drugs and alcohol use. 0 = None or infrequent use (no concern), "
                    "1 = Occasional use (requires education/monitoring), "
                    "2 = Frequent/daily use (immediate intervention needed)",
        example=0
    )
    
    suicidality: int = Field(
        ...,
        ge=0,
        le=2,
        description="Suicidality assessment. 0 = No suicidal thoughts, "
                    "1 = Suicidal ideation (thoughts without plan), "
                    "2 = Suicide plan or gesture (immediate psychiatric consultation required)",
        example=0
    )
    
    emotions: int = Field(
        ...,
        ge=0,
        le=2,
        description="Emotions and behaviors. 0 = Mildly anxious/sad/acting out (manageable), "
                    "1 = Moderately anxious/sad/acting out (needs support), "
                    "2 = Significantly distressed/unable to function (crisis intervention needed)",
        example=1
    )
    
    discharge: int = Field(
        ...,
        ge=0,
        le=2,
        description="Discharge resources availability. 0 = Ongoing/well-connected support, "
                    "1 = Some support but not meeting needs (requires enhancement), "
                    "2 = No resources/waitlisted/noncompliant (immediate resource mobilization needed)",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "home": 1,
                "education": 1,
                "activities": 0,
                "drugs": 0,
                "suicidality": 0,
                "emotions": 1,
                "discharge": 1
            }
        }


class HeadsEdResponse(BaseModel):
    """
    Response model for HEADS-ED pediatric mental health screening tool
    
    The HEADS-ED total score ranges from 0-14 points:
    - 0-7: Low risk - Community resources and routine follow-up
    - ≥8: High risk - Psychiatric consultation recommended
    - Any suicidality score of 2: Immediate psychiatric consultation required
    
    Clinical validation shows:
    - Sensitivity 82% and specificity 87% for predicting admission
    - Sensitivity 92.1% and specificity 72.3% for predicting consultation
    - Mean scores: Admitted (7.21) vs Discharged (5.28)
    
    Reference: Cappelli M, et al. Pediatrics. 2012;130(2):e321-7.
    """
    
    result: int = Field(
        ...,
        description="HEADS-ED total score (0-14 points). Sum of all 7 domain scores",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on total score and suicidality",
        example="Consider community resources and routine follow-up. No immediate psychiatric consultation needed unless other concerning factors present. Provide education about available mental health resources and ensure appropriate outpatient follow-up is arranged."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, or Immediate Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low mental health needs"
    )
    
    requires_consultation: bool = Field(
        ...,
        description="Whether psychiatric consultation is recommended based on scoring criteria",
        example=False
    )
    
    suicidality_score: int = Field(
        ...,
        description="Individual suicidality domain score (0-2) for clinical awareness",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Consider community resources and routine follow-up. No immediate psychiatric consultation needed unless other concerning factors present. Provide education about available mental health resources and ensure appropriate outpatient follow-up is arranged.",
                "stage": "Low Risk",
                "stage_description": "Low mental health needs",
                "requires_consultation": False,
                "suicidality_score": 0
            }
        }