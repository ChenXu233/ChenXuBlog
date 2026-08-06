import { post } from "../utils/request";

export const authService = {
  async refreshToken(refresh_token: string): Promise<{ access_token: string }> {
    const res = await post<{ access_token: string }>("/auth/refresh", {
      refresh_token,
    });
    return res.data;
  },
};
