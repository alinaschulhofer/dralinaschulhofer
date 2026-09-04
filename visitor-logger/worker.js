// Cloudflare Worker — visitor IP logger
// Deploy this at: https://dash.cloudflare.com → Workers & Pages → Create Worker
// Set the environment variable APPS_SCRIPT_URL to your Google Apps Script web app URL

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET',
        },
      });
    }

    const ip        = request.headers.get('CF-Connecting-IP') || 'unknown';
    const ua        = request.headers.get('User-Agent') || '';
    const country   = (request.cf && request.cf.country) || '';
    const city      = (request.cf && request.cf.city) || '';
    const url       = new URL(request.url);
    const page      = url.searchParams.get('page') || '/';
    const ref       = url.searchParams.get('ref') || '';
    const timestamp = new Date().toISOString();

    try {
      await fetch(env.APPS_SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ timestamp, ip, country, city, page, ref, ua }),
      });
    } catch (err) {
      // Fail silently — never break the visitor's page load
    }

    return new Response('ok', {
      headers: { 'Access-Control-Allow-Origin': '*' },
    });
  },
};
