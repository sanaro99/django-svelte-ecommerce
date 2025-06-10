<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let categories: any[] = [];
  export let selectedCategory: string = '';
  const dispatch = createEventDispatcher<{ select: string }>();
  $: selectedName = selectedCategory 
    ? categories.find(cat => cat.id.toString() === selectedCategory)?.name
    : 'All Categories';
  function changeHandler(e: Event) {
    const v = (e.target as HTMLSelectElement).value;
    dispatch('select', v);
  }
</script>

<div class="dropdown">
  <div tabindex="0" role="button" class="btn m-1">{selectedName}</div>
  <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
    <li><a href="#" on:click|preventDefault={() => dispatch('select', '')}>All Categories</a></li>
    {#each categories as cat}
      <li><a href="#" on:click|preventDefault={() => dispatch('select', cat.id.toString())}>{cat.name}</a></li>
    {/each}
  </ul>
</div>
