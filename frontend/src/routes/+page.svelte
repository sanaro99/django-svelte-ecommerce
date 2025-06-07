<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchProducts, fetchCategories } from '$lib/api';

  let products: any[] = [];
  let categories: any[] = [];
  let selectedCategory: string = '';
  let inStockOnly = false;
  let loading = true;
  let error = '';
  let page = 1;
  let next: string | null = null;
  let loadingMore = false;

  onMount(async () => {
    try {
      categories = await fetchCategories();
    } catch (e: any) {
      console.error('Failed to load categories', e);
    }
    await loadProducts();
  });

  async function loadProducts() {
    error = '';
    loading = true;
    try {
      const categoryId = selectedCategory ? Number(selectedCategory) : undefined;
      const res = await fetchProducts(page, categoryId, inStockOnly);
      products = res.results;
      next = res.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function applyFilters() {
    page = 1;
    await loadProducts();
  }

  async function loadMore() {
    if (!next) return;
    loadingMore = true;
    try {
      page += 1;
      const categoryId = selectedCategory ? Number(selectedCategory) : undefined;
      const res = await fetchProducts(page, categoryId, inStockOnly);
      products = [...products, ...res.results];
      next = res.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loadingMore = false;
    }
  }
</script>

<!-- Filters UI -->
<div class="flex flex-wrap gap-4 mb-6">
  <select bind:value={selectedCategory} on:change={applyFilters} class="px-3 py-2 border rounded-3xl pr-10">
    <option value=''>All Categories</option>
    {#each categories as cat}
      <option value={cat.id}>{cat.name}</option>
    {/each}
  </select>
  <label class="inline-flex items-center">
    <input type="checkbox" bind:checked={inStockOnly} on:change={applyFilters} />
    <span class="ml-2">In Stock Only</span>
  </label>
</div>

<h1 class="text-2xl font-bold text-gray-900 mb-6">Products</h1>
{#if loading}
  <p class="text-gray-600">Loading…</p>
{:else if error}
  <p class="text-red-600">{error}</p>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each products as product}
      <div class="bg-white rounded-3xl shadow-sm hover:shadow-md overflow-hidden transition-shadow duration-200">
        {#if product.images?.length}
          <img src={product.images[0].url} alt={product.name} class="w-full h-48 object-cover rounded-t-lg" />
        {/if}
        <div class="p-4">
          <a href={`/products/${product.slug}`} class="text-lg font-semibold text-gray-800 hover:text-indigo-600 transition">
            {product.name}
          </a>
          <p class="text-gray-700 mt-2 font-semibold">${product.price}</p>
        </div>
      </div>
    {/each}
  </div>
  {#if next}
    <div class="mt-6 flex justify-center">
      <button on:click={loadMore} disabled={loadingMore}
              class="px-5 py-2 bg-indigo-600 text-white rounded-3xl shadow hover:bg-indigo-700 transition disabled:opacity-50">
        {#if loadingMore}Loading...{:else}Load More{/if}
      </button>
    </div>
  {/if}
{/if}