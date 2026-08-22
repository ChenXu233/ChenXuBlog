// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  imageUploadApisV1ImgBedPost,
  imageGetApisV1ImgBedObjectNameGet,
} from "../shared/api-client/sdk.gen";
import { apiCall } from "../utils/apiClient";

export const imgBedService = {
  async uploadImg(file: File): Promise<{ url: string }> {
    // 后端 UploadFile 参数名为 image，hey-api 自动构造 multipart
    return apiCall(() =>
      imageUploadApisV1ImgBedPost({ body: { image: file } }),
    );
  },

  async getImage(object_name: string): Promise<Blob> {
    return apiCall(() =>
      imageGetApisV1ImgBedObjectNameGet({
        path: { object_name },
        parseAs: "blob",
      }),
    ) as Promise<Blob>;
  },
};
