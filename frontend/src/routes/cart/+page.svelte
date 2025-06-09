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
      successMessage = `Thanks for Shopping! Order #${order.id} placed successfully!`;
      cart = { items: [], total_amount: 0 };
      qtyMap = {};
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

<div class="p-6 flex flex-col mx-auto">
  <div class="shadow-lg rounded-3xl p-6">
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
        <table class="table">
          <thead>
            <tr class="">
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Product</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Qty</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Price</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Subtotal</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each cart.items as item}
              <tr class="border-b">
                <td class="px-6 py-4 whitespace-nowrap text-sm">{item.product.name}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <input type="number" bind:value={qtyMap[item.id]} min="1" max={item.product.stock}
                    class="rounded-3xl p-1 px-4 w-20"
                    on:change={() => handleQtyChange(item.id)} />
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${item.price}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${item.subtotal}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button on:click={() => handleRemove(item.id)}
                    class="px-2 py-2 bg-red-600 text-white rounded-3xl hover:bg-red-700 transition">Remove</button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        <div class="mt-4 text-right">
          <p class="text-lg font-semibold">Total: ${cart.total_amount}</p>
        </div>
        <button on:click={checkout}
          class="mt-4 mx-2 px-4 py-2 bg-indigo-600 text-white rounded-3xl hover:bg-indigo-700 transition">Checkout
        </button>
        <button on:click={() => window.location.href = '/'}
          class="mt-4 mx-2 px-4 py-2 text-white rounded-3xl transition">Shop More</button>
      {/if}
    {/if}
  </div>
</div>