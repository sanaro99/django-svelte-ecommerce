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

<nav class="navbar bg-base-100 shadow-md sticky top-0 z-50">
  <div class="navbar-start">
    <a href="/" class="btn btn-ghost normal-case text-xl">
      <img src="/logo.png" alt="Logo" class="h-10" />
    </a>
  </div>
  <div class="navbar-center">
    <ul class="menu menu-horizontal px-1 space-x-4">
      <li><a href="/">Products</a></li>
      <li><a href="/cart">Cart</a></li>
      <li><a href="/orders">Orders</a></li>
    </ul>
  </div>
  <div class="navbar-end">
    {#if userLoading}
      <span class="loading loading-spinner">Loading</span>
    {:else if user}
      <div class="dropdown dropdown-end">
        <button class="btn btn-ghost normal-case flex items-center gap-1" aria-haspopup="true">
          {user.username}
          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.585l3.71-3.355a.75.75 0 111.02 1.1l-4.25 3.845a.75.75 0 01-1.02 0l-4.25-3.845a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
          </svg>
        </button>
        <ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
          <li><span class="px-4 py-2 text-sm">{user.first_name} {user.last_name}</span></li>
          <li><span class="px-4 py-2 text-sm">{user.username}</span></li>
          <li><span class="px-4 py-2 text-sm">{user.email}</span></li>
          <li><hr class="border-t my-1"/></li>
          <li><a href="/edit-account">Edit Account</a></li>
          <li><button on:click={handleLogout} class="text-red-600 w-full text-left">Logout</button></li>
        </ul>
      </div>
    {:else}
      <button on:click={() => window.location.href = '/login'} class="btn btn-ghost">Login</button>
      <button on:click={() => window.location.href = '/register'} class="btn btn-ghost">Register</button>
    {/if}
    <!-- theme toggle -->
    <label class="toggle text-base-content">
      <input type="checkbox" data-toggle-theme="cupcake,halloween" />
      <span class="swap-on">🌙</span>
      <span class="swap-off">☀️</span>
    </label>
  </div>
</nav>

<main class="flex-1">
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <slot />
  </div>
</main>
