import { get, post } from "../utils/request";
import type { User, UserUpdate } from "../types/user";

export const userService = {
  async getUserInfo(uuid: string): Promise<User> {
    const res = await get<User>(`/user/info/${uuid}`);
    return res.data;
  },

  async updateUserInfo(id: string, data: UserUpdate): Promise<User> {
    const res = await post<User>(`/user/${id}`, data);
    return res.data;
  },

  async getUserBlogs(params: {
    user_id: string;
    page?: number;
    page_size?: number;
  }): Promise<{ articles: any[]; total: number }> {
    const res = await get<{ articles: any[]; total: number }>("/blog/", {
      user_id: params.user_id,
      page: params.page,
      page_size: params.page_size,
    });
    return res.data;
  },
};
