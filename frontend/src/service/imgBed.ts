import { post } from "../utils/request";

export const imgBedService = {
  async uploadImg(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await post<{ url: string }>("/img_bed/", formData);
    return res.data;
  },
};
