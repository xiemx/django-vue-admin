<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID">
        >
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="username">
        <template slot-scope="scope">
          {{ scope.row.username }}
        </template>
      </el-table-column>
      <el-table-column label="Email" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column label="钉钉" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.profile">{{ scope.row.profile.dingding }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="profile" label="手机号" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.profile">{{ scope.row.profile.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="profile" label="阿里云 ID" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.profile">{{ scope.row.profile.alicloud }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="profile" label="avatar" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.profile">
            <el-image
              style="width: 50px; height: 50px"
              :src="scope.row.profile.avatar"
            ></el-image>
          </span>
        </template>
      </el-table-column>
      <el-table-column label="groups" align="center">
        <template slot-scope="scope">
          <el-tag v-for="group in scope.row.groups" :key="group">{{
            group
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" align="center">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            active-color="#13ce66"
            inactive-color="#ff4949"
            disabled
          >
          </el-switch>
        </template>
      </el-table-column>
      <!-- <el-table-column align="center" prop="created_at" label="Last_login">
        <template slot-scope="scope">
          <span>{{ scope.row.last_login }}</span>
        </template>
      </el-table-column> -->

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
          <el-dialog title="用户信息" :visible.sync="dialogFormVisible">
            <el-form :model="form">
              <el-form-item label="用户名" :label-width="formLabelWidth">
                <el-input
                  v-model="form.username"
                  autocomplete="off"
                  disabled
                  :placeholder="scope.row.username"
                ></el-input>
              </el-form-item>
              <el-form-item label="用户组" :label-width="formLabelWidth">
                <el-select v-model="form.groups" multiple placeholder="请选择">
                  <el-option
                    v-for="group in all_groups"
                    :key="group.id"
                    :label="group.name"
                    :value="group.name"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="邮箱" :label-width="formLabelWidth">
                <el-input v-model="form.email" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="状态" :label-width="formLabelWidth">
                <el-switch
                  v-model="form.is_active"
                  active-text="启用"
                  inactive-text="禁用"
                >
                </el-switch>
              </el-form-item>
              <el-form-item label="阿里云 ID" :label-width="formLabelWidth">
                <el-input
                  v-model="form.profile.alicloud"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="钉钉" :label-width="formLabelWidth">
                <el-input
                  v-model="form.profile.dingding"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="手机号" :label-width="formLabelWidth">
                <el-input
                  v-model="form.profile.phone"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="Avatar" :label-width="formLabelWidth">
                <el-input
                  v-model="form.profile.avatar"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="handleCancel">取 消</el-button>
              <el-button type="primary" @click="postEditUser">确 定</el-button>
            </div>
          </el-dialog>

          <el-button
            size="mini"
            type="danger"
            disabled
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { users, editUser } from "@/api/user";
import { groups } from "@/api/group";

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: "success",
        draft: "gray",
        deleted: "danger",
      };
      return statusMap[status];
    },
  },
  data() {
    return {
      list: null,
      listLoading: true,
      dialogFormVisible: false,

      form: {
        username: "",
        groups: "",
        email: "",
        is_active: false,
        profile: {
          dingding: "",
          avatar: "",
          alicloud: "",
          phone: "",
        },
      },
      formLabelWidth: "80px",
      all_groups: [],
    };
  },
  created() {
    this.fetchData();
    this.fetchGroups();
  },
  methods: {
    fetchData() {
      this.listLoading = true;
      users().then((response) => {
        this.list = response.data.items;
        this.listLoading = false;
      });
    },
    fetchGroups() {
      groups().then((response) => {
        this.all_groups = response.data.items;
      });
    },
    handleEdit(row) {
      if (!row.profile) {
        row.profile = {};
      }
      this.form = row;

      this.dialogFormVisible = !this.dialogFormVisible;
    },
    postEditUser() {
      editUser(this.form).then((res) => {});

      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleCancel() {
      this.form = { profile: {} };
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleDelete(index, row) {},
  },
};
</script>
