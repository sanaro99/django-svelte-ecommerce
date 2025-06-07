<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchCart, removeFromCart, addToCart } from '$lib/api';

  let cart: { items: any[]; total_amount: number } = { items: [], total_amount: 0 };
  let loading = true;
  let error = '';
  let qtyMap: Record<number, number> = {};

  onMount(async () => {
    try {
      cart = await fetchCart();
      cart.items.forEach(item => { qtyMap[item.id] = item.qty; });
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  async function handleRemove(itemId: number) {
    loading = true;
    try {
      cart = await removeFromCart(itemId);
      delete qtyMap[itemId];
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function handleQtyChange(itemId: number) {
    const newQty = qtyMap[itemId];
    loading = true;
    try {
      const item = cart.items.find(i => i.id === itemId);
      cart = await addToCart(item.product.id, newQty);
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="p-6 max-w-2xl mx-auto">
  <div class="bg-white shadow-lg rounded-lg p-6">
    <h2 class="text-2xl font-bold mb-4">Your Cart</h2>
    {#if loading}
      <p>Loading cart...</p>
    {:else if error}
      <p class="text-red-600">{error}</p>
    {:else}
      {#if cart.items.length === 0}
        <p>Your cart is empty.</p>
      {:else}
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr class="bg-gray-50">
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subtotal</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each cart.items as item}
              <tr class="border-b">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{item.product.name}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <input type="number" bind:value={qtyMap[item.id]} min="1" max={item.product.stock}
                    class="border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 rounded-md p-1 w-20"
                    on:change={() => handleQtyChange(item.id)} />
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${item.price}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${item.subtotal}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button on:click={() => handleRemove(item.id)}
                    class="px-2 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 transition">Remove</button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        <div class="mt-4 text-right">
          <p class="text-lg font-semibold text-gray-900">Total: ${cart.total_amount}</p>
        </div>
      {/if}
    {/if}
  </div>
</div>