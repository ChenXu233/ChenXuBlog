import { get, post, del } from "../utils/request";
import type { Article, ArticleCreate, Articles } from "../types/article";

export const blogService = {
  async getBlog(id: number): Promise<Article> {
    const res = await get<Article>(`/blog/${id}`);
    return res.data;
  },

  async getBlogList(params?: {
    page?: number;
    page_size?: number;
    tag?: string;
    keyword?: string;
  }): Promise<Articles> {
    const res = await get<Articles>("/blog/", params);
    return res.data;
  },

  async likeBlog(id: number): Promise<{ likes_count: number }> {
    const res = await post<{ likes_count: number }>(`/blog/${id}/like`);
    return res.data;
  },

  async deleteBlog(id: number): Promise<void> {
    await del<void>(`/blog/${id}`);
  },

  async createBlog(data: ArticleCreate): Promise<Article> {
    const res = await post<Article>("/blog/", data);
    return res.data;
  },

  async updateBlog(id: number, data: ArticleCreate): Promise<Article> {
    const res = await post<Article>(`/blog/${id}`, data);
    return res.data;
  },
};
