const API_BASE = 'http://localhost:8000/api';

export async function fetchProducts(page: number = 1, token?: string) {
  // Paginated fetch: default to page 1
  const res = await fetch(`${API_BASE}/products/?page=${page}`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch products');
  return res.json();
}

// Utility for attaching token, if present
function getAuthHeaders(token?: string): HeadersInit | undefined {
    const t = token || localStorage.getItem('access_token');
    if (t) {
        return { Authorization: `Bearer ${t}` };
    }
    return undefined; // Or return {} if your fetch setup prefers an empty headers object
}

// Fetch product by slug
export async function fetchProductBySlug(slug: string, token?: string) {
  const res = await fetch(`${API_BASE}/products/${slug}/`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch product');
  return res.json();
}

// Fetch all categories
export async function fetchCategories(token?: string) {
  const res = await fetch(`${API_BASE}/categories/`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

// Fetch products by category id or slug (as needed)
export async function fetchProductsByCategory(categoryId: number, token?: string) {
  const res = await fetch(`${API_BASE}/products/?category=${categoryId}`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch products for category');
  return res.json();
}

// Fetch current authenticated user details
export async function fetchCurrentUser(token?: string) {
  const res = await fetch(`http://localhost:8000/accounts/user/`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch user details');
  return res.json();
}

// Logout helper: clear stored tokens only
export function logout() {
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('pkce_code_verifier');
}

// Fetch current user's cart
export async function fetchCart(token?: string) {
  const res = await fetch(`${API_BASE}/cart/`, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error('Failed to fetch cart');
  return res.json();
}

// Add item to cart
export async function addToCart(productId: number, qty: number = 1, token?: string) {
  const res = await fetch(`${API_BASE}/cart/add/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(token),
    },
    body: JSON.stringify({ product_id: productId, qty }),
  });
  let data: any;
  try { data = await res.json(); } catch { data = null; }
  if (!res.ok) {
    const msg = data?.error || data?.detail || `Failed to add to cart (${res.status})`;
    throw new Error(msg);
  }
  return data;
}

// Remove item from cart
export async function removeFromCart(itemId: number, token?: string) {
  const res = await fetch(`${API_BASE}/cart/remove/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(token),
    },
    body: JSON.stringify({ item_id: itemId }),
  });
  let data: any;
  try { data = await res.json(); } catch { data = null; }
  if (!res.ok) {
    const msg = data?.error || data?.detail || `Failed to remove from cart (${res.status})`;
    throw new Error(msg);
  }
  return data;
}