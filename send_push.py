import json
import os
import random

from pywebpush import webpush, WebPushException

base = os.environ["SITE_URL"].rstrip("/")
subs = json.loads(os.environ["SUBSCRIPTIONS"])
if isinstance(subs, dict):
    subs = [subs]
items = json.load(open("docs/content.json", encoding="utf-8"))

item = random.choice(items)
payload = json.dumps({
    "title": item["titulo"],
    "body": item["texto"],
    "image": f"{base}/drawings/{item['imagen']}",
})

for i, sub in enumerate(subs, 1):
    try:
        webpush(
            sub,
            payload,
            vapid_private_key=os.environ["VAPID_PRIVATE_KEY"],
            vapid_claims={"sub": "mailto:" + os.environ["VAPID_EMAIL"]},
        )
        print(f"Dispositivo {i}: enviado OK")
    except WebPushException as e:
        print(f"Dispositivo {i}: error -> {e}")
