# nobra_calculator 🏥

Modular API for medical calculations and scores developed with FastAPI, originally designed for [Nobra](https://www.nobregamedtech.com), our AI research agent for medical doctors.

## 🌐 Live API

**🚀 Try it now at: https://calculator.nobra.app.br**

- **Free tier**: 10 requests per second
- **Commercial use**: Contact us at daniel@nobregamedtech.com.br for higher limits
- **Self-hosted**: Deploy locally using the instructions below

## 📋 Description

nobra_calculator is a scalable REST API that allows the calculation of various medical scores and indices. Originally developed as part of the **Nobra ecosystem** at [Nobrega MedTech](https://www.nobregamedtech.com), we've decided to open-source this powerful tool to benefit the global medical community.

Our company specializes in AI solutions for healthcare, focusing on academic support and medical decision-making tools. This calculator represents our commitment to advancing evidence-based medicine through technology.

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

### Live API Documentation
- **Swagger UI**: https://calculator.nobra.app.br/docs
- **ReDoc**: https://calculator.nobra.app.br/redoc
- **Health Check**: https://calculator.nobra.app.br/health

### Local Development Documentation
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

# Calculate CKD-EPI 2021 (Live API)
curl -X POST https://calculator.nobra.app.br/ckd_epi_2021 \
  -H "Content-Type: application/json" \
  -d '{"sex": "female", "age": 65, "serum_creatinine": 1.2}'

# Calculate CKD-EPI 2021 (Local)
curl -X POST http://localhost:8000/ckd_epi_2021 \
  -H "Content-Type: application/json" \
  -d '{"sex": "female", "age": 65, "serum_creatinine": 1.2}'
```

## 🤝 Contributing

We welcome contributions from the medical and developer communities! This project is part of our mission to democratize access to evidence-based medical tools.

### How to Contribute

1. **Fork the project** on GitHub
2. **Create a feature branch** (`git checkout -b feature/amazing-new-score`)
3. **Add your medical calculator** following our [implementation guide](CLAUDE.md)
4. **Test thoroughly** - medical calculations require precision
5. **Include proper references** - all scores must cite original publications
6. **Commit your changes** (`git commit -am 'Add APACHE II score'`)
7. **Push to your branch** (`git push origin feature/amazing-new-score`)
8. **Open a Pull Request** with a detailed description

### What We're Looking For

- **New medical scores and calculators** from any medical specialty
- **Bug fixes and improvements** to existing calculations
- **Documentation enhancements** and translations
- **Performance optimizations** and code quality improvements
- **Test coverage** improvements

### Code Quality Standards

- Follow our established patterns for new calculators
- Include comprehensive input validation
- Provide clinical interpretations for all results
- Cite original research using Vancouver style references
- Test with edge cases and boundary values

## 📄 License

This project is licensed under Apache 2.0. See the `LICENSE` file for details.

## 👨‍💻 About

### Author
**Daniel Nobrega Medeiros**
- Email: daniel@nobregamedtech.com.br
- GitHub: [@danielxmed](https://github.com/danielxmed)
- Repository: https://github.com/danielxmed/nobra_calculator.git

### Company
**[Nobrega MedTech](https://www.nobregamedtech.com)** - AI Solutions for Healthcare
- Specializing in academic support tools for medical education
- Developing AI-powered medical decision support systems
- Building the **Nobra ecosystem** - AI research agents for medical professionals
- Committed to evidence-based medicine and open-source healthcare tools

### The Nobra Project
This calculator was originally developed as a component of **Nobra**, our comprehensive AI research agent designed to assist medical doctors with:
- Evidence-based clinical decision making
- Medical literature research and synthesis
- Educational support for medical training
- Real-time access to medical calculators and scores

By open-sourcing this calculator API, we're contributing to the global effort to make medical knowledge more accessible and standardized.

## 🌟 Support the Project

- ⭐ **Star this repository** if you find it useful
- 🐛 **Report bugs** and suggest improvements
- 📖 **Contribute new calculators** from your medical specialty
- 📢 **Share with colleagues** in the medical community
- 💼 **Contact us** for enterprise solutions and custom development

## ⚠️ Medical Disclaimer

**IMPORTANT**: This API is intended for educational and research purposes only. It should not be used as a substitute for professional clinical judgment. All medical calculations should be verified independently, and clinical decisions should always involve qualified healthcare professionals.

- Always validate results with original references
- Consider patient-specific factors not captured in scores
- Use as a supplement to, not replacement for, clinical expertise
- Verify calculations independently for critical decisions