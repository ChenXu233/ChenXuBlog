import { get, post } from "../utils/request";
import type { Comment, CommentCreate, CommentsResponse } from "../types/comment";

export const commentService = {
  async getComments(blogId: number): Promise<CommentsResponse> {
    const res = await get<CommentsResponse>(`/comment/get/${blogId}`);
    return res.data;
  },

  async createComment(data: CommentCreate): Promise<Comment> {
    const res = await post<Comment>("/comment/create", data);
    return res.data;
  },

  async deleteComment(commentId: number): Promise<void> {
    await post(`/comment/delete/${commentId}`, {});
  },

  async updateComment(commentId: number, data: CommentCreate): Promise<Comment> {
    const res = await post<Comment>(`/comment/update/${commentId}`, data);
    return res.data;
  },
};
