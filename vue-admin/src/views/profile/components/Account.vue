<template>
  <el-form>
    <el-form>
      <el-form-item label="用户名" :label-width="formLabelWidth">
        <el-input
          v-model="user.username"
          disabled
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="邮箱" :label-width="formLabelWidth">
        <el-input v-model="user.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="阿里云 ID" :label-width="formLabelWidth">
        <el-input
          v-if="user.profile"
          v-model="user.profile.alicloud"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="钉钉" :label-width="formLabelWidth">
        <el-input
          v-if="user.profile"
          v-model="user.profile.dingding"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="手机号" :label-width="formLabelWidth">
        <el-input
          v-if="user.profile"
          v-model="user.profile.phone"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="Avatar" :label-width="formLabelWidth">
        <el-input
          v-if="user.profile"
          v-model="user.profile.avatar"
          autocomplete="off"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-form-item>
      <el-button type="primary" @click="submit(user)">Update</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { editUser } from "@/api/user";
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          username: "",
          email: "",
          profile: { alicloud: "", dingding: "", phone: "" },
        };
      },
    },
  },
  methods: {
    submit(user) {
      editUser(user);
    },
  },
  data() {
    return {
      formLabelWidth: "100",
    };
  },
};
</script>
