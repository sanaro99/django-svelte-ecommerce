<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { fetchProductBySlug } from '$lib/api';

  let product: any = null;
  let loading = true;
  let error = '';
  let slug = '';

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
</script>

<div class="min-h-screen bg-gray-100 flex flex-col items-center py-8">
  {#if loading}
    <p class="text-gray-600">Loading product…</p>
  {:else if error}
    <p class="text-red-600">Error: {error}</p>
  {:else}
    <div class="max-w-2xl w-full bg-white shadow rounded-lg p-6">
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