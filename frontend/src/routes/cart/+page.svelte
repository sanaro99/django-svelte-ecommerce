<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchCart, removeFromCart, addToCart, checkoutCart } from '$lib/api';

  let cart: { items: any[]; total_amount: number } = { items: [], total_amount: 0 };
  let loading = true;
  let error = '';
  let successMessage = '';
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

  async function checkout() {
    error = '';
    loading = true;
    try {
      const order = await checkoutCart();
      successMessage = `Order #${order.id} placed successfully!`;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function handleRemove(itemId: number) {
    error = '';
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
    error = '';
    const item = cart.items.find(i => i.id === itemId);
    if (!item) return;
    if (newQty < 1) {
      error = 'Quantity must be at least 1';
      qtyMap[itemId] = item.qty;
      return;
    }
    if (newQty > item.product.stock) {
      error = `Only ${item.product.stock} items in stock`;
      qtyMap[itemId] = item.qty;
      return;
    }
    loading = true;
    try {
      cart = await addToCart(item.product.id, newQty);
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="p-6 max-w-2xl mx-auto">
  <div class="bg-white shadow-lg rounded-3xl p-6">
    <h2 class="text-2xl font-bold mb-4">Your Cart</h2>
    {#if loading}
      <p>Loading cart...</p>
    {:else}
      {#if error}
        <p class="text-red-600 mb-4">{error}</p>
      {/if}
      {#if successMessage}
        <p class="text-green-600 mb-4">{successMessage} <a href="/orders" class="text-indigo-600 hover:underline">View Orders</a></p>
      {/if}
      {#if cart.items.length === 0}
        <p>Your cart is empty. <a href="/" class="text-indigo-600 hover:underline">Start shopping</a>.</p>
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
                    class="border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 rounded-3xl p-1 w-20"
                    on:change={() => handleQtyChange(item.id)} />
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${item.price}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${item.subtotal}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button on:click={() => handleRemove(item.id)}
                    class="px-2 py-1 bg-red-600 text-white rounded-3xl hover:bg-red-700 transition">Remove</button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        <div class="mt-4 text-right">
          <p class="text-lg font-semibold text-gray-900">Total: ${cart.total_amount}</p>
        </div>
        <button on:click={checkout}
          class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-3xl hover:bg-indigo-700 transition">Checkout
        </button>
        <button on:click={() => window.location.href = '/'}
          class="mt-4 px-4 py-2 bg-gray-600 text-white rounded-3xl hover:bg-gray-700 transition">Shop
          More</button>
      {/if}
    {/if}
  </div>
</div>