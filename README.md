# nobra_calculator

Modular API for medical calculations and scores developed with FastAPI.

## 📋 Description

nobra_calculator is a scalable REST API that allows the calculation of various medical scores and indices. Its modular architecture, organized by medical specialties, facilitates the progressive addition of new calculations.

### Features

- **Modular**: Specialty-organized structure for easy addition of new medical scores
- **Scalable**: Clean architecture designed for growth
- **Documented**: Automatic documentation with Swagger/OpenAPI
- **Validated**: Robust parameter validation with Pydantic
- **Interpreted**: Returns not only the result but also the clinical interpretation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/danielxmed/nobra_calculator.git
cd nobra_calculator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`


## 🛠️ API Endpoints

### Scores
- `GET /api/scores` - Lists all available scores
- `GET /api/scores/{score_id}` - Metadata for a specific score
- `GET /api/categories` - Lists medical categories
- `POST /api/reload` - Reloads scores and calculators


### Specific Score Endpoints
Each score also has its dedicated endpoint:
- `POST /ckd_epi_2021` - CKD-EPI 2021
- `POST /cha2ds2_vasc` - CHA₂DS₂-VASc
...

### System
- `GET /health` - API health check
- `GET /` - API information

## 📁 Project Structure

```
nobra_calculator/
├── app/
│   ├── models/
│   │   ├── shared.py           # Common models and enums
│   │   └── scores/             # Score models by specialty
│   │       ├── cardiology/
│   │       ├── nephrology/
│   │       ├── pulmonology/
│   │       └── ...
│   ├── routers/
│   │   ├── scores.py           # Main router with common endpoints
│   │   └── scores/             # Score endpoints by specialty
│   │       ├── cardiology/
│   │       ├── nephrology/
│   │       └── ...
│   └── services/               # Business Logic
├── calculators/                # Calculation Modules
├── scores/                     # Score Metadata (JSON)
├── main.py                     # Main application
└── requirements.txt            # Dependencies
```

## 🔧 Adding New Scores

To add a new score:

### 1. Create the JSON metadata file
Create `/scores/{score_id}.json` with the score metadata:
```json
{
  "id": "new_score",
  "title": "Score Title",
  "description": "Detailed description",
  "category": "medical_specialty",
  "parameters": [...],
  "result": {...},
  "interpretation": {...}
}
```

### 2. Create the calculation module
Create `/calculators/{score_id}.py`:
```python
def calculate_new_score(param1, param2):
    # Calculation logic
    result = ...
    return {
        "result": result,
        "unit": "unit",
        "interpretation": "interpretation"
    }
```

### 3. Create the Pydantic models
Create `/app/models/scores/{specialty}/{score_id}.py`:
```python
from pydantic import BaseModel, Field

class NewScoreRequest(BaseModel):
    """Request model for New Score"""
    param1: str = Field(..., description="Parameter 1")
    param2: float = Field(..., description="Parameter 2")

class NewScoreResponse(BaseModel):
    """Response model for New Score"""
    result: float = Field(..., description="Calculation result")
    unit: str = Field(..., description="Result unit")
    interpretation: str = Field(..., description="Clinical interpretation")
```

### 4. Create the router endpoint
Create `/app/routers/scores/{specialty}/{score_id}.py`:
```python
from fastapi import APIRouter, HTTPException
from app.models.scores.{specialty}.{score_id} import NewScoreRequest, NewScoreResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/new_score", response_model=NewScoreResponse)
async def calculate_new_score(request: NewScoreRequest):
    """Calculate New Score"""
    try:
        result = calculator_service.calculate_score("new_score", request.dict())
        return NewScoreResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 5. Update the specialty __init__.py files
- Add imports to `/app/models/scores/{specialty}/__init__.py`
- Add router to `/app/routers/scores/{specialty}/__init__.py`

### 6. Reload the scores
```bash
curl -X POST http://localhost:8000/api/reload
```

## 🧪 Testing

### Manual test with curl:

```bash
# Health check
curl http://localhost:8000/health

# List scores
curl http://localhost:8000/api/scores

# Calculate CKD-EPI 2021
curl -X POST http://localhost:8000/ckd_epi_2021 \
  -H "Content-Type: application/json" \
  -d '{"sex": "female", "age": 65, "serum_creatinine": 1.2}'
```

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Adds new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under Apache 2.0. See the `LICENSE` file for details.

## 👨‍💻 Author

**Daniel Nobrega Medeiros**
- Email: daniel@nobregamedtech.com.br
- GitHub: [@danielxmed](https://github.com/danielxmed)
- Repository: https://github.com/danielxmed/nobra_calculator.git

## ⚠️ Disclaimer

This API is intended for educational and research purposes only. It should not be used as a substitute for professional clinical judgment. Always consult a qualified healthcare professional for medical diagnosis and treatment.