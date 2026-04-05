import { get, post } from "../utils/request";
import type { Article, ArticleCreate } from "../types/article";

export const blogService = {
  async getBlog(id: number): Promise<Article> {
    const res = await get<Article>(`/blog/${id}`);
    return res.data;
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
