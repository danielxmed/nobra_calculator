"""
Benzodiazepine Conversion Calculator Router

Endpoint for calculating benzodiazepine conversions for safe medication interchanging.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.benzodiazepine_conversion import (
    BenzodiazepineConversionRequest,
    BenzodiazepineConversionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/benzodiazepine_conversion", response_model=BenzodiazepineConversionResponse)
async def calculate_benzodiazepine_conversion(request: BenzodiazepineConversionRequest):
    """
    Calculates Benzodiazepine Conversion between different medications
    
    The Benzodiazepine Conversion Calculator provides safe equivalents between different 
    benzodiazepine medications for patients already established on benzodiazepine therapy. 
    This tool is essential for medication transitions, hospital formulary changes, and 
    clinical situations requiring benzodiazepine substitution.
    
    **Target Population:**
    - Patients already on benzodiazepine therapy requiring medication changes
    - Hospital formulary conversions
    - Medication reconciliation during transitions of care
    - Clinical situations requiring benzodiazepine substitution
    
    **⚠️ NOT for benzodiazepine-naive patients or initial dosing**
    
    **Supported Medications:**
    
    **Short Acting (6-12 hours):**
    - **Alprazolam (Xanax)** - Half-life: 11-13 hours, high potency
    - **Oxazepam (Serax)** - Half-life: 4-15 hours, lower potency
    - **Temazepam (Restoril)** - Half-life: 3-18 hours, primarily for sleep
    
    **Intermediate Acting (12-24 hours):**
    - **Lorazepam (Ativan)** - Half-life: 10-20 hours, high potency
    
    **Long Acting (>24 hours):**
    - **Chlordiazepoxide (Librium)** - Half-life: 36-200 hours, lower potency
    - **Clonazepam (Klonopin)** - Half-life: 18-50 hours, high potency
    - **Diazepam (Valium)** - Half-life: 20-100 hours, reference standard
    
    **Very Short Acting (<6 hours):**
    - **Midazolam (Versed)** - Half-life: 1-4 hours, procedural sedation
    
    **Conversion Examples:**
    - 1 mg Lorazepam ≈ 10 mg Diazepam
    - 0.5 mg Alprazolam ≈ 5 mg Diazepam
    - 0.25 mg Clonazepam ≈ 5 mg Diazepam
    - 25 mg Chlordiazepoxide ≈ 5 mg Diazepam
    
    **Clinical Guidelines:**
    
    **Safety Protocol:**
    1. **Start Low**: Use calculated dose or lower to minimize oversedation
    2. **Monitor Closely**: Watch for oversedation and withdrawal symptoms
    3. **Adjust Gradually**: Titrate based on individual patient response
    4. **Consider Context**: Account for age, liver function, concurrent medications
    
    **Timing Considerations:**
    - **Short → Long Acting**: May need less frequent dosing, longer time to steady state
    - **Long → Short Acting**: May need more frequent dosing, faster onset/offset
    - **Half-life Overlap**: Consider timing to prevent withdrawal gaps
    
    **Monitoring Parameters:**
    - **Oversedation Signs**: Sedation, confusion, ataxia, respiratory depression
    - **Withdrawal Signs**: Anxiety, insomnia, tremor, diaphoresis, seizures
    - **Vital Signs**: Blood pressure, heart rate, respiratory rate
    - **Mental Status**: Alertness, orientation, coordination
    
    **Special Populations:**
    - **Elderly**: Increased sensitivity, longer half-lives, higher fall risk
    - **Hepatic Impairment**: Reduced metabolism, dose reduction needed
    - **Renal Impairment**: Generally no dose adjustment for most benzodiazepines
    - **Pregnancy**: Avoid if possible, consider neonatal withdrawal
    
    **Drug Interactions:**
    - **CNS Depressants**: Opioids, alcohol, antihistamines - increased sedation risk
    - **CYP3A4 Inhibitors**: Ketoconazole, clarithromycin - increased benzodiazepine levels
    - **CYP3A4 Inducers**: Carbamazepine, phenytoin - decreased benzodiazepine levels
    
    **Withdrawal Prevention:**
    - **Never stop abruptly** - risk of life-threatening seizures
    - **Gradual taper**: 10-25% dose reduction every 1-2 weeks
    - **Monitor symptoms**: Anxiety, insomnia, perceptual disturbances
    - **Consider hospitalization**: For high-dose or complicated withdrawals
    
    **Quality Assurance:**
    - Conversion factors based on established equivalency tables
    - Approximations requiring clinical judgment and individualization
    - Regular review and adjustment based on patient response
    - Documentation of conversion rationale and monitoring plan
    
    **Common Clinical Scenarios:**
    - ICU formulary limitations requiring substitution
    - Transition from IV to oral formulations
    - Patient transfer between healthcare facilities
    - Insurance formulary restrictions
    - Adverse effects requiring medication change
    
    Args:
        request: Benzodiazepine conversion parameters (from drug, dose, to drug)
        
    Returns:
        BenzodiazepineConversionResponse: Equivalent dose with comprehensive clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("benzodiazepine_conversion", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Benzodiazepine Conversion",
                    "details": {"parameters": parameters}
                }
            )
        
        return BenzodiazepineConversionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Benzodiazepine Conversion",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )