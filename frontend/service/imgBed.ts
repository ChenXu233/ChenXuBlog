// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  imageUploadApisV1ImgBedPost,
  imageGetApisV1ImgBedObjectNameGet,
} from "../src/client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import type { BodyImageUploadApisV1ImgBedPost } from "../src/client/types.gen";

export const imgBedService = {
  async uploadImg(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append("file", file);
    const body: BodyImageUploadApisV1ImgBedPost = formData;
    return apiCall(() => imageUploadApisV1ImgBedPost({ body }));
  },

  async getImage(object_name: string): Promise<Blob> {
    return apiCall(() =>
      imageGetApisV1ImgBedObjectNameGet({
        path: { object_name },
        parseAs: "blob",
      }),
    );
  },
};
