<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { fetchCurrentUser, logout } from '$lib/api';
  import { BACKEND_BASE_URL } from '$lib/api';
  import { FRONTEND_BASE_URL } from '$lib/api';
  let user: any = null;
  let userLoading = true;
  let dropdownOpen = false;

  onMount(async () => {
    try { user = await fetchCurrentUser(); } catch { } finally { userLoading = false; }
  });

  function handleLogout() {
    // Clear local tokens and redirect to backend logout to clear session
    logout();
    window.location.href = `${BACKEND_BASE_URL}/accounts/logout/?next=${FRONTEND_BASE_URL}/login`;
  }
</script>

<nav class="bg-white shadow-md">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
    <div class="flex items-center">
      <img src="/logo.png" alt="Logo" class="h-10 w-32 mr-2" />
    </div>
    <div class="flex items-center space-x-4">
      {#if userLoading}
        <span class="text-gray-500">Loading...</span>
      {:else if user}
        <a href="/" class="px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">Products</a>
        <a href="/cart" class="px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">Cart</a>
        <a href="/orders" class="px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">Orders</a>
        <div class="relative">
          <button on:click={() => dropdownOpen = !dropdownOpen}
            class="flex items-center px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">
            {user.username}
            <svg class="ml-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.585l3.71-3.355a.75.75 0 111.02 1.1l-4.25 3.845a.75.75 0 01-1.02 0l-4.25-3.845a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
            </svg>
          </button>
          {#if dropdownOpen}
            <div class="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-3xl py-2 z-20">
              <div class="px-4 py-2 text-sm text-gray-700">{user.username}</div>
              <div class="px-4 py-2 text-sm text-gray-500">{user.email}</div>
              <div class="border-t my-1"></div>
              <button on:click={handleLogout}
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">Logout</button>
            </div>
          {/if}
        </div>
      {:else}
        <button on:click={() => window.location.href = '/login'} class="px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">Login</button>
        <button on:click={() => window.location.href = '/register'} class="px-3 py-2 rounded-3xl text-gray-700 hover:bg-gray-100 hover:text-indigo-600">Register</button>
      {/if}
    </div>
  </div>
</nav>

<main class="min-h-screen bg-gray-100">
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <slot />
  </div>
</main>
