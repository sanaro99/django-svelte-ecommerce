<script lang="ts">
  export let loading: boolean = false;
  export let label: string = 'Load More';
</script>

<button
  type="button"
  disabled={loading}
  class="px-5 py-2 bg-indigo-600 text-white rounded-3xl shadow hover:bg-indigo-700 transition disabled:opacity-50"
>
  {#if loading}Loading...{:else}{label}{/if}
</button>
