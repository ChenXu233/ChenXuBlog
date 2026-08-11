// 与后端 openapi.json 生成的类型保持一致（UserResponse）
export interface User {
  uuid: string;
  username: string;
  email: string;
  avatar?: string | null;
  bio?: string | null;
}
