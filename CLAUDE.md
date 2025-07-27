# Guide for Programming Agents: Implementing New Calculators in nobra_calculator

This guide is intended for programming agents (AI assistants) to implement new medical calculators within the modular structure of the **nobra_calculator API**.

## 🤖 Automated Workflow

### Continuous Implementation Process

This document defines an automated flow where Claude Code works autonomously implementing medical calculators progressively:

1. **📋 Check Task List** - Consult `@CALC_LIST.md` to identify the next calculator to implement
2. **📖 Review Context** - Read `@README.md` to understand the current application and architecture
2.5. **Search on MDCALC via Tavily MCP** - Use Tavily search to find information on how to calculate the score in question, its interpretation, and citeable references. Preferably on MDCALC. CRITICAL STEP.
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

## 🏗️ API Architecture

### Directory Structure
```
nobra_calculator/
├── app/
│   ├── models/          # Pydantic Models (requests/responses)
│   ├── routers/         # API Endpoints
│   └── services/        # Business Logic (loading and execution)
├── calculators/         # ⭐ Python modules with calculation logic
├── scores/              # ⭐ Score Metadata (JSON)
├── main.py             # Main FastAPI application
└── requirements.txt    # Dependencies
```

### Workflow
1. **ScoreService** loads metadata from JSONs in `/scores/`
2. **CalculatorService** dynamically imports modules from `/calculators/`
3. **API Routes** expose endpoints for calculations and metadata
4. **Reload System** allows adding scores without restarting

## 📝 Implementing a New Calculator

### STEP 1: Create the JSON Metadata File

Create a file in `/scores/{score_id}.json` following this structure:

```json
{
  "id": "score_name",
  "title": "Full Score Title",
  "description": "Detailed description of what the score calculates",
  "category": "medical_category",
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

If you want specific endpoints, add them to `/app/models/score_models.py`:

```python
class {ScoreId}Request(BaseModel):
    """Request model for {Score Name}"""
    param1: type = Field(..., description="Description")
    param2: int = Field(..., ge=min_val, le=max_val, description="Description")
    param3: float = Field(..., description="Description")
    
    class Config:
        schema_extra = {
            "example": {
                "param1": "example_value",
                "param2": 50,
                "param3": 1.5
            }
        }


class {ScoreId}Response(BaseModel):
    """Response model for {Score Name}"""
    result: float = Field(..., description="Calculation result")
    unit: str = Field(..., description="Result unit")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Stage/classification")
    stage_description: str = Field(..., description="Stage description")
```

### STEP 4: Add Specific Endpoint

In `/app/routers/scores.py`, add:

```python
@router.post("/{score_id}", response_model={ScoreId}Response)
async def calculate_{score_id}(request: {ScoreId}Request):
    """
    Calculates {Score Name}
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        {ScoreId}Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary
        parameters = {
            "param1": request.param1,
            "param2": request.param2,
            "param3": request.param3
        }
        
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
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": 50, "param3": 1.5}'
```

### 4. Check Metadata
```bash
curl http://localhost:8000/api/scores/{score_id}
```

## ⚠️ Important Points

### Naming Conventions
- **score_id**: snake_case (e.g., `ckd_epi_2021`)
- **Calculator Class**: PascalCase + "Calculator" (e.g., `CkdEpi2021Calculator`)  
- **Convenience Function**: `calculate_{score_id}` (e.g., `calculate_ckd_epi_2021`)

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
- Implement pydantic models
- Implements specific endopoint for the score
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

### Error Handling

- **Implementation Error**: Correct and retest before marking as complete
- **Incomplete Formula**: Seek additional references or skip to the next calculator
- **Naming Conflict**: Adapt name following established conventions

## 🎯 Summary of Steps

1. **Create JSON** in `/scores/{score_id}.json` with complete metadata
2. **Implement calculator** in `/calculators/{score_id}.py` with `calculate_{score_id}` function  
3. **Test** via reload and API endpoints
4. **Add Pydantic models** for specific endpoints
5. **Document** references and formulas appropriately
6. **Mark as complete** in CALC_LIST.md
7. **Compact conversation** and restart cycle

By following this guide, any programming agent can implement new medical calculators in nobra_calculator consistently, functionally, and fully automated! 🚀
