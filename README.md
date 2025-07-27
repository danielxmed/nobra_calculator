# nobra_calculator

API modular para cálculos e scores médicos desenvolvida com FastAPI.

## 📋 Descrição

A nobra_calculator é uma API REST escalável que permite o cálculo de diversos scores e índices médicos. A arquitetura modular facilita a adição de novos cálculos progressivamente.

### Características

- **Modular**: Fácil adição de novos scores médicos
- **Escalável**: Estrutura organizada para crescimento
- **Documentada**: Documentação automática com Swagger/OpenAPI
- **Validada**: Validação robusta de parâmetros com Pydantic
- **Interpretada**: Retorna não apenas o resultado, mas também a interpretação clínica

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/danielxmed/nobra_calculator.git
cd nobra_calculator
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a API:
```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## 📖 Documentação

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🩺 Scores Disponíveis

### CKD-EPI 2021
Calcula a Taxa de Filtração Glomerular Estimada (TFGe) usando a equação CKD-EPI 2021.

**Endpoint**: `POST /api/ckd_epi_2021`

**Parâmetros**:
- `sex`: "masculino" ou "feminino"
- `age`: Idade em anos (18-120)
- `serum_creatinine`: Creatinina sérica em mg/dL (0.1-20.0)

**Exemplo de Request**:
```json
{
  "sex": "feminino",
  "age": 65,
  "serum_creatinine": 1.2
}
```

**Exemplo de Response**:
```json
{
  "result": 52.3,
  "unit": "mL/min/1.73 m²",
  "interpretation": "Estágio 3a de Doença Renal Crônica. Acompanhamento nefrológico recomendado.",
  "stage": "G3a",
  "stage_description": "Diminuição leve a moderada da TFG"
}
```

## 🛠️ Endpoints da API

### Scores
- `GET /api/scores` - Lista todos os scores disponíveis
- `GET /api/scores/{score_id}` - Metadados de um score específico
- `GET /api/categories` - Lista categorias médicas
- `POST /api/reload` - Recarrega scores e calculadoras

### Cálculos
- `POST /api/ckd_epi_2021` - Calcula CKD-EPI 2021

### Sistema
- `GET /health` - Health check da API
- `GET /` - Informações da API

## 📁 Estrutura do Projeto

```
nobra_calculator/
├── app/
│   ├── models/          # Modelos Pydantic
│   ├── routers/         # Rotas da API
│   └── services/        # Lógica de negócio
├── calculators/         # Módulos de cálculo
├── scores/              # Metadados dos scores (JSON)
├── main.py             # Aplicação principal
└── requirements.txt    # Dependências
```

## 🔧 Adicionando Novos Scores

Para adicionar um novo score:

1. **Crie o arquivo JSON** em `/scores/` com os metadados:
```json
{
  "id": "novo_score",
  "title": "Título do Score",
  "description": "Descrição detalhada",
  "category": "categoria_medica",
  "parameters": [...],
  "result": {...},
  "interpretation": {...}
}
```

2. **Crie o módulo de cálculo** em `/calculators/`:
```python
def calculate_novo_score(param1, param2):
    # Lógica do cálculo
    result = ...
    return {
        "result": result,
        "unit": "unidade",
        "interpretation": "interpretação"
    }
```

3. **Adicione o endpoint** (opcional) ou use o sistema genérico

4. **Recarregue**: `POST /api/reload`

## 🧪 Testando

### Teste manual com curl:

```bash
# Health check
curl http://localhost:8000/health

# Listar scores
curl http://localhost:8000/api/scores

# Calcular CKD-EPI 2021
curl -X POST http://localhost:8000/api/ckd_epi_2021 \
  -H "Content-Type: application/json" \
  -d '{"sex": "feminino", "age": 65, "serum_creatinine": 1.2}'
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença Apache 2.0. Veja o arquivo `LICENSE` para detalhes.

## 👨‍💻 Autor

**Daniel Nobrega Medeiros**
- Email: daniel@nobregamedtech.com.br
- GitHub: [@danielxmed](https://github.com/danielxmed)
- Repositório: https://github.com/danielxmed/nobra_calculator.git

## ⚠️ Disclaimer

Esta API é destinada apenas para fins educacionais e de pesquisa. Não deve ser usada como substituto para julgamento clínico profissional. Sempre consulte um profissional de saúde qualificado para diagnóstico e tratamento médico.
