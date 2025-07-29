"""
Benzodiazepine Conversion Calculator Models

Request and response models for Benzodiazepine Conversion Calculator.

References (Vancouver style):
1. Ashton H. Benzodiazepines: how they work and how to withdraw. The Ashton Manual. 2002. 
   Available at: https://www.benzo.org.uk/manual/
2. Lader M, Tylee A, Donoghue J. Withdrawing benzodiazepines in primary care. 
   CNS Drugs. 2009;23(1):19-34.
3. Parr JM, Kavanagh DJ, Cahill L, et al. Effectiveness of current treatment approaches 
   for benzodiazepine discontinuation: a meta-analysis. Addiction. 2009 Jan;104(1):13-24.

The Benzodiazepine Conversion Calculator provides safe equivalents between different 
benzodiazepines for medication interchanging. It is intended for patients already on 
benzodiazepine therapy, not for calculating initial doses in benzodiazepine-naive patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BenzodiazepineConversionRequest(BaseModel):
    """
    Request model for Benzodiazepine Conversion Calculator
    
    This calculator provides approximate dose equivalents when switching between different 
    benzodiazepine medications. It is designed for safe medication interchanging in patients 
    already established on benzodiazepine therapy.
    
    **Supported Benzodiazepines:**
    
    **Short Acting (6-12 hours):**
    - Alprazolam (Xanax) - Half-life: 11-13 hours
    - Oxazepam (Serax) - Half-life: 4-15 hours  
    - Temazepam (Restoril) - Half-life: 3-18 hours
    
    **Intermediate Acting (12-24 hours):**
    - Lorazepam (Ativan) - Half-life: 10-20 hours
    
    **Long Acting (>24 hours):**
    - Chlordiazepoxide (Librium) - Half-life: 36-200 hours
    - Clonazepam (Klonopin) - Half-life: 18-50 hours
    - Diazepam (Valium) - Half-life: 20-100 hours
    
    **Very Short Acting (<6 hours):**
    - Midazolam (Versed) - Half-life: 1-4 hours
    
    **Clinical Guidelines:**
    - Use for patients already on benzodiazepine therapy
    - NOT for benzodiazepine-naive patients
    - Start with lower end of calculated dose range
    - Monitor for oversedation and withdrawal symptoms
    - Consider half-life differences in timing conversions
    
    **Important Considerations:**
    - Conversions are approximate and may require clinical adjustment
    - Individual factors (age, liver function, concurrent medications) affect dosing
    - Abrupt discontinuation should be avoided due to withdrawal risk
    - Short-acting benzodiazepines are generally more potent than long-acting ones
    
    **Safety Warnings:**
    - Does not account for individual patient variability
    - Risk of oversedation if doses are not carefully monitored
    - Risk of withdrawal symptoms including seizures if discontinued abruptly
    - Requires clinical supervision and dose adjustment based on response
    
    References (Vancouver style):
    1. Ashton H. Benzodiazepines: how they work and how to withdraw. The Ashton Manual. 2002. 
    Available at: https://www.benzo.org.uk/manual/
    2. Lader M, Tylee A, Donoghue J. Withdrawing benzodiazepines in primary care. 
    CNS Drugs. 2009;23(1):19-34.
    3. Parr JM, Kavanagh DJ, Cahill L, et al. Effectiveness of current treatment approaches 
    for benzodiazepine discontinuation: a meta-analysis. Addiction. 2009 Jan;104(1):13-24.
    """
    
    converting_from: Literal["alprazolam", "chlordiazepoxide", "clonazepam", "diazepam", "lorazepam", "midazolam", "oxazepam", "temazepam"] = Field(
        ...,
        description="Current benzodiazepine medication being converted from. Options: alprazolam (Xanax), chlordiazepoxide (Librium), clonazepam (Klonopin), diazepam (Valium), lorazepam (Ativan), midazolam (Versed), oxazepam (Serax), temazepam (Restoril)",
        example="lorazepam"
    )
    
    total_daily_dose: float = Field(
        ...,
        description="Total daily dosage of current benzodiazepine in milligrams. Must be greater than 0 and should not exceed 100mg for safety",
        ge=0.1,
        le=100.0,
        example=2.0
    )
    
    converting_to: Literal["alprazolam", "chlordiazepoxide", "clonazepam", "diazepam", "lorazepam", "midazolam", "oxazepam", "temazepam"] = Field(
        ...,
        description="Target benzodiazepine medication being converted to. Options: alprazolam (Xanax), chlordiazepoxide (Librium), clonazepam (Klonopin), diazepam (Valium), lorazepam (Ativan), midazolam (Versed), oxazepam (Serax), temazepam (Restoril)",
        example="diazepam"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Convert Lorazepam to Diazepam",
                    "value": {
                        "converting_from": "lorazepam",
                        "total_daily_dose": 2.0,
                        "converting_to": "diazepam"
                    }
                },
                {
                    "title": "Convert Alprazolam to Clonazepam",
                    "value": {
                        "converting_from": "alprazolam",
                        "total_daily_dose": 1.0,
                        "converting_to": "clonazepam"
                    }
                },
                {
                    "title": "Convert Diazepam to Lorazepam",
                    "value": {
                        "converting_from": "diazepam",
                        "total_daily_dose": 10.0,
                        "converting_to": "lorazepam"
                    }
                }
            ]
        }


class BenzodiazepineConversionResponse(BaseModel):
    """
    Response model for Benzodiazepine Conversion Calculator
    
    Returns the calculated equivalent dose with comprehensive clinical guidance including:
    - Equivalent daily dose of target benzodiazepine
    - Conversion ratio between medications
    - Half-life and duration information for both medications
    - Safety considerations and monitoring recommendations
    - Clinical warnings about oversedation and withdrawal risks
    
    The calculator provides approximate equivalents that serve as starting points for 
    clinical decision-making. Individual patient factors may require dose adjustments, 
    and close monitoring is essential during benzodiazepine conversions.
    
    **Clinical Use:**
    - Start with calculated dose or lower to minimize oversedation risk
    - Monitor for signs of oversedation (sedation, confusion, ataxia)
    - Watch for withdrawal symptoms (anxiety, insomnia, tremor, seizures)
    - Consider half-life differences when timing dose administration
    - Adjust based on individual patient response and clinical factors
    
    **Safety Reminders:**
    - Intended for patients already on benzodiazepine therapy
    - Not for benzodiazepine-naive patients
    - Requires clinical supervision and individualization
    - Abrupt discontinuation may cause life-threatening withdrawal
    
    Reference: Conversion factors are based on established equivalency tables and 
    clinical literature, but individual patient response may vary significantly.
    """
    
    result: float = Field(
        ...,
        description="Equivalent daily dose of target benzodiazepine in milligrams",
        example=10.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the equivalent dose",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including conversion details, medication half-lives, safety considerations, and monitoring recommendations",
        example="Benzodiazepine conversion: 2.0 mg lorazepam (Ativan) daily is approximately equivalent to 10.0 mg diazepam (Valium) daily (conversion ratio: 1:5.00). Original medication: intermediate acting (12-24 hours) with half-life 10-20 hours. Target medication: long acting (>24 hours) with half-life 20-100 hours. IMPORTANT CLINICAL CONSIDERATIONS: This conversion is intended for interchanging benzodiazepines in patients already on benzodiazepine therapy, NOT for calculating initial doses in benzodiazepine-naive patients. Use the lower end of the dose range initially to minimize oversedation risk. Monitor closely for signs of oversedation (sedation, confusion, ataxia) or withdrawal symptoms (anxiety, insomnia, tremor, seizures). Consider half-life differences when timing the conversion - longer-acting medications may require less frequent dosing but take longer to reach steady state. Individual patient factors such as age, hepatic function, and concurrent medications may require dose adjustments. Abrupt discontinuation should be avoided due to risk of withdrawal symptoms including potentially life-threatening seizures."
    )
    
    stage: str = Field(
        ...,
        description="Conversion status",
        example="Conversion Complete"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the conversion result",
        example="Benzodiazepine conversion calculated"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 10.0,
                "unit": "mg",
                "interpretation": "Benzodiazepine conversion: 2.0 mg lorazepam (Ativan) daily is approximately equivalent to 10.0 mg diazepam (Valium) daily (conversion ratio: 1:5.00). Original medication: intermediate acting (12-24 hours) with half-life 10-20 hours. Target medication: long acting (>24 hours) with half-life 20-100 hours. IMPORTANT CLINICAL CONSIDERATIONS: This conversion is intended for interchanging benzodiazepines in patients already on benzodiazepine therapy, NOT for calculating initial doses in benzodiazepine-naive patients. Use the lower end of the dose range initially to minimize oversedation risk. Monitor closely for signs of oversedation (sedation, confusion, ataxia) or withdrawal symptoms (anxiety, insomnia, tremor, seizures). Consider half-life differences when timing the conversion - longer-acting medications may require less frequent dosing but take longer to reach steady state. Individual patient factors such as age, hepatic function, and concurrent medications may require dose adjustments. Abrupt discontinuation should be avoided due to risk of withdrawal symptoms including potentially life-threatening seizures.",
                "stage": "Conversion Complete",
                "stage_description": "Benzodiazepine conversion calculated"
            }
        }