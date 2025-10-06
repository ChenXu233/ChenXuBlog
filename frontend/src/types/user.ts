export interface User {
  uuid: string;
  username: string;
  email: string;
  avatar_url: string;
}

export interface UserLogin {
  evidence: string;
  password: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password: string;
}

export interface UserRegisterResponse {
  user: User;
}

export interface UserUpdate {
  username: string;
  email: string;
  avatar_url: string;
}

export interface UserLoginResponse {
  user_uuid: string;
  access_token: string;
}
