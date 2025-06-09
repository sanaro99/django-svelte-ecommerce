<script lang="ts">
  import { FRONTEND_BASE_URL, BACKEND_BASE_URL } from '$lib/api';
  import { onMount } from 'svelte';
  let errorMessage = '';

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const err = urlParams.get('error');
    if (err) {
      errorMessage = err.replace(/_/g, ' ');
      return;
    }
    const code = urlParams.get('code');
    const code_verifier = sessionStorage.getItem('pkce_code_verifier');

    if (code && code_verifier) {
      // Exchange code for token
      const res = await fetch(`${BACKEND_BASE_URL}/o/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          grant_type: "authorization_code",
          code,
          redirect_uri: `${FRONTEND_BASE_URL}/auth/callback`,
          client_id: import.meta.env.VITE_CLIENT_ID,
          code_verifier: code_verifier
        })
      });

      if (res.ok) {
        const tokens = await res.json();
        localStorage.setItem("access_token", tokens.access_token);
        // (Optional) localStorage.setItem("refresh_token", tokens.refresh_token);
        window.location.href = "/"; // Redirect to homepage or dashboard
      } else {
        // Handle error
        console.error(await res.text());
      }
    } else {
      // No code/verifier; do nothing
    }
  });
</script>

{#if errorMessage}
  <div class="min-h-screen flex items-center justify-center bg-gray-100 p-4">
    <div class="p-6 rounded-3xl shadow-md text-center">
      <h2 class="text-xl font-semibold text-red-600 mb-2">Authorization Error</h2>
      <p class="text-gray-700">{errorMessage}</p>
      <button on:click={() => window.location.href = '/'} class="mt-4 inline-block px-4 py-2 text-white rounded-3xl">Go Home</button>
    </div>
  </div>
{:else}
  <p class="min-h-screen flex items-center justify-center">Authorizing…</p>
{/if}