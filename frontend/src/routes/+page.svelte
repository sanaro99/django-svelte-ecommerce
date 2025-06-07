<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchProducts } from '$lib/api';

  let products: any[] = [];
  let loading = true;
  let error = '';
  let page: number = 1;
  let next: string | null = null;
  let loadingMore: boolean = false;

  onMount(async () => {
    try {
      const res = await fetchProducts(page);
      products = res.results;
      next = res.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  async function loadMore() {
    if (!next) return;
    loadingMore = true;
    try {
      page += 1;
      const res = await fetchProducts(page);
      products = [...products, ...res.results];
      next = res.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loadingMore = false;
    }
  }
</script>

<h1 class="text-2xl font-bold text-gray-900 mb-6">Products</h1>
{#if loading}
  <p class="text-gray-600">Loading…</p>
{:else if error}
  <p class="text-red-600">{error}</p>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each products as product}
      <div class="bg-white rounded-lg shadow-sm hover:shadow-md overflow-hidden transition-shadow duration-200">
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
              class="px-5 py-2 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700 transition disabled:opacity-50">
        {#if loadingMore}Loading...{:else}Load More{/if}
      </button>
    </div>
  {/if}
{/if}