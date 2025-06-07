<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchOrders } from '$lib/api';

  let orders: any[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      const data = await fetchOrders();
      orders = data;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });
</script>

<div class="p-6 max-w-4xl mx-auto">
  <h2 class="text-2xl font-bold mb-4">Your Orders</h2>
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
          <div class="bg-white shadow p-4 rounded-lg">
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
    {/if}
  {/if}
</div>