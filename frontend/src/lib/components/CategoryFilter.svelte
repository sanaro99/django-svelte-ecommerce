<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let categories: any[] = [];
  export let selectedCategory: string = '';
  const dispatch = createEventDispatcher<{ select: string }>();
  function changeHandler(e: Event) {
    const v = (e.target as HTMLSelectElement).value;
    dispatch('select', v);
  }
</script>

<select bind:value={selectedCategory} on:change={changeHandler} class="input py-2 border rounded-3xl">
  <option value=''>All Categories</option>
  {#each categories as cat}
    <option value={cat.id.toString()}>{cat.name}</option>
  {/each}
</select>
