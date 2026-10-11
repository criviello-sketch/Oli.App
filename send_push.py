import json
import os
import random

from pywebpush import webpush, WebPushException

base = os.environ["SITE_URL"].rstrip("/")
subs = json.loads(os.environ["SUBSCRIPTIONS"])
if isinstance(subs, dict):
    subs = [subs]
textos = json.load(open("docs/content.json", encoding="utf-8"))

texto = random.choice(textos)
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
