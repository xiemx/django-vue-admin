<template>
  <div class="app-container">
    <el-button type="success" @click="dialogFormVisible = true"
      >创建用户组</el-button
    >
    <el-dialog title="用户组信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="组名" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="用户" :label-width="formLabelWidth">
          <el-select v-model="form.users" multiple placeholder="请选择用户">
            <el-option
              v-for="user in userlist"
              :label="user.username"
              :value="user.username"
              :key="user.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCreate">确 定</el-button>
      </div>
    </el-dialog>

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
      <el-table-column label="Name">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      >
      <el-table-column class-name="status-col" label="Users" align="center">
        <template slot-scope="scope">
          <el-tag v-for="user in scope.row.users" :key="user">{{
            user
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleEdit(scope.row)"
            >编辑</el-button
          >
          <el-dialog title="用户组信息" :visible.sync="editDialogFormVisible">
            <el-form :model="form">
              <el-form-item label="组名" :label-width="formLabelWidth">
                <el-input
                  v-model="form.name"
                  disabled
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="用户" :label-width="formLabelWidth">
                <el-select
                  v-model="form.users"
                  multiple
                  placeholder="请选择用户"
                >
                  <el-option
                    v-for="user in userlist"
                    :label="user.username"
                    :value="user.username"
                    :key="user.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="editDialogFormVisible = false"
                >取 消</el-button
              >
              <el-button type="primary" @click="postHandleEdit"
                >确 定</el-button
              >
            </div>
          </el-dialog>
          <el-button
            v-if="scope.row.name === 'admin'"
            size="mini"
            disabled
            type="danger"
            @click="handleDelete(scope.row)"
            >删除</el-button
          >
          <el-button
            v-else
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { groups, create, update, deleted } from "@/api/group";
import { users } from "@/api/user";

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
      editDialogFormVisible: false,
      form: {
        name: "",
        permissions: [],
        users: [],
      },
      userlist: [],
      formLabelWidth: "120px",
      visible: false,
    };
  },
  created() {
    this.fetchData();
    this.fetchUsers();
  },
  methods: {
    fetchData() {
      this.listLoading = true;
      groups().then((response) => {
        console.log(response.data);
        this.list = response.data.items;
        this.listLoading = false;
      });
    },
    fetchUsers() {
      users().then((response) => {
        this.userlist = response.data.items;
      });
    },
    handleCreate() {
      create(this.form).then((response) => {
        groups().then((response) => {
          this.list = response.data.items;
          this.listLoading = false;
        });
      });
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleEdit(row) {
      this.form = row;
      this.editDialogFormVisible = !this.editDialogFormVisible;
    },
    postHandleEdit() {
      update(this.form).then((response) => {});
      this.editDialogFormVisible = !this.editDialogFormVisible;
    },
    handleDelete(row) {
      this.dialogFormVisible = false;
      deleted(row).then((response) => {
        groups().then((response) => {
          this.list = response.data.items;
          this.listLoading = false;
        });
      });
    },
  },
};
</script>
