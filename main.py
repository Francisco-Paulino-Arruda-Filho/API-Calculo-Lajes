from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="API Cálculo de Lajes")

class LajeInput(BaseModel):
    a: float  # lado a (m)
    b: float  # lado b (m)
    h: float  # espessura (m)
    p: float  # carga distribuída (kN/m²)
    e: float  # módulo de elasticidade
    v: float  # coeficiente de poisson


def calcular_laje(data: LajeInput):
    a, b, h, p, e, v = data.a, data.b, data.h, data.p, data.e, data.v

    x = a / 2
    y = b / 2

    D = (e * (h**3)) / (12 * (1 - v**2))

    N = 15
    w = Mx = My = Mxy = 0

    for m in range(1, N+1, 2):
        for n in range(1, N+1, 2):
            termo = (m/a)**2 + (n/b)**2

            seno = np.sin(m*np.pi*x/a) * np.sin(n*np.pi*y/b)
            cosseno = np.cos(m*np.pi*x/a) * np.cos(n*np.pi*y/b)

            w += (16*p)/(D*np.pi**6) * (seno/(m*n*termo**2))

            My += (16*p)/(np.pi**4) * (
                ((m/a)**2 + v*(n/b)**2)/(m*n*termo**2)
            ) * seno

            Mx += (16*p)/(np.pi**4) * (
                (v*(m/a)**2 + (n/b)**2)/(m*n*termo**2)
            ) * seno

            Mxy += -(16*(1-v)*p)/(np.pi**4*a*b) * (cosseno/termo**2)

    return {
        "flecha_maxima": w,
        "Mx": Mx,
        "My": My,
        "Mxy": Mxy,
        "rigidez_D": D
    }


@app.post("/calcular-laje")
def calcular(data: LajeInput):
    resultado = calcular_laje(data)
    return resultado