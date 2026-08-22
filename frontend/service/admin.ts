// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  getStatsApisV1AdminStatsGet,
  getUsersApisV1AdminUsersGet,
  deleteUserApisV1AdminUsersUserIdDelete,
  getBlogsApisV1AdminBlogsGet,
  toggleBlogPublishApisV1AdminBlogsBlogIdPublishPut,
  deleteBlogApisV1AdminBlogsBlogIdDelete,
  getCommentsApisV1AdminCommentsGet,
  deleteCommentApisV1AdminCommentsCommentIdDelete,
  getRolesApisV1AdminRolesGet,
} from "../shared/api-client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import type {
  AdminRoleResponse,
  AdminUserListResponse,
  AdminBlogListResponse,
  AdminCommentListResponse,
} from "../shared/api-client/types.gen";

export const adminService = {
  async getStats() {
    return apiCall(() => getStatsApisV1AdminStatsGet({}));
  },

  async getRoles(): Promise<AdminRoleResponse[]> {
    return apiCall(() => getRolesApisV1AdminRolesGet({}));
  },

  async getUsers(
    page: number,
    pageSize: number,
  ): Promise<AdminUserListResponse> {
    return apiCall(() =>
      getUsersApisV1AdminUsersGet({ query: { page, page_size: pageSize } }),
    );
  },

  async deleteUser(id: number): Promise<void> {
    await apiCall(() =>
      deleteUserApisV1AdminUsersUserIdDelete({ path: { user_id: id } }),
    );
  },

  async getBlogs(
    page: number,
    pageSize: number,
    published?: boolean | null,
  ): Promise<AdminBlogListResponse> {
    return apiCall(() =>
      getBlogsApisV1AdminBlogsGet({
        query: { page, page_size: pageSize, published: published ?? undefined },
      }),
    );
  },

  async toggleBlogPublish(id: number): Promise<void> {
    await apiCall(() =>
      toggleBlogPublishApisV1AdminBlogsBlogIdPublishPut({
        path: { blog_id: id },
      }),
    );
  },

  async deleteBlog(id: number): Promise<void> {
    await apiCall(() =>
      deleteBlogApisV1AdminBlogsBlogIdDelete({ path: { blog_id: id } }),
    );
  },

  async getComments(
    page: number,
    pageSize: number,
  ): Promise<AdminCommentListResponse> {
    return apiCall(() =>
      getCommentsApisV1AdminCommentsGet({
        query: { page, page_size: pageSize },
      }),
    );
  },

  async deleteComment(id: number): Promise<void> {
    await apiCall(() =>
      deleteCommentApisV1AdminCommentsCommentIdDelete({
        path: { comment_id: id },
      }),
    );
  },
};
