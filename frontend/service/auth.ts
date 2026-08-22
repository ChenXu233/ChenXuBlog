// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  loginApisV1AuthLoginPost,
  registerUserApisV1AuthRegisterPost,
  verifyEmailApisV1AuthVerifyTokenGet,
  forgotPasswordApisV1AuthForgotPasswordPost,
  resetPasswordApisV1AuthResetPasswordPost,
  refreshTokenApisV1AuthRefreshPost,
} from "../src/client/sdk.gen";
import { apiCall, setAccessToken } from "../utils/apiClient";
import type {
  LoginResponse,
  UserRegisterResponse,
  MessageResponse,
} from "../src/client/types.gen";

export const authService = {
  async login(evidence: string, password: string): Promise<LoginResponse> {
    const data = await apiCall(() =>
      loginApisV1AuthLoginPost({ body: { evidence, password } }),
    );
    setAccessToken(data.access_token);
    return data;
  },

  // refresh_token 是 httpOnly cookie，浏览器自动携带
  async refreshToken(): Promise<string | null> {
    const data = await apiCall(() => refreshTokenApisV1AuthRefreshPost({}));
    setAccessToken(data.access_token);
    return data.access_token;
  },

  async register(data: {
    username: string;
    password: string;
    email: string;
  }): Promise<UserRegisterResponse> {
    return apiCall(() => registerUserApisV1AuthRegisterPost({ body: data }));
  },

  async verifyEmail(token: string): Promise<string> {
    // ponytail: 后端该端点直接返回字符串而非 MessageResponse，按生成的类型声明
    return apiCall(() =>
      verifyEmailApisV1AuthVerifyTokenGet({ path: { token } }),
    );
  },

  async forgotPassword(email: string): Promise<MessageResponse> {
    return apiCall(() =>
      forgotPasswordApisV1AuthForgotPasswordPost({ body: { email } }),
    );
  },

  async resetPassword(
    token: string,
    new_password: string,
  ): Promise<MessageResponse> {
    return apiCall(() =>
      resetPasswordApisV1AuthResetPasswordPost({
        body: { token, new_password },
      }),
    );
  },
};
