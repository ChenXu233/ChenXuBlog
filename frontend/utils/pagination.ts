export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/** Fetch every page while retaining the first page's response metadata. */
export async function fetchAllPages<T>(
  fetchPage: (page: number, pageSize: number) => Promise<PaginatedResult<T>>,
  pageSize = 100,
): Promise<PaginatedResult<T>> {
  const first = await fetchPage(1, pageSize);
  const items = [...first.items];

  for (let page = 2; page <= first.total_pages; page += 1) {
    const next = await fetchPage(page, pageSize);
    items.push(...next.items);
  }

  return { ...first, items };
}
