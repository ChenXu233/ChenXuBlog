export interface Article {
  id: number;
  title: string;
  content: string;
  date: string;
  tags: string[];
  cover_url?: string;
}
