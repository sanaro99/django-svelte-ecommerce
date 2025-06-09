<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let checked: boolean = false;
  export let label: string = '';
  const dispatch = createEventDispatcher<{ change: boolean }>();
  function onChange(e: Event) {
    const target = e.target as HTMLInputElement;
    dispatch('change', target.checked);
  }
</script>

<label class="inline-flex items-center space-x-2">
  <input type="checkbox" class="checkbox" bind:checked={checked} on:change={onChange} />
  <span>{label}</span>
</label>
