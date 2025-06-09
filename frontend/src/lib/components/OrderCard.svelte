<script>
  export let order;
</script>

<div class="card shadow-xl rounded-3xl mb-4">
  <div class="card-body space-y-4">
    <div class="flex justify-between items-center">
      <span class="font-semibold">Order #{order.id}</span>
      <span class="text-sm 500">{new Date(order.created_at).toLocaleString()}</span>
    </div>
    <div class="flex justify-between items-center">
      <span class="text-sm">Status: <span class="capitalize">{order.status}</span></span>
      <span class="font-semibold">Total: ${order.total_amount}</span>
    </div>
    <div class="overflow-x-auto">
      <table class="table w-full mb-0">
        <thead>
          <tr>
            <th>Product</th>
            <th class="text-right">Qty</th>
            <th class="text-right">Price</th>
            <th class="text-right">Subtotal</th>
          </tr>
        </thead>
        <tbody>
          {#each order.items as item}
          <tr>
            <td>{item.product.name}</td>
            <td class="text-right">{item.qty}</td>
            <td class="text-right">${item.price}</td>
            <td class="text-right">${item.subtotal}</td>
          </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
