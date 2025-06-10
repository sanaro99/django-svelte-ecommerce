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
        <div class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Subtotal</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {#each cart.items as item}
                <tr class="border-b">
                  <td>{item.product.name}</td>
                  <td>
                    <input type="number" bind:value={qtyMap[item.id]} min="1" max={item.product.stock}
                      class="input input-bordered rounded-3xl max-w-20"
                      on:change={() => handleQtyChange(item.id)} />
                  </td>
                  <td>${item.price}</td>
                  <td>${item.subtotal}</td>
                  <td>
                    <button on:click={() => handleRemove(item.id)}
                      class="btn rounded-3xl bg-red-600 text-white">Remove</button>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
        <div class="mt-4 text-right">
          <p class="text-lg font-semibold">Total: ${cart.total_amount}</p>
        </div>
        <button on:click={checkout}
          class="btn rounded-3xl bg-indigo-600 text-white">Checkout
        </button>
        <button on:click={() => window.location.href = '/'}
          class="btn rounded-3xl bg-gray-600 text-white">Shop More</button>
      {/if}
    {/if}
  </div>
</div>