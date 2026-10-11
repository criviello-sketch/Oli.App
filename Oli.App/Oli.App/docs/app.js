const PUBLIC_KEY = "BHTusDJkw7Y_SRf_PUaUKLmXQKdQkkcTECP6yWEUACyzZrSEgsu2thAwrSXNRTO4mqlZFUWXf4kUazy14xsllVA";

const estado = document.getElementById("estado");

function b64ToUint8(b64) {
  const pad = "=".repeat((4 - (b64.length % 4)) % 4);
  const raw = atob((b64 + pad).replace(/-/g, "+").replace(/_/g, "/"));
  return Uint8Array.from([...raw].map(c => c.charCodeAt(0)));
}

document.getElementById("activar").onclick = async () => {
  try {
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
      estado.textContent = "Este navegador no soporta notificaciones push.";
      return;
    }
    const permiso = await Notification.requestPermission();
    if (permiso !== "granted") {
      estado.textContent = "Permiso denegado. Habilitalo en los ajustes del sitio.";
      return;
    }
    const reg = await navigator.serviceWorker.register("sw.js");
    await navigator.serviceWorker.ready;
    let sub = await reg.pushManager.getSubscription();
    if (!sub) {
      sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: b64ToUint8(PUBLIC_KEY),
      });
    }
    document.getElementById("sub").value = JSON.stringify(sub);
    document.getElementById("codigo").classList.remove("oculto");
    estado.textContent = "¡Listo! Notificaciones activadas en este dispositivo.";
  } catch (e) {
    estado.textContent = "Error: " + e.message;
  }
};

document.getElementById("copiar").onclick = async () => {
  const t = document.getElementById("sub");
  t.select();
  try { await navigator.clipboard.writeText(t.value); estado.textContent = "Código copiado."; }
  catch { document.execCommand("copy"); }
};
