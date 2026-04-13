export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly statusText: string,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

type RequestOptions = {
  cache?: RequestCache
  next?: NextFetchRequestConfig
  headers?: Record<string, string>
  signal?: AbortSignal
}

export abstract class BaseApiClient {
  protected readonly baseUrl: string
  protected readonly defaultHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  }

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
  }

  private async request<T>(
    method: string,
    path: string,
    opts: RequestOptions & { body?: unknown } = {},
  ): Promise<T> {
    const { cache, next, headers, signal, body } = opts
    const res = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: { ...this.defaultHeaders, ...headers },
      ...(body !== undefined && { body: JSON.stringify(body) }),
      ...(cache !== undefined && { cache }),
      ...(next !== undefined && { next }),
      ...(signal !== undefined && { signal }),
    })

    if (!res.ok) {
      throw new ApiError(res.status, res.statusText, `${method} ${path} → ${res.status}`)
    }

    if (res.status === 204) return undefined as T
    return res.json() as Promise<T>
  }

  protected get<T>(path: string, opts?: RequestOptions): Promise<T> {
    return this.request<T>("GET", path, opts)
  }

  protected post<T>(path: string, body: unknown, opts?: RequestOptions): Promise<T> {
    return this.request<T>("POST", path, { ...opts, body })
  }

  protected put<T>(path: string, body: unknown, opts?: RequestOptions): Promise<T> {
    return this.request<T>("PUT", path, { ...opts, body })
  }

  protected delete<T>(path: string, opts?: RequestOptions): Promise<T> {
    return this.request<T>("DELETE", path, opts)
  }
}
