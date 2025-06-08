<script lang="ts">
  import { BACKEND_BASE_URL } from '$lib/api';
  import { FRONTEND_BASE_URL } from '$lib/api';
  import pkceChallenge from "pkce-challenge";

  let error = "";

  async function handleLogin(event: Event) {
    event.preventDefault();

    // 1. Generate PKCE values
    const pkceValues = await pkceChallenge();
    // console.log('PKCE Values:', pkceValues);
    const { code_verifier, code_challenge } = pkceValues;
    // console.log('Code Verifier:', code_verifier);
    // console.log('Code Challenge:', code_challenge);

    // 2. Store the code_verifier (needed after redirect)
    sessionStorage.setItem("pkce_code_verifier", code_verifier);

    // 3. Build params for Django OAuth2 /o/authorize/
    const params = new URLSearchParams({
      client_id: import.meta.env.VITE_CLIENT_ID,
      response_type: "code",
      redirect_uri: `${FRONTEND_BASE_URL}/auth/callback`, // must match Django app config
      scope: "read:products read:orders read:customers read:cart write:orders write:customers write:cart",
      code_challenge: code_challenge,
      code_challenge_method: "S256"
    });

    // 4. Redirect to Django OAuth2 authorize
    window.location.href = `${BACKEND_BASE_URL}/o/authorize/?${params.toString()}`;
  }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Sign in to your account
    </h2>
  </div>

  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-3xl sm:px-10">
      <form class="space-y-6" on:submit|preventDefault={handleLogin}>
        <div>
          <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-3xl shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Login with your account (OAuth2)
          </button>
        </div>
      </form>

      {#if error}
        <div class="mt-6">
          <div class="rounded-3xl bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <!-- Heroicon name: solid/x-circle -->
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">
                  {error}
                </p>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>