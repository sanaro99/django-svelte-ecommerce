<script>
  let username = '';
  let email = '';
  let password = '';
  let password2 = '';
  let message = '';
  let messageType = ''; // 'success' or 'error'

  async function handleSubmit() {
    if (password !== password2) {
      message = 'Passwords do not match.';
      messageType = 'error';
      return;
    }

    const userData = {
      username,
      email,
      password,
      password2
    };

    try {
      const response = await fetch('http://localhost:8000/accounts/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }, 
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        message = data.message || 'Registration successful! Please login.';
        messageType = 'success';
        // Optionally, redirect to login page or clear form
        username = '';
        email = '';
        password = '';
        password2 = '';
      } else {
        // Attempt to construct a more detailed error message
        let errorDetail = '';
        if (data.username) errorDetail += `Username: ${data.username.join(' ')} `;
        if (data.email) errorDetail += `Email: ${data.email.join(' ')} `;
        if (data.password) errorDetail += `Password: ${data.password.join(' ')} `;
        if (data.non_field_errors) errorDetail += `${data.non_field_errors.join(' ')} `;
        
        message = errorDetail || data.message || 'Registration failed. Please try again.';
        messageType = 'error';
      }
    } catch (error) {
      console.error('Registration error:', error);
      message = 'An error occurred during registration. Please try again.';
      messageType = 'error';
    }
  }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Create your account
    </h2>
  </div>

  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            Username
          </label>
          <div class="mt-1">
            <input id="username" name="username" type="text" bind:value={username} required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <div class="mt-1">
            <input id="email" name="email" type="email" bind:value={email} autocomplete="email" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Password
          </label>
          <div class="mt-1">
            <input id="password" name="password" type="password" bind:value={password} autocomplete="new-password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <label for="password2" class="block text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <div class="mt-1">
            <input id="password2" name="password2" type="password" bind:value={password2} autocomplete="new-password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Register
          </button>
        </div>
      </form>

      {#if message}
        <div class="mt-6">
          <div class="rounded-md {messageType === 'success' ? 'bg-green-50 p-4' : 'bg-red-50 p-4'}">
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
