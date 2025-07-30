"""
CholeS Score for Duration of Laparoscopic Cholecystectomy Models

Request and response models for CholeS Score calculation.

References (Vancouver style):
1. Vohra RS, Pasquali S, Kirkham JJ, Marriott P, Johnstone M, Spreadborough P, et al. 
   The development and validation of a scoring tool to predict the operative duration 
   of elective laparoscopic cholecystectomy. Surg Endosc. 2018 Jul;32(7):3149-3157.
2. Griffiths EA, Hodson J, Vohra RS, Marriott P, Katbeh T, Zino S, et al. Utilisation 
   of an operative difficulty grading scale for laparoscopic cholecystectomy. Surg 
   Endosc. 2019 Jan;33(1):110-121.
3. Nassar AHM, Hodson J, Ng HJ, Vohra RS, Katbeh T, Zino S, et al. Predicting the 
   difficult laparoscopic cholecystectomy: development and validation of a pre-operative 
   risk score using an objective operative difficulty grading system. Surg Endosc. 
   2020 Oct;34(10):4549-4561.

The CholeS Score for Duration of Laparoscopic Cholecystectomy is a validated prediction 
tool designed to estimate operative time for elective laparoscopic cholecystectomy 
procedures. Developed from the landmark CholeS study involving 8,820 patients across 
166 UK hospitals, this score helps optimize theatre scheduling, resource allocation, 
and surgical planning.

CholeS Score Components and Clinical Significance:

Patient Demographics:

Age (0-1.5 points):
Age represents a fundamental risk factor affecting operative complexity and duration.
- <40 years (0 points): Younger patients typically have less complex anatomy
- ≥40 years (1.5 points): Advanced age associated with increased surgical complexity

Gender (0-1 point):
Gender differences reflect anatomical and physiological variations affecting surgery.
- Female (0 points): Baseline risk category
- Male (1 point): Male patients show increased operative complexity in validation studies

Surgical Indication (0-2.5 points):
The underlying pathology significantly influences operative complexity and duration.

Pancreatitis (0 points):
- Post-inflammatory state with defined anatomy
- Often less complex dissection planes
- Lower risk for prolonged operative time

Colic/Dyskinesia/Polyp (0.5 points):
- Functional disorders or benign lesions
- Moderate complexity procedures
- Intermediate operative risk

Common Bile Duct Stone (2 points):
- Complex biliary pathology requiring careful dissection
- Increased risk of complications during surgery
- Often requires additional procedures or exploration

Acalculous/Cholecystitis (2.5 points):
- Inflammatory conditions creating difficult dissection planes
- Highest complexity category in indication scoring
- Associated with prolonged operative times and conversion risk

Physical Factors:

Body Mass Index (0-2 points):
BMI directly impacts surgical visualization, instrument manipulation, and operative difficulty.
- <25 kg/m² (0 points): Optimal surgical conditions
- 25-35 kg/m² (1 point): Moderate increase in operative complexity
- >35 kg/m² (2 points): Significant technical challenges and prolonged operative time

Anatomical and Imaging Factors:

Common Bile Duct Diameter (0-2 points):
CBD diameter reflects biliary pathology complexity and potential for complications.
- Normal (0 points): Standard anatomy without biliary obstruction
- Dilated (2 points): Suggests biliary pathology requiring careful evaluation

Gallbladder Wall Thickness (0-1.5 points):
Wall thickness indicates inflammatory changes affecting surgical dissection.
- Normal (0 points): Standard anatomy with clear dissection planes
- Thick (1.5 points): Inflammatory changes complicating surgery

Pre-operative Imaging (0-1.5 points):
CT imaging requirement suggests clinical complexity or diagnostic uncertainty.
- No CT (0 points): Straightforward clinical presentation
- CT performed (1.5 points): Complex presentation requiring additional imaging

Procedural Factors:

Planned Intra-operative Cholangiogram (0-3 points):
Cholangiography adds significant time and complexity to the procedure.
- Not planned (0 points): Standard cholecystectomy without additional procedures
- Planned (3 points): Additional time for cholangiogram setup and interpretation

Surgical History (0-2.5 points):
Previous surgical admissions indicate patient complexity and potential adhesions.
- 0 previous admissions (0 points): No previous surgical history
- 1-2 previous admissions (1 point): Limited surgical history
- >2 previous admissions (2.5 points): Extensive surgical history with adhesion risk

Patient Risk Assessment:

ASA Physical Status Classification (0-2.5 points):
ASA grade reflects overall patient fitness and perioperative risk.
- ASA 1 (0 points): Healthy patient without systemic disease
- ASA 2 (1 point): Mild systemic disease without functional limitation
- ASA ≥3 (2.5 points): Severe systemic disease with functional limitation

Clinical Applications and Implementation:

Theatre Scheduling Optimization:
The CholeS Score enables evidence-based operative scheduling by predicting cases 
likely to exceed 90 minutes duration, allowing surgical teams to:
- Optimize case sequencing and theatre utilization
- Reduce overruns and improve on-time performance
- Enhance patient and staff satisfaction through predictable scheduling

Resource Allocation:
Healthcare administrators can use score predictions to:
- Allocate appropriate theatre time and staffing resources
- Plan for complex cases requiring additional support
- Optimize overall departmental efficiency and cost-effectiveness

Risk Stratification Categories:

Low Risk (0-3.5 points): 5.1% chance of >90-minute surgery
- Clinical significance: Minimal risk of prolonged operative time
- Scheduling recommendation: Standard scheduling with 3 cases per half-day list
- Resource allocation: Standard staffing and equipment requirements
- Patient counseling: Routine operative expectations

Intermediate Risk (4-8 points): 5.1-41.8% chance of >90-minute surgery  
- Clinical significance: Moderate risk requiring individualized assessment
- Scheduling recommendation: 2-3 cases per half-day list based on total risk
- Resource allocation: Consider additional resources for complex cases
- Patient counseling: Possible extended operative time

High Risk (>8 points): >41.8% chance of >90-minute surgery
- Clinical significance: High likelihood of prolonged or complex surgery
- Scheduling recommendation: Maximum 2 cases per half-day list
- Resource allocation: Enhanced staffing and equipment preparation
- Patient counseling: Anticipate longer procedure with possible complications

Quality Improvement Applications:
- Benchmark operative efficiency across surgical teams
- Identify factors contributing to prolonged operative times
- Support surgical training and skill development programs
- Enable data-driven improvements in surgical protocols

Limitations and Considerations:
- Validated specifically for elective laparoscopic cholecystectomy
- Not applicable to emergency or acute surgical presentations
- Does not account for anesthesia time or theatre turnover
- Should complement rather than replace clinical judgment
- Requires regular validation with local surgical outcomes

Clinical Decision Support:
The CholeS Score provides objective data to support:
- Pre-operative patient counseling about expected operative duration
- Surgical team preparation and resource planning
- Administrative decision-making for theatre scheduling
- Quality improvement initiatives and outcome tracking
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CholesScoredRequest(BaseModel):
    """
    Request model for CholeS Score for Duration of Laparoscopic Cholecystectomy
    
    The CholeS Score uses 10 clinical and demographic factors to predict the likelihood 
    of prolonged operative time (>90 minutes) for elective laparoscopic cholecystectomy. 
    This evidence-based tool enables optimal theatre scheduling and resource allocation.
    
    Patient Demographics:
    
    Age Assessment:
    Age represents a fundamental risk factor affecting operative complexity due to 
    anatomical changes, comorbidities, and tissue characteristics that develop over time.
    - Younger patients (<40 years) typically have clearer anatomy and fewer adhesions
    - Older patients (≥40 years) may have more complex anatomy and comorbidities
    
    Gender Considerations:
    Gender-based anatomical differences impact surgical complexity and operative duration.
    - Female patients represent the baseline risk category
    - Male patients demonstrate increased operative complexity in validation studies
    
    Clinical Factors:
    
    Surgical Indication Assessment:
    The underlying pathological condition significantly influences operative complexity:
    
    Pancreatitis (Lowest Risk):
    - Post-inflammatory state often creates defined tissue planes
    - Generally associated with less complex dissection requirements
    - Lower likelihood of conversion to open surgery
    
    Colic/Dyskinesia/Polyp (Low-Moderate Risk):
    - Functional disorders or benign pathology
    - Intermediate complexity requiring careful evaluation
    - Moderate operative time expectations
    
    Common Bile Duct Stone (High Risk):
    - Complex biliary pathology requiring meticulous dissection
    - Higher risk of complications during Calot's triangle dissection
    - Often requires additional procedures or exploration
    
    Acalculous/Cholecystitis (Highest Risk):
    - Inflammatory conditions creating difficult, unclear dissection planes
    - Highest complexity category with increased conversion risk
    - Associated with prolonged operative times and technical challenges
    
    Physical Assessment:
    
    Body Mass Index Impact:
    BMI directly affects surgical visualization, instrument manipulation, and access:
    - Normal BMI (<25): Optimal surgical conditions with clear visualization
    - Overweight (25-35): Moderate technical challenges, slightly prolonged time
    - Obese (>35): Significant technical difficulties, substantially increased time
    
    Anatomical and Imaging Evaluation:
    
    Common Bile Duct Diameter:
    CBD assessment reflects biliary tree pathology and complexity:
    - Normal diameter: Standard anatomy without significant biliary disease
    - Dilated diameter: Suggests obstruction or pathology requiring careful evaluation
    
    Gallbladder Wall Thickness:
    Wall thickness indicates inflammatory changes affecting dissection difficulty:
    - Normal wall: Clear tissue planes facilitating standard dissection
    - Thick wall: Inflammatory changes complicating identification of anatomy
    
    Pre-operative CT Imaging:
    CT requirement suggests clinical complexity or diagnostic uncertainty:
    - No CT needed: Straightforward clinical presentation
    - CT performed: Complex presentation requiring additional imaging evaluation
    
    Procedural Planning:
    
    Intra-operative Cholangiogram:
    Planned cholangiography significantly impacts operative duration:
    - Not planned: Standard cholecystectomy without additional procedures
    - Planned: Adds substantial time for setup, contrast injection, and interpretation
    
    Surgical History:
    Previous operations affect operative complexity through adhesion formation:
    - No previous surgery: Clear peritoneal cavity without adhesions
    - Limited history (1-2 admissions): Some adhesions possible
    - Extensive history (>2 admissions): Significant adhesions likely
    
    Risk Assessment:
    
    ASA Physical Status:
    Overall patient fitness impacts operative approach and duration:
    - ASA 1: Healthy patient without limitations
    - ASA 2: Mild systemic disease without functional impairment
    - ASA ≥3: Significant systemic disease requiring modified approach
    
    Clinical Implementation:
    The CholeS Score enables evidence-based operative planning by:
    - Predicting cases likely to exceed standard operative time
    - Supporting appropriate theatre scheduling and resource allocation
    - Enhancing patient counseling with realistic time expectations
    - Improving overall surgical department efficiency and satisfaction
    
    References (Vancouver style):
    1. Vohra RS, Pasquali S, Kirkham JJ, Marriott P, Johnstone M, Spreadborough P, et al. 
    The development and validation of a scoring tool to predict the operative duration 
    of elective laparoscopic cholecystectomy. Surg Endosc. 2018 Jul;32(7):3149-3157.
    2. Griffiths EA, Hodson J, Vohra RS, Marriott P, Katbeh T, Zino S, et al. Utilisation 
    of an operative difficulty grading scale for laparoscopic cholecystectomy. Surg 
    Endosc. 2019 Jan;33(1):110-121.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Scoring: <40 years (0 pts), ≥40 years (1.5 pts)",
        example=45
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Female (0 pts), Male (1 pt)",
        example="female"
    )
    
    indication: Literal["pancreatitis", "colic_dyskinesia_polyp", "cbd_stone", "acalculous_cholecystitis"] = Field(
        ...,
        description="Surgical indication. Pancreatitis (0 pts), Colic/dyskinesia/polyp (0.5 pts), CBD stone (2 pts), Acalculous/cholecystitis (2.5 pts)",
        example="colic_dyskinesia_polyp"
    )
    
    bmi: float = Field(
        ...,
        ge=15.0,
        le=60.0,
        description="Body Mass Index in kg/m². Scoring: <25 (0 pts), 25-35 (1 pt), >35 (2 pts)",
        example=28.5
    )
    
    cbd_diameter: Literal["normal", "dilated"] = Field(
        ...,
        description="Common bile duct diameter. Normal (0 pts), Dilated (2 pts)",
        example="normal"
    )
    
    gallbladder_wall: Literal["normal", "thick"] = Field(
        ...,
        description="Gallbladder wall thickness. Normal (0 pts), Thick (1.5 pts)",
        example="normal"
    )
    
    preoperative_ct: Literal["yes", "no"] = Field(
        ...,
        description="Pre-operative CT scan performed. No (0 pts), Yes (1.5 pts)",
        example="no"
    )
    
    planned_cholangiogram: Literal["yes", "no"] = Field(
        ...,
        description="Planned intra-operative cholangiogram. No (0 pts), Yes (3 pts)",
        example="no"
    )
    
    previous_admissions: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of previous surgical admissions. 0 (0 pts), 1-2 (1 pt), >2 (2.5 pts)",
        example=1  
    )
    
    asa_grade: int = Field(
        ...,
        ge=1,
        le=5,
        description="ASA Physical Status Classification. Grade 1 (0 pts), Grade 2 (1 pt), Grade ≥3 (2.5 pts)",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "gender": "female",
                "indication": "colic_dyskinesia_polyp",
                "bmi": 28.5, 
                "cbd_diameter": "normal",
                "gallbladder_wall": "normal",
                "preoperative_ct": "no",
                "planned_cholangiogram": "no",
                "previous_admissions": 1,
                "asa_grade": 2
            }
        }


class CholesScoredResponse(BaseModel):
    """
    Response model for CholeS Score for Duration of Laparoscopic Cholecystectomy
    
    The CholeS Score response provides comprehensive operative duration prediction with 
    evidence-based scheduling recommendations for elective laparoscopic cholecystectomy. 
    The score ranges from 0.5-17.5 points and stratifies patients into risk categories 
    for prolonged operative time (>90 minutes).
    
    Risk Stratification and Clinical Management:
    
    Low Risk (0-3.5 points): 5.1% chance of >90-minute surgery
    - Clinical significance: Minimal risk of prolonged operative duration
    - Patient characteristics: Younger, healthier patients with straightforward pathology
    - Operative expectations: Standard cholecystectomy with routine complexity
    - Scheduling recommendation: 3 cases per half-day operating list
    - Resource allocation: Standard staffing and equipment requirements
    - Patient counseling: Routine operative duration and recovery expectations
    - Quality metrics: High efficiency with predictable completion times
    
    Intermediate Risk (4-8 points): 5.1-41.8% chance of >90-minute surgery
    - Clinical significance: Moderate risk requiring individualized case assessment
    - Patient characteristics: Mixed risk factors with moderate complexity
    - Operative expectations: Variable complexity requiring flexible approach
    - Scheduling recommendation: 2-3 cases per half-day list based on total risk
    - Resource allocation: Consider additional resources for complex cases
    - Patient counseling: Possible extended operative time with standard outcomes
    - Quality metrics: Moderate efficiency requiring case-by-case planning
    
    High Risk (>8 points): >41.8% chance of >90-minute surgery
    - Clinical significance: High likelihood of prolonged or complex surgery
    - Patient characteristics: Multiple risk factors indicating technical challenges
    - Operative expectations: Complex surgery with potential conversion risk
    - Scheduling recommendation: Maximum 2 cases per half-day list
    - Resource allocation: Enhanced staffing, senior surgeon involvement
    - Patient counseling: Extended operative time with increased complexity
    - Quality metrics: Lower efficiency requiring dedicated resources
    
    Surgical Planning Applications:
    
    Theatre Scheduling Optimization:
    - Enable evidence-based case sequencing and time allocation
    - Reduce theatre overruns and improve on-time performance
    - Support realistic scheduling that accounts for case complexity
    - Enhance predictability for patients, families, and healthcare teams
    
    Resource Management:
    - Guide appropriate staffing levels for different case complexities
    - Support equipment and consumable planning for complex cases
    - Enable cost-effective resource allocation across surgical programs
    - Improve overall departmental efficiency and utilization metrics
    
    Clinical Decision Support:
    - Inform pre-operative patient counseling about expected duration
    - Support surgical team preparation and approach planning
    - Guide conversion threshold discussions and contingency planning
    - Enable quality improvement initiatives and outcome benchmarking
    
    Quality Improvement Framework:
    
    Performance Metrics:
    - Benchmark operative efficiency across surgical teams and institutions
    - Identify factors contributing to prolonged operative times
    - Support targeted interventions for efficiency improvement
    - Enable data-driven surgical protocol development
    
    Training and Education:
    - Support surgical resident and fellow training by predicting case complexity
    - Guide appropriate case selection for different skill levels
    - Enable structured progression through increasing operative complexity
    - Support competency-based surgical education programs
    
    Research Applications:
    - Standardize case complexity for surgical outcome studies
    - Enable risk-adjusted comparisons across different patient populations
    - Support development of new surgical techniques and approaches
    - Facilitate multi-center studies with standardized complexity assessment
    
    Patient Communication Framework:
    
    Pre-operative Counseling:
    - Provide realistic expectations about operative duration and complexity
    - Discuss potential for extended surgery based on individual risk factors
    - Address patient and family concerns about surgical duration
    - Support informed consent with evidence-based time predictions
    
    Post-operative Management:
    - Correlate actual operative duration with predicted complexity
    - Support quality improvement through outcome tracking
    - Enable feedback to patients about surgical experience relative to expectations
    - Guide post-operative care planning based on operative complexity
    
    Administrative and Economic Considerations:
    
    Healthcare Economics:
    - Support accurate operative time estimation for cost analysis
    - Enable efficient theatre utilization and resource planning
    - Guide staffing models based on predicted case complexity
    - Support value-based care initiatives through improved efficiency
    
    Risk Management:
    - Identify high-risk cases requiring additional preparation
    - Support appropriate consent processes for complex procedures
    - Enable proactive communication with patients and families
    - Guide quality assurance and safety initiatives
    
    Limitations and Clinical Judgment:
    
    Scope of Application:
    - Validated specifically for elective laparoscopic cholecystectomy
    - Not applicable to emergency or acute surgical presentations
    - Does not predict conversion to open surgery or complications
    - Should complement rather than replace clinical assessment
    
    Integration with Practice:
    - Use as adjunct to clinical experience and surgical judgment
    - Consider individual patient factors not captured in scoring system
    - Regular validation with local surgical outcomes and practices
    - Continuous quality improvement through outcome monitoring
    
    Reference: Vohra RS, et al. Surg Endosc. 2018;32(7):3149-3157.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CholeS assessment including score, risk stratification, and operative planning guidance",
        example={
            "total_score": 4.5,
            "risk_category": "Intermediate Risk",
            "prolonged_surgery_probability": "5.1-41.8% chance of >90-minute surgery",
            "operative_planning": "Consider operative complexity in scheduling",
            "scheduling_recommendation": "2-3 cases per half-day list based on total risk profile",
            "scoring_breakdown": {
                "component_scores": {
                    "age": {
                        "value": 45,
                        "category": "Age 45 years (≥40)",
                        "points": 1.5,
                        "description": "Patient age factor"
                    },
                    "gender": {
                        "value": "Female",
                        "points": 0,
                        "description": "Gender factor (male higher risk)"
                    },
                    "indication": {
                        "value": "Colic/Dyskinesia/Polyp",
                        "points": 0.5,
                        "description": "Surgical indication complexity"
                    },
                    "bmi": {
                        "value": 28.5,
                        "unit": "kg/m²",
                        "category": "BMI 28.5 kg/m² (25-35)",
                        "points": 1,
                        "description": "Body Mass Index"
                    },
                    "cbd_diameter": {
                        "value": "Normal",
                        "points": 0,
                        "description": "Common bile duct diameter"
                    },
                    "gallbladder_wall": {
                        "value": "Normal",
                        "points": 0,
                        "description": "Gallbladder wall thickness"
                    },
                    "preoperative_ct": {
                        "value": "NO",
                        "points": 0,
                        "description": "Pre-operative CT scan performed"
                    },
                    "planned_cholangiogram": {
                        "value": "NO",
                        "points": 0,
                        "description": "Planned intra-operative cholangiogram"
                    },
                    "previous_admissions": {
                        "value": 1,
                        "category": "1 previous admissions (1-2)",
                        "points": 1,
                        "description": "Number of previous surgical admissions"
                    },
                    "asa_grade": {
                        "value": 2,
                        "category": "ASA Grade 2 (2)",
                        "points": 1,
                        "description": "ASA Physical Status Classification"
                    }
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and operative planning recommendations",
        example="CholeS Score 4.5: Intermediate risk for prolonged surgery (5.1-41.8% chance >90 minutes). Consider scheduling 2-3 cases per half-day list based on case complexity."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the operative duration risk category",
        example="Moderate likelihood of prolonged surgery"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 4.5,
                    "risk_category": "Intermediate Risk",
                    "prolonged_surgery_probability": "5.1-41.8% chance of >90-minute surgery",
                    "operative_planning": "Consider operative complexity in scheduling",
                    "scheduling_recommendation": "2-3 cases per half-day list based on total risk profile",
                    "scoring_breakdown": {
                        "component_scores": {
                            "age": {
                                "value": 45,
                                "category": "Age 45 years (≥40)",
                                "points": 1.5,
                                "description": "Patient age factor"
                            },
                            "gender": {
                                "value": "Female",
                                "points": 0,
                                "description": "Gender factor (male higher risk)"
                            },
                            "indication": {
                                "value": "Colic/Dyskinesia/Polyp",
                                "points": 0.5,
                                "description": "Surgical indication complexity"
                            },
                            "bmi": {
                                "value": 28.5,
                                "unit": "kg/m²",
                                "category": "BMI 28.5 kg/m² (25-35)",
                                "points": 1,
                                "description": "Body Mass Index"
                            }
                        }
                    }
                },
                "unit": "points",
                "interpretation": "CholeS Score 4.5: Intermediate risk for prolonged surgery (5.1-41.8% chance >90 minutes). Consider scheduling 2-3 cases per half-day list based on case complexity.",
                "stage": "Intermediate Risk",
                "stage_description": "Moderate likelihood of prolonged surgery"
            }
        }