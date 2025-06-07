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
    await addToCart(product.id, qty);
    window.location.href = '/cart';
  }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col items-center py-8">
  {#if loading}
    <p class="text-gray-600">Loading product…</p>
  {:else if error}
    <p class="text-red-600">Error: {error}</p>
  {:else}
    <div class="max-w-2xl w-full bg-white shadow rounded-lg p-6">
      {#if product.images?.length}
        <div class="relative mb-4">
          <img src={product.images[currentIndex].url} alt={product.name} class="w-full h-64 object-cover rounded-lg" />
          <button on:click={prevImage} class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-50 p-2 rounded-full">&#10094;</button>
          <button on:click={nextImage} class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-50 p-2 rounded-full">&#10095;</button>
        </div>
      {/if}
      <div class="mt-4 flex items-center space-x-2">
        <input type="number" bind:value={qty} min="1" max={product.stock} class="w-20 border p-1 rounded" />
        <button on:click={handleAddToCart} class="px-4 py-2 bg-indigo-600 text-white rounded">Add to Cart</button>
      </div>
      <h1 class="text-3xl font-bold text-gray-900 mb-4">{product.name}</h1>
      <p class="text-gray-700 mb-2">{product.description}</p>
      <p class="text-xl font-semibold text-indigo-600">Price: ${product.price}</p>
      <!-- Specifications -->
      <div class="mt-4">
        <h2 class="text-lg font-medium text-gray-900 mb-2">Specifications</h2>
        {#if product.specifications && product.specifications.length}
          <ul class="list-disc list-inside text-gray-700">
            {#each product.specifications as spec}
              <li><strong>{spec.name}:</strong> {spec.value}</li>
            {/each}
          </ul>
        {:else}
          <p class="text-gray-600">No specifications available.</p>
        {/if}
      </div>
    </div>
  {/if}
</div>