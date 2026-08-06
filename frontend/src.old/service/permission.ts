import { get } from "../utils/request";

export interface PermissionResponse {
  permissions: string[];
}

export const permissionService = {
  async getPermissions(): Promise<PermissionResponse> {
    const res = await get<PermissionResponse>("/permission/");
    return res.data;
  },
};
