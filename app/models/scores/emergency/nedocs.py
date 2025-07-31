"""
NEDOCS Score for Emergency Department Overcrowding Models

Request and response models for NEDOCS calculation.

References (Vancouver style):
1. Weiss SJ, Derlet R, Arndahl J, Ernst AA, Richards J, Fernández-Frankelton M, et al. 
   Estimating the degree of emergency department overcrowding in academic medical centers: 
   results of the National ED Overcrowding Study (NEDOCS). Acad Emerg Med. 2004 Jan;11(1):38-50. 
   doi: 10.1197/j.aem.2003.07.017.
2. Hwang U, McCarthy ML, Aronsky D, Asplin B, Crane PW, Craven CK, et al. Measures of 
   crowding in the emergency department: a systematic review. Acad Emerg Med. 2011 
   May;18(5):527-38. doi: 10.1111/j.1553-2712.2011.01054.x.
3. Hoot N, Aronsky D. An early warning system for overcrowding in the emergency department. 
   AMIA Annu Symp Proc. 2006;2006:339-43. PMID: 17238358.

The NEDOCS (National Emergency Department Overcrowding Scale) is an objective tool that 
uses 7 measurable parameters to quantify the degree of overcrowding in emergency departments. 
It was validated in academic medical centers and provides a standardized score from 1-200 
to help identify when patient safety may be compromised due to overcrowding.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any


class NedocsRequest(BaseModel):
    """
    Request model for NEDOCS Score for Emergency Department Overcrowding
    
    The NEDOCS score uses 7 objective parameters to assess ED overcrowding:
    
    Capacity Parameters:
    - ED beds: Total licensed number of ED beds
    - Hospital beds: Total number of hospital beds
    
    Volume Parameters:
    - Total patients: All patients in ED including doubled up and hallway beds
    - Ventilated patients: Number of patients on mechanical ventilation
    - Admitted patients: Number of patients admitted but still in ED
    
    Time Parameters:
    - Longest admit wait: Hours the longest-waiting admitted patient has been in ED
    - Longest waiting room wait: Hours the last roomed patient waited before being roomed
    
    Formula:
    NEDOCS = -20 + 85.8×(Total patients/ED beds) + 600×(Admits/Hospital beds) + 
             13.3×(Ventilated) + 0.93×(Longest admit hours) + 5.64×(Longest wait hours)
    
    Score ranges from 1-200 with 6 levels of interpretation.

    References (Vancouver style):
    1. Weiss SJ, Derlet R, Arndahl J, Ernst AA, Richards J, Fernández-Frankelton M, et al. 
    Estimating the degree of emergency department overcrowding in academic medical centers: 
    results of the National ED Overcrowding Study (NEDOCS). Acad Emerg Med. 2004 Jan;11(1):38-50. 
    doi: 10.1197/j.aem.2003.07.017.
    """
    
    ed_beds: int = Field(
        ...,
        ge=1,
        le=500,
        description="Number of ED beds (total licensed number of beds). This is the official capacity of the emergency department",
        example=30
    )
    
    hospital_beds: int = Field(
        ...,
        ge=1,
        le=5000,
        description="Number of hospital beds. This is the total inpatient bed capacity of the hospital",
        example=400
    )
    
    total_patients: int = Field(
        ...,
        ge=0,
        le=1000,
        description="Total patients in the ED. Include all patients: those in rooms, doubled up in rooms, and in hallway beds",
        example=45
    )
    
    ventilated_patients: int = Field(
        ...,
        ge=0,
        le=100,
        description="Number of patients on ventilators in the ED. These patients require intensive monitoring and resources",
        example=2
    )
    
    admitted_patients: int = Field(
        ...,
        ge=0,
        le=500,
        description="Number of admitted patients still in the ED. These are patients with admission orders waiting for inpatient beds",
        example=8
    )
    
    longest_admit_wait: float = Field(
        ...,
        ge=0,
        le=168,
        description="Waiting time of longest admitted patient in hours. Time from admission decision to current time for the patient who has been waiting longest",
        example=4.5
    )
    
    longest_waiting_room_wait: float = Field(
        ...,
        ge=0,
        le=168,
        description="Waiting time of longest waiting room patient in hours. Technically 'Last roomed patient's prior wait time' - the time the most recently roomed patient spent in the waiting room",
        example=2.0
    )
    
    @field_validator('ventilated_patients')
    def validate_ventilated_patients(cls, v, values):
        """Ensure ventilated patients don't exceed total patients"""
        if 'total_patients' in values and v > values['total_patients']:
            raise ValueError('Ventilated patients cannot exceed total patients')
        return v
    
    @field_validator('admitted_patients')
    def validate_admitted_patients(cls, v, values):
        """Ensure admitted patients don't exceed total patients"""
        if 'total_patients' in values and v > values['total_patients']:
            raise ValueError('Admitted patients cannot exceed total patients')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "ed_beds": 30,
                "hospital_beds": 400,
                "total_patients": 45,
                "ventilated_patients": 2,
                "admitted_patients": 8,
                "longest_admit_wait": 4.5,
                "longest_waiting_room_wait": 2.0
            }
        }


class NedocsResponse(BaseModel):
    """
    Response model for NEDOCS Score for Emergency Department Overcrowding
    
    The NEDOCS score ranges from 1 to 200 points and classifies ED overcrowding into:
    - Level 1 (1-20): Not busy
    - Level 2 (21-60): Busy
    - Level 3 (61-100): Extremely busy but not overcrowded
    - Level 4 (101-140): Overcrowded
    - Level 5 (141-180): Severely overcrowded
    - Level 6 (181-200): Dangerously overcrowded
    
    Higher scores indicate greater overcrowding and increased risk to patient safety.
    Scores above 100 suggest compromised patient care and excessive wait times.
    
    Reference: Weiss SJ, et al. Acad Emerg Med. 2004;11(1):38-50.
    """
    
    result: float = Field(
        ...,
        ge=1,
        le=200,
        description="NEDOCS score calculated from ED parameters (range: 1-200 points)",
        example=95.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the overcrowding level and recommended actions",
        example="The emergency department is very busy with high patient volume, but resources are still adequate to manage patient flow effectively."
    )
    
    stage: str = Field(
        ...,
        description="Overcrowding level (Level 1-6)",
        example="Level 3"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the overcrowding level",
        example="Extremely busy but not overcrowded"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 95.3,
                "unit": "points",
                "interpretation": "The emergency department is very busy with high patient volume, but resources are still adequate to manage patient flow effectively.",
                "stage": "Level 3",
                "stage_description": "Extremely busy but not overcrowded"
            }
        }