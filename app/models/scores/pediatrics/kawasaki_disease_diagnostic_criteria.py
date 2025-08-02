"""
Kawasaki Disease Diagnostic Criteria Models

Request and response models for Kawasaki Disease diagnostic criteria calculation.

References (Vancouver style):
1. McCrindle BW, Rowley AH, Newburger JW, Burns JC, Bolger AF, Gewitz M, et al. 
   Diagnosis, Treatment, and Long-Term Management of Kawasaki Disease: A Scientific 
   Statement for Health Professionals From the American Heart Association. 
   Circulation. 2017;135(17):e927-e999.
2. Newburger JW, Takahashi M, Gerber MA, Gewitz MH, Tani LY, Burns JC, et al. 
   Diagnosis, treatment, and long-term management of Kawasaki disease: a statement 
   for health professionals from the Committee on Rheumatic Fever, Endocarditis and 
   Kawasaki Disease, Council on Cardiovascular Disease in the Young, American Heart 
   Association. Circulation. 2004;110(17):2747-71.
3. Ayusawa M, Sonobe T, Uemura S, Ogawa S, Nakamura Y, Kiyosawa N, et al. 
   Revision of diagnostic guidelines for Kawasaki disease (the 5th revised edition). 
   Pediatr Int. 2005;47(2):232-4.
4. Yellen ES, Gauvreau K, Takahashi M, Burns JC, Shulman S, Baker AL, et al. 
   Performance of 2004 American Heart Association recommendations for treatment of 
   Kawasaki disease. Pediatrics. 2010;125(2):e234-41.

Kawasaki Disease is a systemic vasculitis of childhood that affects medium-sized arteries, 
particularly the coronary arteries. It is the leading cause of acquired heart disease in 
children in developed countries. Early diagnosis and treatment are crucial to prevent 
coronary artery abnormalities, which can lead to myocardial infarction, sudden death, 
or ischemic heart disease later in life.

The diagnostic criteria are based on the presence of fever lasting ≥4 days plus a specific 
number of principal clinical features. Classic Kawasaki disease requires ≥4 of 5 principal 
features, while incomplete Kawasaki disease is diagnosed when patients have fever ≥5 days 
with 2-3 principal features and supportive laboratory findings or coronary abnormalities.

Principal clinical features include:
1. Bilateral conjunctival injection without exudate
2. Oral changes (cracked/erythematous lips, strawberry tongue, erythema of oral mucosa)
3. Cervical lymphadenopathy (≥1.5 cm diameter, usually unilateral)
4. Extremity changes (erythema of palms/soles, induration, or desquamation)
5. Polymorphous rash (not vesicular or bullous)

Early treatment with intravenous immunoglobulin (IVIG) and aspirin within 10 days of 
fever onset significantly reduces the risk of coronary artery abnormalities from ~25% 
to <5%. Long-term management includes echocardiographic monitoring and cardiovascular 
risk stratification based on coronary artery involvement.
"""

from pydantic import BaseModel, Field
from typing import Literal


class KawasakiDiseaseRequest(BaseModel):
    """
    Request model for Kawasaki Disease Diagnostic Criteria
    
    Kawasaki Disease diagnostic criteria are based on fever duration and the presence 
    of principal clinical features:
    
    Fever Duration:
    - Minimum 4 days required for classic diagnosis consideration
    - Minimum 5 days required for incomplete diagnosis consideration
    - In rare cases with coronary abnormalities, shorter fever duration may warrant treatment
    
    Principal Clinical Features (5 total):
    1. Bilateral conjunctival injection: Non-purulent conjunctival injection without exudate
    2. Oral changes: Including cracked and erythematous lips, strawberry tongue, 
       or diffuse erythema of oral and pharyngeal mucosa
    3. Cervical lymphadenopathy: Usually unilateral, ≥1.5 cm in diameter
    4. Extremity changes: Erythema of palms and soles, induration of hands and feet, 
       or desquamation of fingertips (usually in recovery phase)
    5. Polymorphous rash: Maculopapular, diffuse erythroderma, or erythema multiforme-like 
       (not vesicular, petechial, or bullous)
    
    Diagnostic Categories:
    - Classic Kawasaki Disease: Fever ≥4 days + ≥4 principal features
    - Incomplete Kawasaki Disease: Fever ≥5 days + 2-3 principal features + supportive 
      laboratory findings or coronary abnormalities
    
    Clinical Considerations:
    - Principal features may not appear simultaneously and can resolve before diagnosis
    - Incomplete presentation is more common in infants <6 months and children >8 years
    - Infants ≤6 months are at highest risk for coronary complications
    - Early treatment (within 10 days of fever onset) prevents coronary artery abnormalities
    
    References (Vancouver style):
    1. McCrindle BW, Rowley AH, Newburger JW, Burns JC, Bolger AF, Gewitz M, et al. 
       Diagnosis, Treatment, and Long-Term Management of Kawasaki Disease: A Scientific 
       Statement for Health Professionals From the American Heart Association. 
       Circulation. 2017;135(17):e927-e999.
    2. Newburger JW, Takahashi M, Gerber MA, Gewitz MH, Tani LY, Burns JC, et al. 
       Diagnosis, treatment, and long-term management of Kawasaki disease: a statement 
       for health professionals from the Committee on Rheumatic Fever, Endocarditis and 
       Kawasaki Disease, Council on Cardiovascular Disease in the Young, American Heart 
       Association. Circulation. 2004;110(17):2747-71.
    3. Ayusawa M, Sonobe T, Uemura S, Ogawa S, Nakamura Y, Kiyosawa N, et al. 
       Revision of diagnostic guidelines for Kawasaki disease (the 5th revised edition). 
       Pediatr Int. 2005;47(2):232-4.
    4. Yellen ES, Gauvreau K, Takahashi M, Burns JC, Shulman S, Baker AL, et al. 
       Performance of 2004 American Heart Association recommendations for treatment of 
       Kawasaki disease. Pediatrics. 2010;125(2):e234-41.
    """
    
    fever_duration: int = Field(
        ...,
        description="Duration of fever in days. Minimum 4 days required for classic diagnosis consideration, "
                   "minimum 5 days for incomplete diagnosis. Early diagnosis and treatment are crucial "
                   "to prevent coronary artery complications.",
        ge=1,
        le=30,
        example=6
    )
    
    bilateral_conjunctival_injection: Literal["yes", "no"] = Field(
        ...,
        description="Bilateral conjunctival injection without exudate (no purulent discharge). "
                   "This is typically non-purulent redness of both eyes affecting the bulbar conjunctiva "
                   "more than the palpebral conjunctiva. Principal clinical feature.",
        example="yes"
    )
    
    oral_changes: Literal["yes", "no"] = Field(
        ...,
        description="Oral changes including cracked and erythematous lips, strawberry tongue "
                   "(prominent papillae), or diffuse erythema of oral and pharyngeal mucosa. "
                   "Principal clinical feature.",
        example="yes"
    )
    
    cervical_lymphadenopathy: Literal["yes", "no"] = Field(
        ...,
        description="Cervical lymphadenopathy ≥1.5 cm in diameter, usually unilateral. "
                   "This is the least common of the principal clinical features, present in "
                   "approximately 50-75% of patients. Principal clinical feature.",
        example="no"
    )
    
    extremity_changes: Literal["yes", "no"] = Field(
        ...,
        description="Extremity changes including erythema of palms and soles, induration "
                   "(swelling) of hands and feet, or desquamation of fingertips. Desquamation "
                   "typically occurs in the recovery phase (2-3 weeks after fever onset). "
                   "Principal clinical feature.",
        example="yes"
    )
    
    polymorphous_rash: Literal["yes", "no"] = Field(
        ...,
        description="Polymorphous rash that is maculopapular, diffuse erythroderma, or "
                   "erythema multiforme-like. The rash is NOT vesicular, petechial, or bullous. "
                   "It typically appears within 5 days of fever onset and may be more prominent "
                   "in the groin area. Principal clinical feature.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "fever_duration": 6,
                "bilateral_conjunctival_injection": "yes",
                "oral_changes": "yes", 
                "cervical_lymphadenopathy": "no",
                "extremity_changes": "yes",
                "polymorphous_rash": "yes"
            }
        }


class KawasakiDiseaseResponse(BaseModel):
    """
    Response model for Kawasaki Disease Diagnostic Criteria
    
    Provides diagnostic assessment based on fever duration and principal clinical features.
    The response includes diagnostic category, clinical recommendations, and treatment guidance.
    
    Diagnostic Categories:
    - Classic Kawasaki Disease: Meets full criteria for diagnosis and treatment
    - Possible Incomplete Kawasaki Disease: Requires additional evaluation and consideration of treatment
    - Kawasaki Disease Unlikely/Possible: Continue monitoring, consider alternative diagnoses
    - Insufficient Fever Duration: Too early for diagnosis but continue monitoring
    
    Treatment Considerations:
    - IVIG (2 g/kg) plus aspirin (80-100 mg/kg/day) is first-line treatment
    - Treatment ideally within 10 days of fever onset to prevent coronary complications
    - Echocardiography recommended at diagnosis, 2 weeks, and 6-8 weeks after onset
    - Long-term cardiology follow-up based on coronary artery involvement
    
    Reference: McCrindle BW, et al. Circulation. 2017;135(17):e927-e999.
    """
    
    result: str = Field(
        ...,
        description="Number of principal clinical features present out of 5 total features",
        example="4/5 principal features"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic assessment",
        example="features"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including diagnostic category, treatment recommendations, "
                   "and monitoring guidance based on the diagnostic criteria",
        example="Classic Kawasaki Disease diagnosed. Patient meets criteria with fever for 6 days and 4/5 principal clinical features. Immediate treatment with IVIG and aspirin is indicated. Echocardiography should be performed to assess coronary arteries. Early treatment (within 10 days of fever onset) significantly reduces risk of coronary artery abnormalities. Close monitoring and cardiology consultation are recommended."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (Classic Kawasaki Disease, Possible Incomplete Kawasaki Disease, "
                   "Kawasaki Disease Unlikely, Kawasaki Disease Possible, Insufficient Fever Duration)",
        example="Classic Kawasaki Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category",
        example="Meets criteria for classic diagnosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "4/5 principal features",
                "unit": "features",
                "interpretation": "Classic Kawasaki Disease diagnosed. Patient meets criteria with fever for 6 days and 4/5 principal clinical features. Immediate treatment with IVIG and aspirin is indicated. Echocardiography should be performed to assess coronary arteries. Early treatment (within 10 days of fever onset) significantly reduces risk of coronary artery abnormalities. Close monitoring and cardiology consultation are recommended.",
                "stage": "Classic Kawasaki Disease",
                "stage_description": "Meets criteria for classic diagnosis"
            }
        }