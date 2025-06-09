<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchProducts, fetchCategories } from '$lib/api';
  import ProductCard from '$lib/components/ProductCard.svelte';
  import LoadMoreButton from '$lib/components/LoadMoreButton.svelte';

  let products: any[] = [];
  let categories: any[] = [];
  let selectedCategory: string = '';
  let inStockOnly = false;
  let loading = true;
  let error = '';
  let page = 1;
  let next: string | null = null;
  let loadingMore = false;
  let token: string | undefined;
  let needAuth = false;
  let catNext: string | null = null;
  let catLoadingMore = false;
  let showCatDropdown = false;

  onMount(async () => {
  if (typeof window === 'undefined') return; // SSR guard
  const t = window.localStorage.getItem('access_token');
  if (!t) {
    needAuth = true;
    loading = false;
    return;
  }
  token = t ?? undefined;
  try {
    const catData = await fetchCategories(1, token);
    categories = catData.results;
    catNext = catData.next;
  } catch (e: any) {
    console.error('Failed to load categories', e);
  }
  await loadProducts();
  window.addEventListener('scroll', handleScroll);
  // auto-trigger loadMore if content shorter than viewport
  handleScroll();
});

  onDestroy(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', handleScroll);
  }
});

  async function loadProducts() {
    error = '';
    loading = true;
    try {
      const categoryId = selectedCategory ? Number(selectedCategory) : undefined;
      const res = await fetchProducts(page, categoryId, inStockOnly, token);
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
      const res = await fetchProducts(page, categoryId, inStockOnly, token);
      products = [...products, ...res.results];
      next = res.next;
    } catch (e: any) {
      error = e.message;
    } finally {
      loadingMore = false;
    }
  }

  async function loadMoreCategories() {
    if (!catNext) return;
    catLoadingMore = true;
    try {
      const data = await fetchCategories(catNext, token);
      categories = [...categories, ...data.results];
      catNext = data.next;
    } catch (e: any) {
      console.error('Failed to load more categories', e);
    } finally {
      catLoadingMore = false;
    }
  }

  function onCatScroll(event: Event) {
    const el = event.target as HTMLElement;
    if (catNext && !catLoadingMore && el.scrollHeight - el.scrollTop <= el.clientHeight + 10) {
      loadMoreCategories();
    }
  }

  // infinite scroll for products
  function handleScroll() {
    if (!loadingMore && next && window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
      loadMore();
    }
  }
</script>

<!-- Filters UI -->
<div class="mx-2">
  <div class="flex flex-wrap gap-4 mb-6">
    <div class="relative w-64">
      <button on:click={() => showCatDropdown = !showCatDropdown} class="w-full px-3 py-2 border rounded-3xl pr-8 text-left flex justify-between items-center">
        {#if selectedCategory}
          {categories.find(c => c.id === +selectedCategory)?.name}
        {:else}
          All Categories
        {/if}
        <svg class="w-4 h-4 text-gray-500 ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {#if showCatDropdown}
        <ul on:scroll={onCatScroll} class="absolute z-10 bg-white border rounded-3xl shadow max-h-36 overflow-y-auto w-full">
          <li class="px-3 py-2 hover:bg-gray-100 cursor-pointer" on:click={() => { selectedCategory = ''; applyFilters(); showCatDropdown = false; }}>All Categories</li>
          {#each categories as cat}
            <li class="px-3 py-2 hover:bg-gray-100 cursor-pointer" on:click={() => { selectedCategory = cat.id.toString(); applyFilters(); showCatDropdown = false; }}>{cat.name}</li>
          {/each}
          {#if catNext}
            <li class="px-3 py-2 text-center">
              <button on:click={loadMoreCategories} disabled={catLoadingMore} class="text-gray-600 hover:text-gray-800 disabled:opacity-50">
                {#if catLoadingMore}Loading…{:else}Load more{/if}
              </button>
            </li>
          {/if}
        </ul>
      {/if}
    </div>
    <label class="inline-flex items-center">
      <input type="checkbox" bind:checked={inStockOnly} on:change={applyFilters} />
      <span class="ml-2">In Stock Only</span>
    </label>
  </div>

  <h1 class="text-2xl font-bold text-gray-900 mb-6">Products</h1>

  {#if needAuth}
    <div class="text-center py-8">
      <p class="text-xl text-gray-700">Welcome! Please <a href="/login" class="text-indigo-600 hover:underline">login</a> or <a href="/register" class="text-indigo-600 hover:underline">register</a> to view products.</p>
    </div>
  {:else if loading}
    <p class="text-gray-600">Loading…</p>
  {:else if error}
    <p class="text-red-600">{error}</p>
  {:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {#each products as product}
        <ProductCard {product} />
      {/each}
    </div>
    {#if next}
      <div class="mt-6 flex justify-center">
        <LoadMoreButton on:click={loadMore} loading={loadingMore} label="Load More" />
      </div>
    {/if}
  {/if}
</div>