// 与后端 openapi.json 生成的类型保持一致（BlogResponse / BlogCreate）
export interface Article {
  id: number;
  user_uuid: string;
  title: string;
  body: string;
  created_at: string;
  updated_at: string;
  view_count: number;
  likes_count: number;
  published: boolean;
  tags_name: string[];
  cover_url?: string;
}

export interface Articles {
  items: Article[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// 与后端 BlogCreate 对齐（tags 而非 tags_name）
export interface ArticleCreate {
  title: string;
  body: string;
  tags: string[];
  cover_url?: string;
  published: boolean;
}
