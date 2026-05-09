const API_BASE = import.meta.env.VITE_FRONTEND_API_BASE_URL || 'http://localhost:8000';

const defaultHeaders = { 'Content-Type': 'application/json' };

async function fetchWithRetry(url, options, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        let errMessage = 'API Error';
        try {
          const errData = await response.json();
          errMessage = errData.detail || errMessage;
        } catch {}
        throw new Error(errMessage);
      }
      return await response.json();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise((res) => setTimeout(res, 300 * Math.pow(2, i)));
    }
  }
}

export const api = {
  checkHealth: () => fetchWithRetry(`${API_BASE}/health`, { method: 'GET' }),
  stage1Assess: (responses) => fetchWithRetry(`${API_BASE}/stage1/assess`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify({ responses }),
  }),
  stage2Assess: (response, imageId) => fetchWithRetry(`${API_BASE}/stage2/assess`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify({ response, image_id: imageId }),
  }),
  stage3Assess: (responses) => fetchWithRetry(`${API_BASE}/stage3/assess`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify({ responses }),
  }),
  finalAssess: (stage1, stage2, stage3) => fetchWithRetry(`${API_BASE}/assessment/final`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify({
      stage1_results: stage1,
      stage2_results: stage2,
      stage3_results: stage3,
    }),
  }),
};
