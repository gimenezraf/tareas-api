from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/etapas/{estructura_procesal}")
def obtener_etapas(estructura_procesal: str):
    estructura = estructura_procesal.lower()

    if estructura == "ordinario":
        return [
            {"etapa": "Demanda"},
            {"etapa": "Contestación de demanda", "plazo_dias": 30, "tipo_plazo": "corridos"},
            {"etapa": "Evacuar excepciones", "plazo_dias": 15, "tipo_plazo": "hábiles", "opcional": True},
            {"etapa": "Contestar reconvención", "plazo_dias": 30, "tipo_plazo": "corridos", "opcional": True},
            {"etapa": "Audiencia preliminar"},
            {"etapa": "Audiencia complementaria"},
            {"etapa": "Alegatos"},
            {"etapa": "Apelación", "plazo_dias": 15, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de apelación", "plazo_dias": 15, "tipo_plazo": "hábiles", "opcional": True},
            {"etapa": "Casación", "plazo_dias": 15, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de casación", "plazo_dias": 15, "tipo_plazo": "hábiles", "opcional": True}
        ]
    elif estructura == "laboral":
        return [
            {"etapa": "Demanda"},
            {"etapa": "Contestación de demanda", "plazo_dias": 15, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar excepciones", "plazo_dias": 10, "tipo_plazo": "hábiles", "opcional": True},
            {"etapa": "Audiencia única"},
            {"etapa": "Alegatos"},
            {"etapa": "Apelación", "plazo_dias": 10, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de apelación", "plazo_dias": 10, "tipo_plazo": "hábiles", "opcional": True},
            {"etapa": "Casación", "plazo_dias": 10, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de casación", "plazo_dias": 10, "tipo_plazo": "hábiles", "opcional": True}
        ]
    elif estructura == "monitorio":
        return [
            {"etapa": "Demanda"},
            {"etapa": "Presentación de excepciones", "plazo_dias": 10, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de excepciones", "plazo_dias": 10, "tipo_plazo": "hábiles"},
            {"etapa": "Audiencia única"},
            {"etapa": "Alegatos"},
            {"etapa": "Apelación", "plazo_dias": 15, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de apelación", "plazo_dias": 15, "tipo_plazo": "hábiles", "opcional": True},
            {"etapa": "Casación", "plazo_dias": 15, "tipo_plazo": "hábiles"},
            {"etapa": "Evacuar traslado de casación", "plazo_dias": 15, "tipo_plazo": "hábiles", "opcional": True}
        ]
    elif estructura == "penal":
        return [
            {"etapa": "Audiencia de formalización"},
            {"etapa": "Medidas cautelares", "nota": "Debe ingresarse manualmente el plazo establecido por el juez"}
        ]
    else:
        raise HTTPException(status_code=404, detail="Estructura procesal no reconocida")