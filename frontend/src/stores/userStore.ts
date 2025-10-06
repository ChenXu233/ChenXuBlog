import { defineStore } from "pinia";

// 定义状态类型接口
interface IUserState {
  id: string;
  name: string;
  avatar_url: string;
}

export const useUserStore = defineStore("user", {
  state: (): IUserState => ({
    id: "",
    name: "Guest",
    avatar_url: "",
  }),
  actions: {
    // 带参数的方法需明确类型
    setUserInfo(payload: { id: string; name: string }) {
      this.id = payload.id;
      this.name = payload.name;
    },
  },
  getters: {},
});
