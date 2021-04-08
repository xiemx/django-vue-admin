<template>
  <div class="app-container">
    <el-tabs v-model="active_cluster" type="card" @tab-click="handleClick">
      <el-tab-pane
        v-for="cluster in cluster_list"
        :label="cluster.displayname"
        :name="cluster.name"
        :key="cluster.name"
      >
        <el-table
          v-loading="listLoading"
          :data="rbac_list"
          element-loading-text="Loading"
          border
          fit
          highlight-current-row
        >
          <el-table-column align="center" label="username">
            <template slot-scope="scope">
              {{ scope.row.username }}
            </template>
          </el-table-column>

          <el-table-column label="ClusterRole" align="center">
            <template slot-scope="scope">
              <el-tag v-for="role in scope.row.cluster_role" :key="role">{{
                role
              }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Role" align="center">
            <template slot-scope="scope">
              <el-tag
                v-for="(namesapce, index) in scope.row.namespace"
                :key="index"
                >{{ namesapce }}</el-tag
              >
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="success"
                @click="handleEdit(scope.row)"
                >编辑</el-button
              >
              <el-dialog
                title="用户信息"
                :visible.sync="dialogFormVisible"
                :modal="is_modal"
              >
                <el-form :model="form">
                  <el-form-item label="用户名" :label-width="formLabelWidth">
                    <el-input
                      v-model="form.username"
                      autocomplete="off"
                      disabled
                      :placeholder="scope.row.username"
                    ></el-input>
                  </el-form-item>
                  <el-form-item
                    label="ClusterRole"
                    :label-width="formLabelWidth"
                  >
                    <el-select
                      v-model="form.cluster_role"
                      multiple
                      filterable
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="item in clusterrole_list"
                        :key="item.metadata.name"
                        :label="item.metadata.name"
                        :value="item.metadata.name"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="Role" :label-width="formLabelWidth">
                    <el-checkbox-group v-model="form.namespace">
                      <el-checkbox
                        v-for="ns in namespace_list"
                        :label="ns.metadata.name"
                        :key="ns.metadata.name"
                      ></el-checkbox>
                    </el-checkbox-group>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="handleCancel">取 消</el-button>
                  <el-button type="primary" @click="postEditUser"
                    >确 定</el-button
                  >
                </div>
              </el-dialog>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { clusters } from "@/api/k8s/cluster";
import { namespaces } from "@/api/k8s/namespace";
import { k8sRBAC } from "@/api/rbac-k8s";
import { clusterRoles } from "@/api/k8s/cluster-role";
export default {
  data() {
    return {
      list: null,
      listLoading: true,
      is_modal: false,
      dialogFormVisible: false,
      form: {
        username: "",
        namespace: [],
        cluster_role: [],
      },
      formLabelWidth: "100px",
      active_cluster: "",
      cluster_list: [],
      rbac_list: [],
      namespace_list: [],
      clusterrole_list: [],
    };
  },
  created() {
    this.fetchCluster();
  },

  methods: {
    // fetchUser() {
    //   this.listLoading = true;
    //   users().then((response) => {
    //     this.user_list = response.data.items;
    //     this.listLoading = false;
    //   });
    // },
    fetchCluster() {
      clusters().then((response) => {
        this.cluster_list = response.data.items;
      });
    },
    fetchK8SRBAC() {
      this.listLoading = true;
      k8sRBAC(this.active_cluster).then((response) => {
        this.rbac_list = response.data.items;
        this.listLoading = false;
      });
    },
    fetchNamespace() {
      namespaces(this.active_cluster).then((response) => {
        this.namespace_list = response.data.items;
      });
    },
    fetchClusterRole() {
      clusterRoles(this.active_cluster).then((response) => {
        this.clusterrole_list = response.data.items;
      });
    },
    handleClick() {
      this.rbac_list = [];
      this.fetchK8SRBAC();
      this.fetchClusterRole();
    },
    handleEdit(row) {
      this.form = row;
      this.fetchNamespace();
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    postEditUser() {
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleCancel() {
      this.form = {};
      this.dialogFormVisible = !this.dialogFormVisible;
    },
  },
};
</script>
