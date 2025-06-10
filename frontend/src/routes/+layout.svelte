<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { fetchCurrentUser, logout } from '$lib/api';
  import { BACKEND_BASE_URL } from '$lib/api';
  import { FRONTEND_BASE_URL } from '$lib/api';
  import { themeChange } from 'theme-change';
  let user: any = null;
  let userLoading = true;

  onMount(async () => {
    try { user = await fetchCurrentUser(); } catch { } finally { userLoading = false; }
  });
  onMount(() => themeChange(false));

  function handleLogout() {
    // Clear local tokens and redirect to backend logout to clear session
    logout();
    window.location.href = `${BACKEND_BASE_URL}/accounts/logout/?next=${FRONTEND_BASE_URL}/login`;
  }
</script>

<nav class="navbar bg-base-100 shadow-sm">
  <div class="flex-1">
    <a href="/" class="btn btn-ghost text-xl">
      EShop
    </a>
  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <li><a href="/">Products</a></li>
      <li><a href="/cart">Cart</a></li>
      <li><a href="/orders">Orders</a></li>
      {#if userLoading}
        <li><span class="loading loading-spinner" aria-label="Loading">Loading</span></li>
      {:else if user}
        <li>
          <details>
            <summary>
              {user.username}
            </summary>
            <ul class="bg-base-100 rounded-t-none p-2">
              <li><a class="disabled">{user.first_name} {user.last_name}</a></li>
              <li><a class="disabled">{user.username}</a></li>
              <li><a class="disabled">{user.email}</a></li>
              <li><a href="/edit-account">Edit Account</a></li>
              <li><button on:click={handleLogout} class="text-red-600">Logout</button></li>
            </ul>
          </details>
        </li>
      {:else}
        <li><button on:click={() => window.location.href = '/login'} class="btn btn-ghost">Login</button></li>
        <li><button on:click={() => window.location.href = '/register'} class="btn btn-ghost">Register</button></li>
      {/if}
      <label class="swap swap-rotate">
        <input type="checkbox" data-toggle-theme="cupcake,halloween" aria-label="Toggle Theme" />
        <span class="swap-on">🌙</span>
        <span class="swap-off">☀️</span>
      </label>
    </ul>
  </div>
</nav>

<main class="flex-1">
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <slot />
  </div>
</main>
