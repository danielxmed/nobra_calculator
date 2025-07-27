"""
nobra_calculator - API for medical calculations
"""

__version__ = "1.0.0"
__author__ = "Medical Calculator Team"
__description__ = """
## nobra_calculator - Comprehensive Medical Calculator API

A robust, modular REST API designed for medical professionals and healthcare applications to calculate various medical scores, indices, and clinical assessments.

### 🎯 Key Features

- **🏥 Comprehensive Coverage**: 19+ validated medical calculators across multiple specialties
- **📊 Clinical Interpretations**: Each calculation includes detailed clinical interpretations and recommendations
- **🔒 Production Ready**: Robust input validation, error handling, and standardized responses
- **📚 Evidence-Based**: All calculators based on peer-reviewed medical literature
- **🚀 Easy Integration**: RESTful API with comprehensive OpenAPI documentation
- **🔄 Modular Architecture**: Easy to extend with new calculators

### 🩺 Medical Specialties Covered

- **Cardiology**: CHA₂DS₂-VASc, 6-Minute Walk Distance, ACC/AHA Heart Failure Staging
- **Nephrology**: CKD-EPI 2021 eGFR
- **Pulmonology**: CURB-65, A-a O₂ Gradient
- **Neurology**: ABCD² Score, 4AT Delirium Screen, AIMS, 2HELPS2B
- **Hematology**: Absolute Neutrophil Count, 4Ts HIT Score
- **And many more...

### 🔧 How to Use

1. **Browse Available Scores**: Use `GET /api/scores` to see all available calculators
2. **Get Score Details**: Use `GET /api/scores/{score_id}` for detailed parameter information
3. **Calculate**: Use score-specific endpoints like `POST /api/ckd_epi_2021` or the generic `POST /api/{score_id}/calculate`
4. **Interpret Results**: Each response includes clinical interpretation and recommendations

### ⚠️ Important Notes

- This API is intended for educational and clinical decision support purposes
- Always verify results with clinical judgment
- Not intended to replace professional medical advice
- Ensure proper validation of input parameters

### 📖 Documentation

- **Interactive API Docs**: Available at `/docs`
- **Alternative Docs**: Available at `/redoc`
- **Health Check**: Available at `/health`

For detailed information about each calculator, including formulas, references, and clinical notes, use the metadata endpoints.
"""
