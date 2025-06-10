<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchOrders, fetchCurrentUser } from '$lib/api';
  import { goto } from '$app/navigation';
  import OrderCard from '$lib/components/OrderCard.svelte';

  let orders: any[] = [];
  let loading = true;
  let error = '';
  let statusFilter = '';
  let monthsFilter = 0;
  const statuses = ['pending','paid','shipped','completed','cancelled'];

  // pagination state
  let page = 1;
  let next: string | null = null;
  let loadingMore = false;
  let token: string | undefined;

  function capitalize(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  $: selectedStatusName = statusFilter ? capitalize(statusFilter) : 'All Statuses';

  async function loadOrders() {
    loading = true;
    error = '';
    page = 1;
    let createdAfter: string | undefined;
    if (monthsFilter > 0) {
      const d = new Date();
      d.setMonth(d.getMonth() - monthsFilter);
      createdAfter = d.toISOString();
    }
    try {
      const data = await fetchOrders(page, statusFilter || undefined, createdAfter, token);
      orders = data.results;
      next = data.next;
    } catch (e: any) {
      error = e.message;
    }
    loading = false;
  }

  // load more orders
  async function loadMoreOrders() {
    if (!next) return;
    loadingMore = true;
    let createdAfter: string | undefined;
    if (monthsFilter > 0) {
      const d = new Date();
      d.setMonth(d.getMonth() - monthsFilter);
      createdAfter = d.toISOString();
    }
    try {
      // bump page number and use numeric paging to avoid mixed-content error
      page += 1;
      const data = await fetchOrders(page, statusFilter || undefined, createdAfter, token);
      orders = [...orders, ...data.results];
      next = data.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loadingMore = false;
    }
  }

  // infinite scroll handler
  function handleScroll() {
    if (typeof window === 'undefined' || loadingMore || !next) return;
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
      loadMoreOrders();
    }
  }

  onMount(async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      goto('/login');
      return;
    }
    const t = localStorage.getItem('access_token');
    token = t ?? undefined;
    await loadOrders();
  });

  // register scroll listener
  onMount(() => {
    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', handleScroll);
    }
  });
  onDestroy(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('scroll', handleScroll);
    }
  });
</script>

<div class="p-6 max-w-4xl mx-auto">
  <h2 class="text-2xl font-bold mb-4">Your Orders</h2>
  <!-- Filters -->
  <div class="flex flex-wrap gap-4 mb-4">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn m-1">{selectedStatusName}</div>
      <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
        <li on:click={() => { statusFilter = ''; loadOrders(); }}><a>All Statuses</a></li>
        {#each statuses as s}
          <li on:click={() => { statusFilter = s; loadOrders(); }}><a>{capitalize(s)}</a></li>
        {/each}
      </ul>
    </div>
    <label class="inline-flex items-center">
      <span class="mr-2">Last</span>
      <input type="number" min="0" bind:value={monthsFilter} on:change={loadOrders} class="w-16 px-2 py-1 border rounded-3xl" />
      <span class="ml-2">months</span>
    </label>
  </div>
  {#if loading}
    <p>Loading orders...</p>
  {:else}
    {#if error}
      <p class="text-red-600 mb-4">{error}</p>
    {:else if orders.length === 0}
      <p>You have no orders. <a href="/" class="text-indigo-600 hover:underline">Start shopping</a>.</p>
    {:else}
      <div class="space-y-6">
        {#each orders as order}
          <OrderCard {order} />
        {/each}
      </div>
      {#if next}
        <div class="text-center py-4 space-x-2">
          {#if loadingMore}
            <button class="btn btn-square" disabled>
              <span class="loading loading-spinner"></span>
            </button>
            <button class="btn" disabled>
              <span class="loading loading-spinner"></span>
              loading
            </button>
          {:else}
            <button class="btn btn-outline" on:click={loadMoreOrders}>
              Load more orders
            </button>
          {/if}
        </div>
      {/if}
    {/if}
  {/if}
</div>