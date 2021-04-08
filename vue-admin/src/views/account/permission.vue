<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="groups"
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
      <el-table-column
        class-name="status-col"
        label="Permission"
        align="center"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <el-tag
            v-for="permission in scope.row.permissions"
            :key="permission"
            >{{ permission }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleEdit(scope.row)"
            >编辑</el-button
          >

          <el-dialog
            title="编辑权限"
            :visible.sync="dialogFormVisible"
            destroy-on-close
            width="30%"
          >
            <el-form :model="form">
              <el-form-item label="组名" >
                <el-input v-model="form.name" disabled autocomplete="off"></el-input>
              </el-form-item>
  
              </el-form-item>
            </el-form>
            <div slot="">
              <el-transfer
                filterable
                :titles="titles"
                :filter-method="filterMethod"
                filter-placeholder="输入搜索关键字"
                v-model="choicePerms"
                :data="perms"
              >
              </el-transfer>
            </div>

            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="postHandleEdit"
                >确 定</el-button
              >
            </div>
          </el-dialog>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { groups, update } from "@/api/group";
import { permissions } from "@/api/permission";
import store from "@/store";

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
      perms: [],
      choicePerms: [],
      filterMethod(query, item) {
        return item.pinyin.indexOf(query) > -1;
      },
      form: {
        id: "",
        permissions: [],
        name: "",
      },
      groups: [],
      listLoading: true,
      userlist: [],
      dialogFormVisible: false,
      titles: ["未授权", "已授权"],
    };
  },
  created() {
    this.fetchGroups();
    this.fetchPermissions();
  },
  methods: {
    fetchGroups() {
      this.listLoading = true;
      groups().then((response) => {
        this.groups = response.data.items;
        this.listLoading = false;
      });
    },
    fetchPermissions() {
      permissions().then((response) => {
        response.data.items.forEach((item, index) => {
          this.perms.push({
            label: item.name,
            key: item.name,
            pinyin: item.name,
          });
        });
        this.perms;
      });
    },

    handleEdit(row) {
      this.form = row;
      this.choicePerms = row.permissions;
      this.dialogFormVisible = !this.dialogFormVisible;
    },

    postHandleEdit() {
      this.form.permissions = this.choicePerms;
      update(this.form).then((response) => {});
      this.dialogFormVisible = !this.dialogFormVisible;
    },
  },
};
</script>
