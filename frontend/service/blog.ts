// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  getBlogsApisV1BlogGet,
  getBlogApisV1BlogIdGet,
  createBlogApisV1BlogPost,
  updateBlogApisV1BlogIdPut,
  deleteBlogApisV1BlogIdDelete,
  toggleLikeApisV1BlogIdLikePost,
  getLikeStatusApisV1BlogIdLikeGet,
} from "../shared/api-client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import type {
  BlogResponse,
  BlogListResponse,
  BlogCreate,
} from "../shared/api-client/types.gen";

export const blogService = {
  async getBlog(id: number): Promise<BlogResponse> {
    return apiCall(() => getBlogApisV1BlogIdGet({ path: { id } }));
  },

  async getBlogList(params?: {
    page?: number;
    page_size?: number;
    tag?: string;
    keyword?: string;
    search?: string;
    user_id?: string;
  }): Promise<BlogListResponse> {
    const query: any = {
      page: params?.page,
      page_size: params?.page_size,
      tag: params?.tag,
      user_id: params?.user_id,
    };
    // 兼容新旧参数名
    if (params?.keyword) query.search = params.keyword;
    if (params?.search) query.search = params.search;
    return apiCall(() => getBlogsApisV1BlogGet({ query }));
  },

  async likeBlog(id: number): Promise<{ liked: boolean; likes_count: number }> {
    return apiCall(() => toggleLikeApisV1BlogIdLikePost({ path: { id } }));
  },

  async getLikeStatus(id: number): Promise<{ likes_count: number }> {
    return apiCall(() => getLikeStatusApisV1BlogIdLikeGet({ path: { id } }));
  },

  async deleteBlog(id: number): Promise<void> {
    await apiCall(() => deleteBlogApisV1BlogIdDelete({ path: { id } }));
  },

  async createBlog(data: BlogCreate): Promise<BlogResponse> {
    return apiCall(() => createBlogApisV1BlogPost({ body: data }));
  },

  async updateBlog(id: number, data: BlogCreate): Promise<BlogResponse> {
    return apiCall(() =>
      updateBlogApisV1BlogIdPut({ path: { id }, body: data }),
    );
  },
};
