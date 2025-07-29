"""
Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS) Models

Request and response models for Berlin Criteria ARDS diagnosis and severity classification.

References (Vancouver style):
1. Ranieri VM, Rubenfeld GD, Thompson BT, Ferguson ND, Caldwell E, Fan E, et al; 
   ARDS Definition Task Force. Acute respiratory distress syndrome: the Berlin Definition. 
   JAMA. 2012 Jun 20;307(23):2526-33. doi: 10.1001/jama.2012.5669.
2. Fan E, Brodie D, Slutsky AS. Acute Respiratory Distress Syndrome: Advances in 
   Diagnosis and Treatment. JAMA. 2018 Feb 20;319(7):698-710. doi: 10.1001/jama.2017.21907.
3. Matthay MA, Zemans RL, Zimmerman GA, Arabi YM, Beitler JR, Mercat A, et al. 
   Acute respiratory distress syndrome. Nat Rev Dis Primers. 2019 Mar 14;5(1):18. 
   doi: 10.1038/s41572-019-0069-0.

The Berlin Definition for ARDS (2012) established standardized diagnostic criteria that 
replaced the previous American-European Consensus Conference definition. It requires all 
four criteria to be met: acute onset (≤7 days), bilateral opacities on chest imaging, 
respiratory failure not fully explained by cardiac failure, and presence of a known 
ARDS risk factor. Severity is classified based on the PaO2/FiO2 ratio measured with 
PEEP or CPAP ≥5 cm H2O.

The Berlin Definition improved diagnostic accuracy and prognostic value compared to 
previous definitions, with mortality rates of approximately 27% for mild, 32% for 
moderate, and 45% for severe ARDS. This classification system is now the international 
standard for ARDS diagnosis and is used in clinical practice, research, and clinical trials.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BerlinCriteriaArdsRequest(BaseModel):
    """
    Request model for Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS)
    
    The Berlin Definition for ARDS requires ALL FOUR criteria to be met for diagnosis:
    
    **1. Timing Criterion:**
    - Acute onset within 1 week of a known clinical insult
    - OR new/worsening respiratory symptoms within 1 week
    
    **2. Chest Imaging Criterion:**
    - Bilateral opacities on chest X-ray or CT scan
    - Opacities must NOT be fully explained by:
      * Pleural effusions
      * Lobar or lung collapse
      * Pulmonary nodules
    
    **3. Origin of Pulmonary Edema Criterion:**
    - Respiratory failure NOT fully explained by cardiac failure or fluid overload
    - May require objective assessment (echocardiography) if no ARDS risk factors present
    - Clinical assessment may be sufficient if ARDS risk factors are present
    
    **4. Oxygenation Criterion (with PEEP ≥5 cm H2O):**
    - **Mild ARDS**: PaO2/FiO2 >200 to ≤300 mmHg
    - **Moderate ARDS**: PaO2/FiO2 >100 to ≤200 mmHg  
    - **Severe ARDS**: PaO2/FiO2 ≤100 mmHg
    
    **Common ARDS Risk Factors:**
    - **Direct Lung Injury**: Pneumonia, aspiration, inhalation injury, lung contusion, 
      near drowning, fat embolism
    - **Indirect Lung Injury**: Sepsis, severe trauma, pancreatitis, massive transfusion, 
      drug overdose, burns, transfusion-related acute lung injury (TRALI)
    
    **Clinical Assessment Guidelines:**
    - PaO2/FiO2 ratio MUST be measured with PEEP or CPAP ≥5 cm H2O
    - If altitude >1000m, use correction factor: PaO2/FiO2 × (barometric pressure/760)
    - Bilateral opacities should be consistent with pulmonary edema
    - Consider alternative diagnoses if criteria not fully met
    
    References (Vancouver style):
    1. Ranieri VM, Rubenfeld GD, Thompson BT, Ferguson ND, Caldwell E, Fan E, et al; 
    ARDS Definition Task Force. Acute respiratory distress syndrome: the Berlin Definition. 
    JAMA. 2012 Jun 20;307(23):2526-33. doi: 10.1001/jama.2012.5669.
    2. Fan E, Brodie D, Slutsky AS. Acute Respiratory Distress Syndrome: Advances in 
    Diagnosis and Treatment. JAMA. 2018 Feb 20;319(7):698-710. doi: 10.1001/jama.2017.21907.
    3. Matthay MA, Zemans RL, Zimmerman GA, Arabi YM, Beitler JR, Mercat A, et al. 
    Acute respiratory distress syndrome. Nat Rev Dis Primers. 2019 Mar 14;5(1):18. 
    doi: 10.1038/s41572-019-0069-0.
    """
    
    timing_within_one_week: Literal["yes", "no"] = Field(
        ...,
        description="Acute onset within 1 week of clinical insult or new/worsening respiratory symptoms. Required for ARDS diagnosis.",
        example="yes"
    )
    
    bilateral_opacities: Literal["yes", "no"] = Field(
        ...,
        description="Bilateral opacities on chest X-ray or CT scan not fully explained by effusions, lobar/lung collapse, or nodules. Required for ARDS diagnosis.",
        example="yes"
    )
    
    not_cardiac_failure: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory failure NOT fully explained by cardiac failure or fluid overload. May require echocardiography if no ARDS risk factors present. Required for ARDS diagnosis.",
        example="yes"
    )
    
    ards_risk_factor: Literal["yes", "no"] = Field(
        ...,
        description="Presence of known ARDS risk factor (pneumonia, sepsis, trauma, aspiration, pancreatitis, massive transfusion, etc.). Required for ARDS diagnosis.",
        example="yes"
    )
    
    pao2_fio2_ratio: float = Field(
        ...,
        ge=50,
        le=500,
        description="PaO2/FiO2 ratio in mmHg measured with PEEP or CPAP ≥5 cm H2O. Used to classify ARDS severity: Mild (>200-300), Moderate (>100-200), Severe (≤100).",
        example=150.0
    )
    
    peep_at_least_5: Literal["yes", "no"] = Field(
        ...,
        description="PEEP or CPAP ≥5 cm H2O applied when PaO2/FiO2 ratio was measured. Required for accurate severity classification.",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "timing_within_one_week": "yes",
                "bilateral_opacities": "yes", 
                "not_cardiac_failure": "yes",
                "ards_risk_factor": "yes",
                "pao2_fio2_ratio": 150.0,
                "peep_at_least_5": "yes"
            }
        }


class BerlinCriteriaArdsResponse(BaseModel):
    """
    Response model for Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS)
    
    The Berlin Definition classifies patients into four categories:
    
    **No ARDS**: Does not meet all four required criteria
    - Consider alternative diagnoses for acute respiratory failure
    - May include cardiogenic pulmonary edema, pneumonia without ARDS, atelectasis
    
    **Mild ARDS**: PaO2/FiO2 >200 to ≤300 mmHg with PEEP ≥5 cm H2O
    - Mortality rate: ~27%
    - Management: Lung-protective ventilation, conservative fluid strategy
    
    **Moderate ARDS**: PaO2/FiO2 >100 to ≤200 mmHg with PEEP ≥5 cm H2O  
    - Mortality rate: ~32%
    - Management: Enhanced lung-protective strategies, consider prone positioning
    
    **Severe ARDS**: PaO2/FiO2 ≤100 mmHg with PEEP ≥5 cm H2O
    - Mortality rate: ~45%
    - Management: Aggressive interventions, prone positioning, consider ECMO
    
    Reference: Ranieri VM, et al. JAMA. 2012;307(23):2526-33.
    """
    
    result: str = Field(
        ...,
        description="ARDS diagnosis and severity classification based on Berlin Criteria",
        example="Moderate ARDS"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on ARDS severity",
        example="Patient meets criteria for moderate ARDS. Implement lung-protective ventilation, consider higher PEEP strategies, prone positioning, and close monitoring."
    )
    
    stage: str = Field(
        ...,
        description="ARDS severity stage (No ARDS, Mild ARDS, Moderate ARDS, Severe ARDS)",
        example="Moderate ARDS"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the ARDS severity criteria",
        example="PaO2/FiO2 >100 to ≤200 mmHg with PEEP ≥5 cm H2O"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Moderate ARDS",
                "unit": "classification",
                "interpretation": "Patient meets criteria for moderate ARDS. Implement lung-protective ventilation, consider higher PEEP strategies, prone positioning, and close monitoring.",
                "stage": "Moderate ARDS",
                "stage_description": "PaO2/FiO2 >100 to ≤200 mmHg with PEEP ≥5 cm H2O"
            }
        }