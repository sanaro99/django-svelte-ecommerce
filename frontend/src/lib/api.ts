// Base URLs from env
export const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:8000';
export const FRONTEND_BASE_URL = import.meta.env.VITE_FRONTEND_BASE_URL || window.location.origin;
export const API_BASE = `${BACKEND_BASE_URL}/api`;

export async function fetchProducts(page: number = 1, category?: number, inStockOnly: boolean = false, token?: string) {
  let url = `${API_BASE}/products/?page=${page}`;
  if (category) url += `&category=${category}`;
  if (inStockOnly) url += `&stock__gte=1`;
  const res = await fetch(url, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) throw new Error(`Failed to fetch products (${res.status})`);
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
  if (!res.ok) throw new Error(`Failed to fetch categories (${res.status})`);
  const data = await res.json();
  return data.results ?? data;
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
  const t = token || localStorage.getItem('access_token');
  if (!t) return null;
  const res = await fetch(`${BACKEND_BASE_URL}/accounts/user/`, {
    headers: getAuthHeaders(t),
  });
  if (res.status === 401) return null;
  if (!res.ok) throw new Error(`Failed to fetch user details (${res.status})`);
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

// Checkout cart
export async function checkoutCart(token?: string) {
  const res = await fetch(`${API_BASE}/cart/checkout/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(token),
    },
  });
  let data: any;
  try { data = await res.json(); } catch { data = null; }
  if (!res.ok) {
    const msg = data?.error || data?.detail || `Failed to checkout cart (${res.status})`;
    throw new Error(msg);
  }
  return data;
}

// Fetch current user's orders
export async function fetchOrders(token?: string, status?: string, createdAfter?: string) {
  let url = `${API_BASE}/orders/`;
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  if (createdAfter) params.append('created_at__gte', createdAfter);
  const query = params.toString();
  const res = await fetch(query ? `${url}?${query}` : url, {
    headers: getAuthHeaders(token),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const msg = data?.error || data?.detail || `Failed to fetch orders (${res.status})`;
    throw new Error(msg);
  }
  const data = await res.json();
  return data.results ?? data;
}

/**
 * Update the current user's profile data.
 * @param data Object with username, email, first_name, last_name, and optional profile fields (phone, street_address, city, state, postal_code, country)
 * @param token Optional access token
 */
export async function updateUser(
  data: {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    phone?: string;
    street_address?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
  },
  token?: string
) {
  const t = token || localStorage.getItem('access_token');
  const res = await fetch(`${BACKEND_BASE_URL}/accounts/user/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...(t ? { Authorization: `Bearer ${t}` } : {}),
    },
    body: JSON.stringify(data),
  });
  const result = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(result.error || result.detail || `Failed to update user (${res.status})`);
  return result;
}
