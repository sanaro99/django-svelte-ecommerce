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

<div class="container mx-auto max-w-xl">
  <div class="card shadow-xl rounded-3xl">
    <div class="card-body">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">Edit Account</h2>
      <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <div class="mt-1">
            <input id="username" type="text" bind:value={username} required class="input w-full" disabled />
          </div>
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <div class="mt-1">
            <input id="email" type="email" bind:value={email} required class="input w-full" disabled />
          </div>
        </div>
        <div>
          <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
          <div class="mt-1">
            <input id="firstName" type="text" bind:value={firstName} required class="input w-full" />
          </div>
        </div>
        <div>
          <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
          <div class="mt-1">
            <input id="lastName" type="text" bind:value={lastName} required class="input w-full" />
          </div>
        </div>
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700">Phone</label>
          <div class="mt-1">
            <input id="phone" type="text" bind:value={phone} class="input w-full" />
          </div>
        </div>
        <div>
          <label for="streetAddress" class="block text-sm font-medium text-gray-700">Street Address</label>
          <div class="mt-1">
            <input id="streetAddress" name="street_address" type="text" bind:value={streetAddress} class="input w-full" />
          </div>
        </div>
        <div>
          <label for="city" class="block text-sm font-medium text-gray-700">City</label>
          <div class="mt-1">
            <input id="city" type="text" bind:value={city} class="input w-full" />
          </div>
        </div>
        <div>
          <label for="state" class="block text-sm font-medium text-gray-700">State</label>
          <div class="mt-1">
            <input id="state" type="text" bind:value={state} class="input w-full" />
          </div>
        </div>
        <div>
          <label for="postalCode" class="block text-sm font-medium text-gray-700">Postal Code</label>
          <div class="mt-1">
            <input id="postalCode" name="postal_code" type="number" bind:value={postalCode} class="input w-full" />
          </div>
        </div>
        <div>
          <label for="country" class="block text-sm font-medium text-gray-700">Country</label>
          <div class="mt-1">
            <input id="country" type="text" bind:value={country} class="input w-full" />
          </div>
        </div>
        <div>
          <button type="submit" class="btn btn-primary w-full">Save Changes</button>
        </div>
      </form>
      {#if message}
        <div role="alert" class="my-4 alert rounded-3xl {messageType === 'success' ? 'alert-success' : 'alert-error'}">
          {#if messageType === 'success'}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          {/if}
          <span>{message}</span>
        </div>
      {/if}
    </div>
  </div>
</div>