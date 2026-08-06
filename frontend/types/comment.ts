export interface Comment {
  id: number
  blog_id: number
  user_id: number
  content: string
  reply_to_id: number | null
  created_at: string
  updated_at: string
  user?: CommentUser
  replies?: Comment[]
}

export interface CommentUser {
  uuid: string
  username: string
  avatar_url: string
}

export interface CommentCreate {
  blog_id: number
  content: string
  reply_to_id?: number | null
}

export interface CommentsResponse {
  comments: Comment[]
  total: number
}