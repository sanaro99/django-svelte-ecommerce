<script lang="ts">
  export let product: any;
</script>

<a href={`/products/${product.slug}`} class="card-title link link-hover">
  <div class="card card-compact bg-base-100 shadow-xl hover:shadow-2xl transition duration-200 rounded-3xl w-full">
    {#if product.images?.length}
      <figure><img src={product.images[0].url} alt={product.name} /></figure>
    {/if}
    <div class="card-body text-lg font-semibold">
      {product.name}
      <p class="text-sm">${product.price}</p>
    </div>
  </div>
</a>