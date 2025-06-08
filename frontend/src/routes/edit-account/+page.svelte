<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchCurrentUser, updateUser } from '$lib/api';

  let username = '';
  let email = '';
  let firstName = '';
  let lastName = '';
  let phone = '';
  let streetAddress = '';
  let city = '';
  let state = '';
  let postalCode = '';
  let country = '';
  let message = '';
  let messageType = ''; // 'success' or 'error'

  onMount(async () => {
    try {
      const user = await fetchCurrentUser();
      username = user?.username || '';
      email = user?.email || '';
      firstName = user?.first_name || '';
      lastName = user?.last_name || '';
      phone = user?.phone || '';
      streetAddress = user?.street_address || '';
      city = user?.city || '';
      state = user?.state || '';
      postalCode = user?.postal_code || '';
      country = user?.country || '';
    } catch (e) {
      console.error(e);
    }
  });

  async function handleSubmit() {
    message = '';
    messageType = '';
    try {
      await updateUser({
        username,
        email,
        first_name: firstName,
        last_name: lastName,
        phone,
        street_address: streetAddress,
        city,
        state,
        postal_code: postalCode,
        country
      });
      message = 'Profile updated successfully.';
      messageType = 'success';
    } catch (err: any) {
      message = err.message;
      messageType = 'error';
    }
  }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Edit Account</h2>
  </div>
  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-3xl sm:px-10">
      <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <div class="mt-1">
            <input id="username" type="text" bind:value={username} required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <div class="mt-1">
            <input id="email" type="email" bind:value={email} required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
          <div class="mt-1">
            <input id="firstName" type="text" bind:value={firstName} required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
          <div class="mt-1">
            <input id="lastName" type="text" bind:value={lastName} required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700">Phone</label>
          <div class="mt-1">
            <input id="phone" type="text" bind:value={phone} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="streetAddress" class="block text-sm font-medium text-gray-700">Street Address</label>
          <div class="mt-1">
            <input id="streetAddress" name="street_address" type="text" bind:value={streetAddress} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="city" class="block text-sm font-medium text-gray-700">City</label>
          <div class="mt-1">
            <input id="city" type="text" bind:value={city} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="state" class="block text-sm font-medium text-gray-700">State</label>
          <div class="mt-1">
            <input id="state" type="text" bind:value={state} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="postalCode" class="block text-sm font-medium text-gray-700">Postal Code</label>
          <div class="mt-1">
            <input id="postalCode" name="postal_code" type="text" bind:value={postalCode} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <label for="country" class="block text-sm font-medium text-gray-700">Country</label>
          <div class="mt-1">
            <input id="country" type="text" bind:value={country} class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-3xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
        </div>
        <div>
          <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-3xl shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Save Changes</button>
        </div>
      </form>
      {#if message}
        <div class="mt-6">
          <div class="rounded-3xl {messageType === 'success' ? 'bg-green-50 p-4' : 'bg-red-50 p-4'}">
            <div class="flex">
              <div class="flex-shrink-0">
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
                <p class="text-sm font-medium {messageType === 'success' ? 'text-green-800' : 'text-red-800'}">{message}</p>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>