import { get, del, put } from "../utils/request";

export interface AdminUser {
  id: number;
  uuid: string;
  username: string;
  email: string;
  is_verified: boolean;
  created_at: number;
  roles: string[];
}

export interface AdminBlog {
  id: number;
  user_uuid: string;
  username: string;
  title: string;
  cover_url: string;
  tags_name: string[];
  created_at: number;
  updated_at: number;
  view_count: number;
  likes_count: number;
  published: boolean;
}

export interface AdminComment {
  id: number;
  blog_id: number;
  blog_title: string;
  user_id: number;
  username: string;
  content: string;
  created_at: number;
  updated_at: number;
}

export interface AdminRole {
  id: number;
  name: string;
  description: string;
  is_default: boolean;
  permissions: string[];
}

export interface AdminStats {
  total_users: number;
  total_blogs: number;
  total_comments: number;
  total_blogs_today: number;
  total_comments_today: number;
  recent_blogs: AdminBlog[];
  recent_comments: AdminComment[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

class AdminService {
  async getStats(): Promise<AdminStats> {
    const res = await get<AdminStats>("/apis/v1/admin/stats");
    return res.data;
  }

  async getUsers(
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<AdminUser>> {
    const res = await get<PaginatedResponse<AdminUser>>(
      "/apis/v1/admin/users",
      {
        params: { page, page_size: pageSize },
      },
    );
    return res.data;
  }

  async updateUserRole(userId: number, roleIds: number[]): Promise<AdminUser> {
    const res = await put<AdminUser>(`/apis/v1/admin/users/${userId}/role`, {
      role_ids: roleIds,
    });
    return res.data;
  }

  async deleteUser(userId: number): Promise<void> {
    await del(`/apis/v1/admin/users/${userId}`);
  }

  async getArticles(
    page: number = 1,
    pageSize: number = 10,
    published?: boolean,
  ): Promise<PaginatedResponse<AdminBlog>> {
    const res = await get<PaginatedResponse<AdminBlog>>(
      "/apis/v1/admin/blogs",
      {
        params: { page, page_size: pageSize, published },
      },
    );
    return res.data;
  }

  async toggleBlogPublish(blogId: number): Promise<{ published: boolean }> {
    const res = await put<{ published: boolean }>(
      `/apis/v1/admin/blogs/${blogId}/publish`,
    );
    return res.data;
  }

  async deleteBlog(blogId: number): Promise<void> {
    await del(`/apis/v1/admin/blogs/${blogId}`);
  }

  async getComments(
    page: number = 1,
    pageSize: number = 10,
  ): Promise<PaginatedResponse<AdminComment>> {
    const res = await get<PaginatedResponse<AdminComment>>(
      "/apis/v1/admin/comments",
      {
        params: { page, page_size: pageSize },
      },
    );
    return res.data;
  }

  async deleteComment(commentId: number): Promise<void> {
    await del(`/apis/v1/admin/comments/${commentId}`);
  }

  async getRoles(): Promise<AdminRole[]> {
    const res = await get<AdminRole[]>("/apis/v1/admin/roles");
    return res.data;
  }
}

export const adminService = new AdminService();
