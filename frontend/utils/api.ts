// API request layer — simple $fetch wrapper, no useFetch wrapper needed
export const api = {
  async get<T>(url: string): Promise<T> {
    const auth = useAuthStore()
    return $fetch<T>(url, {
      baseURL: '/apis/v1',
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
  },
  async post<T>(url: string, body?: any): Promise<T> {
    const auth = useAuthStore()
    return $fetch<T>(url, {
      method: 'POST',
      body,
      baseURL: '/apis/v1',
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
  },
  async put<T>(url: string, body?: any): Promise<T> {
    const auth = useAuthStore()
    return $fetch<T>(url, {
      method: 'PUT',
      body,
      baseURL: '/apis/v1',
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
  },
  async delete<T>(url: string): Promise<T> {
    const auth = useAuthStore()
    return $fetch<T>(url, {
      method: 'DELETE',
      baseURL: '/apis/v1',
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
  },
}