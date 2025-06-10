<script lang="ts">
  import { BACKEND_BASE_URL } from '$lib/api';
  let username = '';
  let email = '';
  let firstName = '';
  let lastName = '';
  let password = '';
  let password2 = '';
  let message = '';
  let messageType = ''; // 'success' or 'error'

  async function handleSubmit() {
    // Clear any previous message
    message = '';
    messageType = '';

    if (password !== password2) {
      message = 'Passwords do not match.';
      messageType = 'error';
      return;
    }

    const userData = { username, email, password, password2, first_name: firstName, last_name: lastName };
    let res: Response;
    let data: any;

    try {
      res = await fetch(`${BACKEND_BASE_URL}/accounts/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });
    } catch (networkError: any) {
      console.error('Network error during registration:', networkError);
      message = networkError.message || 'Network error. Please try again.';
      messageType = 'error';
      return;
    }

    // Attempt to parse JSON; fallback if invalid
    try {
      data = await res.json();
    } catch (parseError) {
      console.error('Invalid JSON response:', parseError);
      message = `Server error (${res.status}). Please try again.`;
      messageType = 'error';
      return;
    }

    if (res.ok) {
      message = data.message || 'Registration successful! Please login.';
      messageType = 'success';
      // Clear form
      username = '';
      email = '';
      firstName = '';
      lastName = '';
      password = '';
      password2 = '';
    } else {
      // Build error detail from backend fields
      let errorDetail = '';
      if (data.error) errorDetail += `${data.error} `;
      for (const key in data) {
        if (Array.isArray(data[key])) {
          errorDetail += `${key}: ${data[key].join(' ')} `;
        }
      }
      message = errorDetail.trim() || `Error ${res.status}: ${res.statusText}`;
      messageType = 'error';
    }
  }
</script>

<div class="container mx-auto">
  <div class="card rounded-3xl shadow-xl max-w-xl mx-auto">
    <div class="card-body">
      <div class="mt-6 text-3xl text-center font-extrabold">
        Create your account
      </div>
      <form class="space-y-4" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="username">
            Username
          </label>
          <div class="mt-1">
            <input id="username" name="username" type="text" bind:value={username} required class="input w-full">
          </div>
        </div>

        <div>
          <label for="email">
            Email address
          </label>
          <div class="mt-1">
            <input id="email" name="email" type="email" bind:value={email} autocomplete="email" required class="input w-full">
          </div>
        </div>

        <div>
          <label for="firstName">
            First Name
          </label>
          <div class="mt-1">
            <input id="firstName" name="first_name" type="text" bind:value={firstName} required class="input w-full">
          </div>
        </div>

        <div>
          <label for="lastName">
            Last Name
          </label>
          <div class="mt-1">
            <input id="lastName" name="last_name" type="text" bind:value={lastName} required class="input w-full">
          </div>
        </div>

        <div>
          <label for="password">
            Password
          </label>
          <div class="mt-1">
            <input id="password" name="password" type="password" bind:value={password} autocomplete="new-password" required class="input w-full">
          </div>
        </div>

        <div>
          <label for="password2">
            Confirm Password
          </label>
          <div class="mt-1">
            <input id="password2" name="password2" type="password" bind:value={password2} autocomplete="new-password" required class="input w-full">
          </div>
        </div>

        <div>
          <button type="submit" class="w-full btn btn-primary rounded-3xl my-4">
            Register
          </button>
        </div>
      </form>

      {#if message}
        <div class="mt-6">
          <div class="rounded-3xl {messageType === 'success' ? 'bg-green-50 p-4' : 'bg-red-50 p-4'}">
            <div class="flex">
              <div class="flex-shrink-0">
                <!-- Heroicon name: solid/check-circle for success, solid/x-circle for error -->
                {#if messageType === 'success'}
                  <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                {:else}
                  <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                {/if}
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium {messageType === 'success' ? 'text-green-800' : 'text-red-800'}">
                  {message}
                </p>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
</div>

</div>