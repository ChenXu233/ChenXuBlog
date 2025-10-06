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
  like: number;
  tags_name: string[];
  cover_url?: string;
}

export interface Articles {
  articles: Article[];
  total: number;
}

export interface ArticleUpdate {
  title: string;
  body: string;
  tags_name: string[];
  cover_url?: string;
}

export interface ArticleCreate {
  title: string;
  body: string;
  tags_name: string[];
  cover_url?: string;
}
