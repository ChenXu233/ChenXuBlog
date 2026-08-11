// 由 backend/openapi.json 自动生成 SDK 封装（不要手改端点路径）
import {
  getCommentsApisV1CommentGetBlogIdGet,
  createCommentApisV1CommentCreatePost,
  deleteCommentApisV1CommentDeleteCommentIdDelete,
  updateCommentApisV1CommentUpdateCommentIdPut,
} from "../src/client/sdk.gen";
import { apiCall } from "../utils/apiClient";
import type {
  Comment,
  CommentCreate,
  CommentsResponse,
} from "../src/client/types.gen";

export const commentService = {
  async getComments(blogId: number): Promise<CommentsResponse> {
    return apiCall(() =>
      getCommentsApisV1CommentGetBlogIdGet({ path: { blog_id: blogId } }),
    );
  },

  async createComment(data: CommentCreate): Promise<Comment> {
    return apiCall(() => createCommentApisV1CommentCreatePost({ body: data }));
  },

  async deleteComment(commentId: number): Promise<void> {
    await apiCall(() =>
      deleteCommentApisV1CommentDeleteCommentIdDelete({
        path: { comment_id: commentId },
      }),
    );
  },

  async updateComment(
    commentId: number,
    data: CommentCreate,
  ): Promise<Comment> {
    return apiCall(() =>
      updateCommentApisV1CommentUpdateCommentIdPut({
        path: { comment_id: commentId },
        body: data,
      }),
    );
  },
};
