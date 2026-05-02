/**
 * API Client — all fetch calls to FastAPI backend.
 * Locally: Vite proxy routes /api/* to http://localhost:8000
 * Production: VITE_API_URL routes to Render deployed backend.
 */

const BASE = import.meta.env.VITE_API_URL || '';

// ─── Products ──────────────────────────────────────────

export async function fetchProviders() {
  const res = await fetch(`${BASE}/api/providers`);
  if (!res.ok) throw new Error('Failed to fetch providers');
  return await res.json();
}

export async function fetchProducts() {
  const res = await fetch(`${BASE}/api/products`);
  if (!res.ok) throw new Error('Failed to fetch products');
  return (await res.json()).products;
}

export async function fetchSkus(product) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/skus`);
  if (!res.ok) throw new Error('Failed to fetch SKUs');
  return await res.json();
}

export async function fetchPoses(product) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/poses`);
  if (!res.ok) throw new Error('Failed to fetch poses');
  return await res.json();
}

export async function fetchPrompts(product) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/prompts`);
  if (!res.ok) throw new Error('Failed to fetch prompts');
  return await res.json();
}

export async function fetchSkuImages(product, sku) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/sku/${encodeURIComponent(sku)}/images`);
  if (!res.ok) throw new Error('Failed to fetch SKU images');
  return await res.json();
}

// ─── Reference Image ──────────────────────────────────

export async function uploadReferenceImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${BASE}/api/upload/reference`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error('Failed to upload reference image');
  return await res.json();
}

export async function analyzeReference(imagePath) {
  const formData = new FormData();
  formData.append('image_path', imagePath);
  const res = await fetch(`${BASE}/api/analyze-reference`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error('Reference analysis failed');
  return await res.json();
}

// ─── Generation ───────────────────────────────────────

export async function startFrontGeneration(params) {
  const res = await fetch(`${BASE}/api/generate/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error('Failed to start generation');
  return await res.json();
}

export async function saveFrontImage(product, sku, imageBase64) {
  const res = await fetch(`${BASE}/api/generate/save-front`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product, sku, image_data: imageBase64 }),
  });
  if (!res.ok) throw new Error('Failed to save front image');
  return await res.json();
}

export async function startVariantGeneration(params) {
  const res = await fetch(`${BASE}/api/generate/save-and-variants`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error('Failed to start variant generation');
  return await res.json();
}

export async function cancelGeneration(jobId) {
  const res = await fetch(`${BASE}/api/generate/cancel/${jobId}`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to cancel');
  return await res.json();
}

// ─── SSE Stream ───────────────────────────────────────

export function subscribeToJob(jobId, onEvent) {
  const evtSource = new EventSource(`${BASE}/api/generate/stream/${jobId}`);
  
  evtSource.onmessage = (e) => {
    try {
      const event = JSON.parse(e.data);
      onEvent(event);
      
      if (['done', 'error', 'cancelled'].includes(event.type)) {
        evtSource.close();
      }
    } catch (err) {
      console.error('SSE parse error:', err);
    }
  };
  
  evtSource.onerror = () => {
    evtSource.close();
    onEvent({ type: 'error', data: { message: 'Connection lost' } });
  };
  
  return evtSource;  // return so caller can close it
}

// ─── Auto-Tune ────────────────────────────────────────

export async function autoTunePrompts(product) {
  const res = await fetch(`${BASE}/api/auto-tune`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Auto-tune failed');
  }
  return await res.json();
}

// ─── Product Management ───────────────────────────────

export async function createProduct(name, category, initialColor) {
  const res = await fetch(`${BASE}/api/products`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, category, initial_color: initialColor }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to create product');
  }
  return await res.json();
}

export async function createSku(product, color) {
  const formData = new FormData();
  formData.append('color', color);
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/skus`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to create SKU');
  }
  return await res.json();
}

export async function uploadSkuImage(product, sku, imageType, file) {
  const formData = new FormData();
  formData.append('image_type', imageType);
  formData.append('file', file);
  const res = await fetch(
    `${BASE}/api/products/${encodeURIComponent(product)}/${encodeURIComponent(sku)}/upload`,
    { method: 'POST', body: formData }
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to upload image');
  }
  return await res.json();
}

export async function savePrompts(product, masterPrompt, variants) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}/prompts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ master_prompt: masterPrompt, variants }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to save prompts');
  }
  return await res.json();
}

export async function deleteProduct(product) {
  const res = await fetch(`${BASE}/api/products/${encodeURIComponent(product)}`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to delete product');
  }
  return await res.json();
}

export async function deleteSku(product, sku) {
  const res = await fetch(
    `${BASE}/api/products/${encodeURIComponent(product)}/skus/${encodeURIComponent(sku)}`,
    { method: 'DELETE' }
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to delete SKU');
  }
  return await res.json();
}

// ─── Download ─────────────────────────────────────────

export function getDownloadZipUrl(product, folder) {
  return `${BASE}/api/download/${encodeURIComponent(product)}/${encodeURIComponent(folder)}`;
}
