# Guide for Programming Agents: Implementing New Calculators in nobra_calculator

This guide is intended for programming agents (AI assistants) to implement new medical calculators within the modular, specialty-organized structure of the **nobra_calculator API**.

## 🤖 Automated Workflow

### Continuous Implementation Process

This document defines an automated flow where Claude Code works autonomously implementing medical calculators progressively:

1. **📋 Check Task List** - Consult `@CALC_LIST.md` to identify the next calculator to implement
2. **📖 Review Context** - Read `@README.md` to understand the current application and architecture
2.5. **Search on MDCALC via Tavily/Firecrawl MCP** - Use Tavily/Firecrawl search to find information on how to calculate the score in question, its interpretation, and citeable references. Preferably on MDCALC. CRITICAL STEP. If Tavily is not avaliable, use Firecrawl MCP.
3. **🏗️ Implement Calculator** - Follow the steps described in this document
4. **✅ Mark Completion** - Update `@CALC_LIST.md` with a check for the implemented calculator
5. **🗜️ Compact Conversation** - Use the `/compact` command to optimize context
6. **🔄 Restart Cycle** - Return to step 1 for the next implementation

### Criteria for Selecting the Next Calculator

When consulting `@CALC_LIST.md`, prioritize calculators that:
- Do not have ✅ (not yet implemented)
- Are from fundamental medical categories (cardiology, nephrology, neurology)
- Have well-documented and standardized formulas
- Are widely used in clinical practice

### Process Automation

The agent must work autonomously following this flow:
- **Do not request confirmations** for each individual calculator
- **Completely implement** each calculator before proceeding
- **Test functionality** via reload and API checks
- **Adequately document** each implementation
- **Maintain quality** and consistency across all implementations

## 🏗️ API Architecture (Post-Refactoring)

### Directory Structure
```
nobra_calculator/
├── app/
│   ├── models/
│   │   ├── shared.py            # Common models, enums, base classes
│   │   └── scores/              # Score models organized by specialty
│   │       ├── __init__.py      # Main import aggregator
│   │       ├── cardiology/
│   │       │   ├── __init__.py
│   │       │   ├── cha2ds2_vasc.py
│   │       │   └── acc_aha_hf_staging.py
│   │       ├── nephrology/
│   │       │   ├── __init__.py
│   │       │   ├── ckd_epi_2021.py
│   │       │   └── abic_score.py
│   │       └── ... (other specialties)
│   ├── routers/
│   │   ├── scores.py            # Main router with common endpoints
│   │   └── scores/              # Score endpoints organized by specialty
│   │       ├── __init__.py      # Router aggregator
│   │       ├── cardiology/
│   │       │   ├── __init__.py
│   │       │   ├── cha2ds2_vasc.py
│   │       │   └── acc_aha_hf_staging.py
│   │       └── ... (other specialties)
│   └── services/                # Business Logic (loading and execution)
├── calculators/                 # ⭐ Python modules with calculation logic
├── scores/                      # ⭐ Score Metadata (JSON)
├── main.py                     # Main FastAPI application
└── requirements.txt            # Dependencies
```

### Workflow
1. **ScoreService** loads metadata from JSONs in `/scores/`
2. **CalculatorService** dynamically imports modules from `/calculators/`
3. **API Routes** expose endpoints for calculations and metadata
4. **Reload System** allows adding scores without restarting

### Medical Specialties
The following specialties are currently organized in the system:
- `cardiology`
- `nephrology`
- `pulmonology`
- `neurology`
- `hematology`
- `emergency`
- `psychiatry`
- `pediatrics`
- `geriatrics`
- `rheumatology`
- `infectious_disease`

## 📝 Implementing a New Calculator

### STEP 1: Create the JSON Metadata File

Create a file in `/scores/{score_id}.json` following this structure:

```json
{
  "id": "score_name",
  "title": "Full Score Title",
  "description": "Detailed description of what the score calculates",
  "category": "medical_specialty",
  "version": "year_or_version",
  "parameters": [
    {
      "name": "parameter1",
      "type": "string|integer|float",
      "required": true,
      "description": "Parameter description",
      "options": ["option1", "option2"],  // For strings with fixed values
      "validation": {
        "min": 0,           // For numbers
        "max": 100,
        "enum": ["val1", "val2"]  // For strings
      },
      "unit": "unit"
    }
  ],
  "result": {
    "name": "result_name",
    "type": "float|integer|string",
    "unit": "result_unit",
    "description": "Result description"
  },
  "interpretation": {
    "ranges": [
      {
        "min": 0,
        "max": 10,
        "stage": "Stage1",
        "description": "Short description",
        "interpretation": "Detailed clinical interpretation"
      }
    ]
  },
  "references": [
    "Bibliographic reference 1",
    "Bibliographic reference 2"
  ],
  "formula": "Mathematical formula in text",
  "notes": [
    "Important note 1",
    "Important note 2"
  ]
}
```

### STEP 2: Implement the Python Calculator

Create a file in `/calculators/{score_id}.py` with this structure:

```python
"""
{Score Name} Calculator

Brief description of what it calculates and references.
"""

import math
from typing import Dict, Any


class {ScoreId}Calculator:
    """Calculator for {Score Name}"""
    
    def __init__(self):
        # Formula constants
        self.CONSTANT_1 = value
        self.CONSTANT_2 = value
    
    def calculate(self, param1: type, param2: type, param3: type) -> Dict[str, Any]:
        """
        Calculates the score using the provided parameters
        
        Args:
            param1 (type): Description of parameter 1
            param2 (type): Description of parameter 2
            param3 (type): Description of parameter 3
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(param1, param2, param3)
        
        # Calculation logic
        result = self._calculate_formula(param1, param2, param3)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "unit",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, param1, param2, param3):
        """Validates input parameters"""
        
        # Specific validations for each parameter
        if not isinstance(param1, expected_type):
            raise ValueError("Param1 must be of type X")
        
        if param2 < min_value or param2 > max_value:
            raise ValueError(f"Param2 must be between {min_value} and {max_value}")
    
    def _calculate_formula(self, param1, param2, param3):
        """Implements the score's mathematical formula"""
        
        # Implement specific calculation logic
        result = param1 * param2 + param3  # Example
        
        # Round if necessary
        return round(result, 2)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (float): Calculated value
            
        Returns:
            Dict with interpretation
        """
        
        # Logic based on ranges defined in JSON
        if result >= 90:
            return {
                "stage": "Normal",
                "description": "Normal result",
                "interpretation": "Detailed clinical interpretation"
            }
        elif result >= 60:
            return {
                "stage": "Mild",
                "description": "Mild alteration",
                "interpretation": "Detailed clinical interpretation"
            }
        # ... more conditions
        
        else:
            return {
                "stage": "Severe",
                "description": "Severe alteration",
                "interpretation": "Detailed clinical interpretation"
            }


def calculate_{score_id}(param1, param2, param3) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = {ScoreId}Calculator()
    return calculator.calculate(param1, param2, param3)
```

### STEP 3: Create Pydantic Models

Create a file in `/app/models/scores/{specialty}/{score_id}.py`:

Example:

```python
"""
4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) Models

Request and response models for 4PEPS calculation.

References (Vancouver style):
1. Roy PM, Friou E, Germeau B, Douillet D, Kline JA, Righini M, et al. Derivation and 
   Validation of a 4-Level Clinical Pretest Probability Score for Suspected Pulmonary 
   Embolism to Safely Decrease Imaging Testing. JAMA Cardiol. 2021 Jun 1;6(6):669-677. 
   doi: 10.1001/jamacardio.2021.0064.
2. Stals MAM, Beenen LFM, Coppens M, Faber LM, Hofstee HMA, Hovens MMC, et al. 
   Performance of the 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) 
   in the diagnostic management of pulmonary embolism: An external validation study. 
   Thromb Res. 2023 Nov;231:65-75. doi: 10.1016/j.thromres.2023.09.010.
3. Chiang P, Robert-Ebadi H, Perrier A, Roy PM, Sanchez O, Righini M, et al. 
   Pulmonary embolism risk stratification: external validation of the 4-level Clinical 
   Pretest Probability Score (4PEPS). Res Pract Thromb Haemost. 2024 Feb 15;8(1):102348. 
   doi: 10.1016/j.rpth.2024.102348.

The 4PEPS is a clinical decision tool that uses 13 clinical variables to stratify 
patients with suspected pulmonary embolism into four probability categories, allowing 
for safe reduction of imaging studies in low-risk patients. This score can safely 
rule out PE in 58% of patients without imaging while maintaining a failure rate of 1.3%.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FourPepsRequest(BaseModel):
    """
    Request model for 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)
    
    The 4PEPS uses 13 clinical variables to assess pulmonary embolism probability:
    
    Age Categories:
    - under_50: Age <50 years (-2 points)
    - 50_to_64: Age 50-64 years (-1 point)  
    - 65_or_over: Age ≥65 years (0 points)
    
    Clinical Variables (each yes/no):
    - Chronic respiratory disease (-1 point if yes)
    - Heart rate <80 bpm (-1 point if yes)
    - Chest pain AND acute dyspnea (+1 point if yes)
    - Male gender (+2 points if yes)
    - Hormonal estrogenic treatment (+2 points if yes)
    - Personal history of VTE (+2 points if yes)
    - Syncope (+2 points if yes)
    - Immobility within 4 weeks (+2 points if yes)
    - Pulse oxygen saturation <95% (+3 points if yes)
    - Calf pain/unilateral lower limb edema (+3 points if yes)
    - PE is most likely diagnosis (+5 points if yes)

    References (Vancouver style):
    1. Roy PM, Friou E, Germeau B, Douillet D, Kline JA, Righini M, et al. Derivation and 
    Validation of a 4-Level Clinical Pretest Probability Score for Suspected Pulmonary 
    Embolism to Safely Decrease Imaging Testing. JAMA Cardiol. 2021 Jun 1;6(6):669-677. 
    doi: 10.1001/jamacardio.2021.0064.
    2. Stals MAM, Beenen LFM, Coppens M, Faber LM, Hofstee HMA, Hovens MMC, et al. 
    Performance of the 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) 
    in the diagnostic management of pulmonary embolism: An external validation study. 
    Thromb Res. 2023 Nov;231:65-75. doi: 10.1016/j.thromres.2023.09.010.
    3. Chiang P, Robert-Ebadi H, Perrier A, Roy PM, Sanchez O, Righini M, et al. 
    Pulmonary embolism risk stratification: external validation of the 4-level Clinical 
    Pretest Probability Score (4PEPS). Res Pract Thromb Haemost. 2024 Feb 15;8(1):102348. 
    doi: 10.1016/j.rpth.2024.102348.
    """
    
    age_category: Literal["under_50", "50_to_64", "65_or_over"] = Field(
        ...,
        description="Patient age category. Under 50 years scores -2 points, 50-64 years scores -1 point, 65 or over scores 0 points",
        example="50_to_64"
    )
    
    chronic_respiratory_disease: Literal["yes", "no"] = Field(
        ...,
        description="Presence of chronic respiratory disease (COPD, asthma, pulmonary fibrosis, etc.). Scores -1 point if yes",
        example="no"
    )
    
    heart_rate_under_80: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate less than 80 beats per minute. Scores -1 point if yes",
        example="no"
    )
    
    chest_pain_dyspnea: Literal["yes", "no"] = Field(
        ...,
        description="Presence of BOTH chest pain AND acute dyspnea (not just one). Scores +1 point if yes",
        example="yes"
    )
    
    male_gender: Literal["yes", "no"] = Field(
        ...,
        description="Patient is male. Scores +2 points if yes",
        example="yes"
    )
    
    hormonal_treatment: Literal["yes", "no"] = Field(
        ...,
        description="Current hormonal estrogenic treatment (oral contraceptives, hormone replacement therapy). Scores +2 points if yes",
        example="no"
    )
    
    personal_history_vte: Literal["yes", "no"] = Field(
        ...,
        description="Personal history of venous thromboembolism (previous DVT or PE). Scores +2 points if yes",
        example="no"
    )
    
    syncope: Literal["yes", "no"] = Field(
        ...,
        description="Recent syncope (fainting episode). Scores +2 points if yes",
        example="no"
    )
    
    immobility_4_weeks: Literal["yes", "no"] = Field(
        ...,
        description="Immobility within the last 4 weeks (bed rest, wheelchair, cast, surgery, etc.). Scores +2 points if yes",
        example="no"
    )
    
    oxygen_saturation_under_95: Literal["yes", "no"] = Field(
        ...,
        description="Pulse oxygen saturation less than 95% on room air. Scores +3 points if yes",
        example="no"
    )
    
    calf_pain_edema: Literal["yes", "no"] = Field(
        ...,
        description="Calf pain and/or unilateral lower limb edema suggesting DVT. Scores +3 points if yes",
        example="no"
    )
    
    pe_most_likely: Literal["yes", "no"] = Field(
        ...,
        description="PE is the most likely diagnosis based on clinician's overall assessment. Scores +5 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "50_to_64",
                "chronic_respiratory_disease": "no",
                "heart_rate_under_80": "no",
                "chest_pain_dyspnea": "yes",
                "male_gender": "yes",
                "hormonal_treatment": "no",
                "personal_history_vte": "no",
                "syncope": "no",
                "immobility_4_weeks": "no",
                "oxygen_saturation_under_95": "no",
                "calf_pain_edema": "no",
                "pe_most_likely": "no"
            }
        }


class FourPepsResponse(BaseModel):
    """
    Response model for 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)
    
    The 4PEPS score ranges from -5 to +20 points and classifies patients into:
    - Very Low (<0 points): PE ruled out, no testing needed
    - Low (0-5 points): Use D-dimer with 1000 μg/L cut-off
    - Moderate (6-12 points): Use age-adjusted D-dimer cut-off
    - High (>12 points): Proceed directly to imaging
    
    Reference: Roy PM, et al. JAMA Cardiol. 2021;6(6):669-677.
    """
    
    result: int = Field(
        ...,
        description="4PEPS score calculated from clinical variables (range: -5 to +20 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the score",
        example="Low probability of PE. Use D-dimer with 1000 μg/L cut-off. If D-dimer <1000 μg/L, PE is ruled out."
    )
    
    stage: str = Field(
        ...,
        description="Clinical probability category (Very Low, Low, Moderate, High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the probability category",
        example="Low clinical probability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Low probability of PE. Use D-dimer with 1000 μg/L cut-off. If D-dimer <1000 μg/L, PE is ruled out.",
                "stage": "Low",
                "stage_description": "Low clinical probability"
            }
        }
```

### STEP 4: Update Specialty Model Imports

Add to `/app/models/scores/{specialty}/__init__.py`:

```python
# Import the new score models
from .{score_id} import {ScoreId}Request, {ScoreId}Response

# Add to __all__ export list
__all__ = [
    # ... existing exports ...
    "{ScoreId}Request",
    "{ScoreId}Response",
]
```

### STEP 5: Create Router Endpoint

Create a file in `/app/routers/scores/{specialty}/{score_id}.py`:

```python
"""
{Score Name} Router

Endpoint for calculating {Score Name}.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.{specialty}.{score_id} import (
    {ScoreId}Request,
    {ScoreId}Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/{score_id}", response_model={ScoreId}Response)
async def calculate_{score_id}(request: {ScoreId}Request):
    """
    Calculates {Score Name}
    
    {Brief description of what this score is used for}
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        {ScoreId}Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("{score_id}", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating {Score Name}",
                    "details": {"parameters": parameters}
                }
            )
        
        return {ScoreId}Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for {Score Name}",
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
```

### STEP 6: Update Specialty Router Imports

Add to `/app/routers/scores/{specialty}/__init__.py`:

```python
from fastapi import APIRouter
from .{score_id} import router as {score_id}_router

# Create the specialty router if it doesn't exist
router = APIRouter()

# Include the new score router
router.include_router({score_id}_router)
```

### STEP 7: Update Main Score Model Exports (if needed)

If the score should be importable from the main scores module, add to `/app/models/scores/__init__.py`:

```python
# Add the import
from .{specialty}.{score_id} import {ScoreId}Request, {ScoreId}Response

# Add to __all__ if maintaining backward compatibility
__all__ = [
    # ... existing exports ...
    "{ScoreId}Request",
    "{ScoreId}Response",
]
```

## 🧪 Testing the Implementation

### 1. Reload Scores
```bash
curl -X POST http://localhost:8000/api/reload
```

### 2. Check if the Score Appears in the List
```bash
curl http://localhost:8000/api/scores
```

### 3. Test the Calculation
```bash
curl -X POST http://localhost:8000/{score_id} \  
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": 50, "param3": 1.5}'
```
**Careful!** -> There is no /api on the specific score routes! It`s just root_url/score_id

### 4. Check Metadata
```bash
curl http://localhost:8000/api/scores/{score_id}
```

## ⚠️ Important Points

### Naming Conventions
- **score_id**: snake_case (e.g., `ckd_epi_2021`)
- **Calculator Class**: PascalCase + "Calculator" (e.g., `CkdEpi2021Calculator`)  
- **Convenience Function**: `calculate_{score_id}` (e.g., `calculate_ckd_epi_2021`)
- **Model Classes**: PascalCase + "Request/Response" (e.g., `CkdEpi2021Request`)
- **Specialty folders**: lowercase with underscores (e.g., `infectious_disease`)

### File Organization
- Models go in `/app/models/scores/{specialty}/{score_id}.py`
- Routers go in `/app/routers/scores/{specialty}/{score_id}.py`
- Each specialty has its own `__init__.py` files for aggregation
- Maintain the hierarchical import structure

### Mandatory Validations
- ✅ Validate parameter types
- ✅ Validate value ranges/limits
- ✅ Handle special cases (division by zero, negative values)
- ✅ Return descriptive errors

### Return Structure
The return **MUST** always have this minimum structure:
```python
{
    "result": float|int,           # Calculated value
    "unit": str,                   # Unit of measurement
    "interpretation": str,         # Clinical interpretation
    "stage": str,                  # Classification/stage (optional)
    "stage_description": str       # Stage description (optional)
}
```
### References and information
In the pydantic model, we **MUST** keep the reference for the given score, in *Vancouver* style if possible. We should also keep *info* on what every field means so It makes sense to the client.
The clear, the better. This is for Science - do your best.

## 🐛 Common Troubleshooting

### Error: "Score not found"
- ✅ Check if the JSON file exists in `/scores/`
- ✅ Check if the `id` in the JSON matches the file name
- ✅ Execute reload: `POST /api/reload`

### Error: "Calculator not found"
- ✅ Check if the Python file exists in `/calculators/`
- ✅ Check if the `calculate_{score_id}` function exists
- ✅ Check imports and Python syntax

### Error: "Invalid parameters"
- ✅ Check data types in parameters
- ✅ Check validation ranges
- ✅ Compare with JSON definitions

### Error: "Invalid JSON"
- ✅ Validate JSON syntax
- ✅ Check mandatory fields: `id`, `title`, `description`, `category`, `parameters`, `result`
- ✅ Check if `parameters` is an array and `result` is an object

### Error: "Module import failed"
- ✅ Check if specialty `__init__.py` files are updated
- ✅ Verify model class names match imports
- ✅ Ensure proper indentation in Python files

## 🔄 Automated Implementation Protocol

### Detailed Flow per Iteration

For each implementation cycle, strictly follow:

#### 1. **📋 Consult CALC_LIST.md**
```
- Read file @CALC_LIST.md
- Identify first calculator without ✅
- Prioritize by clinical relevance and formula availability
- Select calculator for implementation
```

#### 2. **📖 Review README.md** 
```
- Read @README.md for application context
- Check current directory structure
- Confirm naming conventions
- Understand endpoint architecture
```

#### 3. **🏗️ Complete Implementation**
```
- Create JSON in /scores/{score_id}.json
- Implement calculator in /calculators/{score_id}.py
- Create Pydantic models in /app/models/scores/{specialty}/{score_id}.py
- Create router in /app/routers/scores/{specialty}/{score_id}.py
- Update specialty __init__.py files (models and routers)
- Test with POST /api/reload
- Verify functionality via API
- Validate all input scenarios
```

#### 4. **✅ Update CALC_LIST.md**
```
- Add ✅ to the line of the implemented calculator
- Maintain original file formatting
- Confirm that the change was saved
```

#### 5. **🗜️ Compact Context**
```
- Execute /compact command
- Summarize implementations performed
- Prepare context for next cycle
```

#### 6. **🔄 Proceed Automatically**
```
- Return to step 1 without interruption
- Continue until list is exhausted or stop instruction is received
- Maintain quality and consistency across all implementations
```

### Quality Guidelines

- **Rigorous Validation**: Each calculator must have complete input validations
- **Functional Tests**: Always test reload and endpoints after implementation  
- **Complete Documentation**: Include bibliographic references and clinical notes
- **Consistent Naming**: Follow snake_case for IDs and PascalCase for classes
- **Clinical Interpretation**: Provide appropriate medical interpretations for each result
- **Specialty Organization**: Place files in correct specialty folders
- **Scientific accuracy**: Always keep the score reference in Vacnouver style in the pydantic model. Always explain how to use and interpret each field.

### Error Handling

- **Implementation Error**: Correct and retest before marking as complete
- **Incomplete Formula**: Seek additional references or skip to the next calculator
- **Naming Conflict**: Adapt name following established conventions
- **Missing Specialty**: Create new specialty folder structure if needed

## 🎯 Summary of Steps

1. **Create JSON** in `/scores/{score_id}.json` with complete metadata
2. **Implement calculator** in `/calculators/{score_id}.py` with `calculate_{score_id}` function  
3. **Create Pydantic models** in `/app/models/scores/{specialty}/{score_id}.py`
4. **Update specialty model imports** in `/app/models/scores/{specialty}/__init__.py`
5. **Create router endpoint** in `/app/routers/scores/{specialty}/{score_id}.py`
6. **Update specialty router imports** in `/app/routers/scores/{specialty}/__init__.py`
7. **Test** via reload and API endpoints
8. **Document** references and formulas appropriately
9. **Mark as complete** in CALC_LIST.md
10. **Compact conversation** and restart cycle

By following this guide, any programming agent can implement new medical calculators in nobra_calculator's modular architecture consistently, functionally, and fully automated! 🚀

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.