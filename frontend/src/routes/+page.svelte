<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchProducts, fetchCurrentUser, logout } from '$lib/api';

  let products = [];
  let loading = true;
  let error = '';
  let user = { username: '', email: '' };
  let userLoading = true;
  let userError = '';

  onMount(async () => {
    try {
      const u = await fetchCurrentUser();
      user = u;
    } catch (e: any) {
      userError = e.message;
    } finally {
      userLoading = false;
    }

    try {
      const res = await fetchProducts();
      products = res.results;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function handleLogout() {
    logout();
    window.location.href = '/login';
  }
</script>

<div class="min-h-screen bg-gray-100">
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <h1 class="text-2xl font-bold text-gray-900">Products</h1>
        </div>
        <div class="flex items-center space-x-4">
          {#if userLoading}
            <p class="text-gray-500">Loading user...</p>
          {:else if userError}
            <a href="/login" class="text-indigo-600 hover:text-indigo-800">Login</a>
          {:else}
            <p class="text-gray-700">Welcome, {user.username} ({user.email})</p>
            <button on:click={handleLogout} class="text-red-600 hover:text-red-800">Logout</button>
          {/if}
        </div>
      </div>
    </div>
  </nav>

  <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    {#if loading}
      <p class="text-gray-600">Loading…</p>
    {:else if error}
      <p class="text-red-600">{error}</p>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each products as product}
          <div class="bg-white shadow rounded-lg p-4">
            <a href={`/products/${product.slug}`} class="text-lg font-medium text-indigo-600 hover:underline">
              {product.name}
            </a>
            <p class="text-gray-500 mt-1">${product.price}</p>
          </div>
        {/each}
      </div>
    {/if}
  </main>
</div>