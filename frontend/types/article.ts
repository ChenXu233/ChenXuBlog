export interface Article {
  id: number
  user_uuid: string
  title: string
  body: string
  created_at: string
  updated_at: string
  view_count: number
  likes_count: number
  published: boolean
  tags_name: string[]
  cover_url?: string
}

export interface ArticleList {
  items: Article[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface ArticleCreate {
  title: string
  body: string
  tags: string[]
  published: boolean
}