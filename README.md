# nobra_calculator

Modular API for medical calculations and scores developed with FastAPI.

## 📋 Description

nobra_calculator is a scalable REST API that allows the calculation of various medical scores and indices. Its modular architecture facilitates the progressive addition of new calculations.

### Features

- **Modular**: Easy addition of new medical scores
- **Scalable**: Organized structure for growth
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

## 🩺 Available Scores

### CKD-EPI 2021
Calculates the Estimated Glomerular Filtration Rate (eGFR) using the CKD-EPI 2021 equation.

**Endpoint**: `POST /api/ckd_epi_2021`

**Parameters**:
- `sex`: "male" or "female"
- `age`: Age in years (18-120)
- `serum_creatinine`: Serum creatinine in mg/dL (0.1-20.0)

**Example Request**:
```json
{
  "sex": "female",
  "age": 65,
  "serum_creatinine": 1.2
}
```

**Example Response**:
```json
{
  "result": 52.3,
  "unit": "mL/min/1.73 m²",
  "interpretation": "Stage 3a Chronic Kidney Disease. Nephrology follow-up recommended.",
  "stage": "G3a",
  "stage_description": "Mild to moderate decrease in GFR"
}
```

## 🛠️ API Endpoints

### Scores
- `GET /api/scores` - Lists all available scores
- `GET /api/scores/{score_id}` - Metadata for a specific score
- `GET /api/categories` - Lists medical categories
- `POST /api/reload` - Reloads scores and calculators

### Calculations
- `POST /api/ckd_epi_2021` - Calculates CKD-EPI 2021

### System
- `GET /health` - API health check
- `GET /` - API information

## 📁 Project Structure

```
nobra_calculator/
├── app/
│   ├── models/          # Pydantic Models
│   ├── routers/         # API Routes
│   └── services/        # Business Logic
├── calculators/         # Calculation Modules
├── scores/              # Score Metadata (JSON)
├── main.py             # Main application
└── requirements.txt    # Dependencies
```

## 🔧 Adding New Scores

To add a new score:

1. **Create the JSON file** in `/scores/` with the metadata:
```json
{
  "id": "new_score",
  "title": "Score Title",
  "description": "Detailed description",
  "category": "medical_category",
  "parameters": [...],
  "result": {...},
  "interpretation": {...}
}
```

2. **Create the calculation module** in `/calculators/`:
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

3. **Add the endpoint** (optional) or use the generic system

4. **Reload**: `POST /api/reload`

## 🧪 Testing

### Manual test with curl:

```bash
# Health check
curl http://localhost:8000/health

# List scores
curl http://localhost:8000/api/scores

# Calculate CKD-EPI 2021
curl -X POST http://localhost:8000/api/ckd_epi_2021 \
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
