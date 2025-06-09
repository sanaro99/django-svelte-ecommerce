<script>
  export let product;
</script>

<a href={`/products/${product.slug}`} class="text-lg font-semibold text-gray-800 hover:text-indigo-600 transition">
    <div class="bg-white rounded-3xl shadow-sm hover:shadow-md overflow-hidden transition-shadow duration-200">
    {#if product.images?.length}
        <img src={product.images[0].url} alt={product.name} class="w-full h-48 object-cover rounded-t-lg" />
    {/if}
    <div class="p-4">
        {product.name}
        <p class="text-gray-700 mt-2 font-semibold">${product.price}</p>
    </div>
    </div>
</a>