<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchOrders, fetchCurrentUser } from '$lib/api';
  import { goto } from '$app/navigation';

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
    <select bind:value={statusFilter} on:change={loadOrders} class="px-3 py-2 border rounded-3xl pr-10">
      <option value=''>All Statuses</option>
      {#each statuses as s}
        <option value={s}>{capitalize(s)}</option>
      {/each}
    </select>
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
          <div class="bg-white shadow p-4 rounded-3xl">
            <div class="flex justify-between items-center mb-2">
              <span class="font-semibold">Order #{order.id}</span>
              <span class="text-sm text-gray-500">{new Date(order.created_at).toLocaleString()}</span>
            </div>
            <div class="flex justify-between items-center mb-4">
              <span class="text-sm">Status: <span class="capitalize">{order.status}</span></span>
              <span class="font-semibold">Total: ${order.total_amount}</span>
            </div>
            <table class="w-full divide-y divide-gray-200 mb-2">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                  <th class="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Qty</th>
                  <th class="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Price</th>
                  <th class="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {#each order.items as item}
                  <tr class="border-b">
                    <td class="px-3 py-2 text-sm text-gray-700">{item.product.name}</td>
                    <td class="px-3 py-2 text-sm text-gray-700 text-right">{item.qty}</td>
                    <td class="px-3 py-2 text-sm text-gray-700 text-right">${item.price}</td>
                    <td class="px-3 py-2 text-sm text-gray-700 text-right">${item.subtotal}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/each}
      </div>
      {#if next}
        <div class="text-center py-4">
          <button on:click={loadMoreOrders} disabled={loadingMore} class="px-4 py-2 bg-indigo-600 text-white rounded-3xl hover:bg-indigo-700 disabled:opacity-50">
            {#if loadingMore}Loading…{:else}Load more orders{/if}
          </button>
        </div>
      {/if}
    {/if}
  {/if}
</div>