export interface User {
  id: number
  uuid: string
  username: string
  email: string
  bio?: string
  avatar?: string
}

export interface UserLogin {
  evidence: string
  password: string
}

export interface UserRegister {
  username: string
  email: string
  password: string
}

export interface UserLoginResponse {
  user_uuid: string
  access_token: string
}