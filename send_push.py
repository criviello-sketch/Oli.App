import json
import os
import random

from pywebpush import webpush, WebPushException

base = os.environ["SITE_URL"].rstrip("/")
subs = json.loads(os.environ["SUBSCRIPTIONS"])
if isinstance(subs, dict):
    subs = [subs]
textos = json.load(open("docs/content.json", encoding="utf-8"))


def orden_ronda(ronda, n):
    orden = list(range(n))
    random.Random(ronda).shuffle(orden)
    return orden


# Cada ejecución de GitHub Actions tiene un número creciente.
# Con él recorremos todos los textos mezclados antes de repetir.
corrida = int(os.environ.get("GITHUB_RUN_NUMBER", "0"))
n = len(textos)
ronda, pos = divmod(corrida, n)
orden = orden_ronda(ronda, n)

# Evita que el último de la ronda anterior sea el primero de esta
if ronda > 0 and n > 1:
    ultimo_anterior = orden_ronda(ronda - 1, n)[-1]
    if orden[0] == ultimo_anterior:
        orden[0], orden[1] = orden[1], orden[0]

texto = textos[orden[pos]]

payload = json.dumps({
    "title": texto,
    "body": "",
    "image": f"{base}/drawings/peluchin.jpg",
})

for i, sub in enumerate(subs, 1):
    try:
        webpush(
            sub,
            payload,
            vapid_private_key=os.environ["VAPID_PRIVATE_KEY"],
            vapid_claims={"sub": "mailto:" + os.environ["VAPID_EMAIL"]},
        )
        print(f"Dispositivo {i}: enviado '{texto}' OK")
    except WebPushException as e:
        print(f"Dispositivo {i}: error -> {e}")
