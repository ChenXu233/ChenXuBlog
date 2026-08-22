// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  getPermissionApisV1PermissionGet,
  havePermissionApisV1PermissionPost,
} from "../shared/api-client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import type { PermissionsResponse } from "../shared/api-client/types.gen";

export const permissionService = {
  async getPermissions(): Promise<PermissionsResponse> {
    return apiCall(() => getPermissionApisV1PermissionGet({}));
  },

  async havePermission(permission: string): Promise<boolean> {
    return apiCall(() =>
      havePermissionApisV1PermissionPost({
        query: { permission_code: permission },
      }),
    );
  },
};
