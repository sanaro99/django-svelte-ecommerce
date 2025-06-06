<script lang="ts">
  import { onMount } from 'svelte';

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const code_verifier = sessionStorage.getItem('pkce_code_verifier');

    if (code && code_verifier) {
      // Exchange code for token
      const res = await fetch("http://localhost:8000/o/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          grant_type: "authorization_code",
          code,
          redirect_uri: "http://localhost:5173/auth/callback",
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
    }
  });
</script>

<p>Authorizing…</p>