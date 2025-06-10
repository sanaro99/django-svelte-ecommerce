<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchProducts, fetchCategories } from '$lib/api';
  import ProductCard from '$lib/components/ProductCard.svelte';
  import CategoryFilter from '$lib/components/CategoryFilter.svelte';
  import CheckboxFilter from '$lib/components/CheckboxFilter.svelte';

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
    <CategoryFilter
      {categories}
      selectedCategory={selectedCategory}
      on:select={(e) => { selectedCategory = e.detail; applyFilters(); }}
    />
    <CheckboxFilter
      checked={inStockOnly}
      label="In Stock Only"
      on:change={(e) => { inStockOnly = e.detail; applyFilters(); }}
    />
  </div>

  <div class="text-2xl font-bold mb-6">Products</div>

  {#if needAuth}
    <div class="text-center py-8">
      <p class="text-xl">Welcome! Please <a href="/login" class="text-indigo-600 hover:underline">login</a> or <a href="/register" class="text-indigo-600 hover:underline">register</a> to view products.</p>
    </div>
  {:else if loading}
  <div class="flex justify-center my-4">
    <button class="btn rounded-3xl" on:click={loadMore}>
      <span class="loading loading-spinner"></span>
      loading
    </button>
  </div>
  {:else if error}
    <p class="text-red-600">{error}</p>
  {:else}
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 md:gap-4">
      {#each products as product}
        <ProductCard {product} />
      {/each}
    </div>
    {#if next}
    <div class="flex justify-center my-4">
      <button class="btn rounded-3xl" on:click={loadMore}>
        <span class="loading loading-spinner"></span>
        loading
      </button>
    </div>
    {/if}
  {/if}
</div>