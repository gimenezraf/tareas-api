import React, { useState, useEffect } from 'react';

function App() {
  const [tareas, setTareas] = useState([]);
  const [nuevoHistorial, setNuevoHistorial] = useState({});

  // ... otras funciones y useEffects ...

  const handleAgregarHistorial = async (tareaId) => {
    const evento = nuevoHistorial[tareaId];
    if (!evento || !evento.descripcion || !evento.fecha) return;

    const response = await fetch(`${API_URL}/tareas/${tareaId}/historial`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        descripcion: evento.descripcion,
        fecha: evento.fecha,
        etapa_procesal: evento.etapa_procesal,
        fecha_limite: evento.fecha_limite
      }),
    });

    if (response.ok) {
      // Actualizar estado, limpiar inputs, etc.
    }
  };

  return (
    <div>
      {tareas.map((tarea) => (
        <div key={tarea.id}>
          {/* Información de la tarea */}

          <div>
            {/* Historial expandido */}
            {/* ... otros campos para agregar evento al historial ... */}

            <button onClick={() => handleAgregarHistorial(tarea.id)}>
              Agregar evento al historial
            </button>

            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
              <div style={{ flex: 1 }}>
                <label>Etapa procesal:</label>
                <input
                  type="text"
                  value={nuevoHistorial[tarea.id]?.etapa_procesal || ''}
                  onChange={(e) =>
                    setNuevoHistorial((prev) => ({
                      ...prev,
                      [tarea.id]: {
                        ...prev[tarea.id],
                        etapa_procesal: e.target.value,
                      },
                    }))
                  }
                />
              </div>
              <div style={{ flex: 1 }}>
                <label>Fecha límite:</label>
                <input
                  type="date"
                  value={nuevoHistorial[tarea.id]?.fecha_limite || ''}
                  onChange={(e) =>
                    setNuevoHistorial((prev) => ({
                      ...prev,
                      [tarea.id]: {
                        ...prev[tarea.id],
                        fecha_limite: e.target.value,
                      },
                    }))
                  }
                />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;