import { defineStore } from "pinia";

// 定义状态类型接口
interface IUserState {
  id: string;
  name: string;
  roles: string[];
}

export const useUserStore = defineStore("user", {
  state: (): IUserState => ({
    id: "",
    name: "Guest",
    roles: [],
  }),
  actions: {
    // 带参数的方法需明确类型
    setUserInfo(payload: { id: string; name: string }) {
      this.id = payload.id;
      this.name = payload.name;
    },
  },
  getters: {
    // 自动推断返回类型，也可显式标注
    isAdmin: (state): boolean => state.roles.includes("admin"),
  },
});
