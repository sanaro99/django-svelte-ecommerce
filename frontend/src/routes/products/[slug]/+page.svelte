<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { fetchProductBySlug, addToCart } from '$lib/api';

  let product: any = null;
  let loading = true;
  let error = '';
  let slug = '';
  let currentIndex: number = 0;
  let qty: number = 1;
  let errorMessage = '';
  let adding = false;

  // Subscribe to the page store to get the slug
  $: slug = $page.params.slug;

  onMount(async () => {
    try {
      product = await fetchProductBySlug(slug);
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function prevImage() {
    if (product.images?.length) {
      currentIndex = currentIndex > 0 ? currentIndex - 1 : product.images.length - 1;
    }
  }

  function nextImage() {
    if (product.images?.length) {
      currentIndex = (currentIndex + 1) % product.images.length;
    }
  }

  async function handleAddToCart() {
    errorMessage = '';
    if (qty < 1) {
      errorMessage = 'Quantity must be at least 1';
      return;
    }
    if (qty > product.stock) {
      errorMessage = `Only ${product.stock} items in stock`;
      return;
    }
    adding = true;
    try {
      await addToCart(product.id, qty);
      window.location.href = '/cart';
    } catch (e: any) {
      errorMessage = e.message;
    } finally {
      adding = false;
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center py-8">
  {#if loading}
    <div class="flex justify-center my-4">
      <button class="btn rounded-3xl">
        <span class="loading loading-spinner"></span>
        loading
      </button>
    </div>
  {:else if error}
    <p class="text-red-600">Error: {error}</p>
  {:else}
    <div class="card max-w-2xl w-full shadow rounded-3xl p-6 card card-compact bg-base-100 shadow-xl hover:shadow-2xl transition duration-200">
      {#if product.images?.length}
        <div class="relative mb-4">
          <img src={product.images[currentIndex].url} alt={product.name} class="w-full h-64 object-cover rounded-3xl" />
          <button on:click={prevImage} class="absolute left-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full">&#10094;</button>
          <button on:click={nextImage} class="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full">&#10095;</button>
        </div>
      {/if}
      <div class="mt-4 flex items-center space-x-2">
        <input type="number" bind:value={qty} min="1" max={product.stock} class="input w-20 border px-5 rounded-3xl" />
        <button on:click={handleAddToCart} class="btn rounded-3xl px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50" disabled={adding || product.stock === 0}>
          {#if adding}Adding...{:else}Add to Cart{/if}
        </button>
      </div>
      {#if errorMessage}
        <p class="text-red-600 mt-2">{errorMessage}</p>
      {/if}
      <h1 class="text-3xl font-bold mb-4">{product.name}</h1>
      <p class="mb-2">{product.description}</p>
      <p class="text-xl font-semibold">Price: ${product.price}</p>
      <!-- Specifications -->
      <div class="mt-4">
        <h2 class="text-lg font-medium mb-2">Specifications</h2>
        {#if product.specifications && product.specifications.length}
          <ul class="list-disc list-inside">
            {#each product.specifications as spec}
              <li><strong>{spec.name}:</strong> {spec.value}</li>
            {/each}
          </ul>
        {:else}
          <p>No specifications available.</p>
        {/if}
      </div>
    </div>
  {/if}
</div>