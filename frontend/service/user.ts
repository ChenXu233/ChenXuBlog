// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  getUserInfoApisV1UserInfoGet,
  getUserInfoByIdApisV1UserInfoUserUuidGet,
  editUserInfoApisV1UserEditPost,
} from "../shared/api-client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import { getBlogsApisV1BlogGet } from "../shared/api-client/sdk.gen";
import type {
  UserResponse,
  UserEdit,
  BlogListResponse,
} from "../shared/api-client/types.gen";

export const userService = {
  // 获取自己的信息（需要登录）
  async getOwnInfo(): Promise<UserResponse> {
    return apiCall(() => getUserInfoApisV1UserInfoGet({}));
  },

  // 获取指定用户信息（公开接口）
  async getUserInfo(uuid: string): Promise<UserResponse> {
    return apiCall(() =>
      getUserInfoByIdApisV1UserInfoUserUuidGet({ path: { user_uuid: uuid } }),
    );
  },

  // 编辑资料（后端用当前登录用户，无需传 id）
  async updateUserInfo(data: UserEdit): Promise<UserResponse> {
    return apiCall(() => editUserInfoApisV1UserEditPost({ body: data }));
  },

  async getUserBlogs(params: {
    user_id: string;
    page?: number;
    page_size?: number;
  }): Promise<BlogListResponse> {
    return apiCall(() =>
      getBlogsApisV1BlogGet({
        query: {
          user_id: params.user_id,
          page: params.page,
          page_size: params.page_size,
        },
      }),
    );
  },
};
