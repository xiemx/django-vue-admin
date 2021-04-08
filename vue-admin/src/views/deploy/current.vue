<template>
  <div class="app-container">
    <el-tabs v-model="activeCluster" type="card" @tab-click="fetchNamespace">
      <el-tab-pane
        v-for="cluster in clusterList"
        :label="cluster.displayname"
        :name="cluster.name"
        :key="cluster.name"
      >
        <el-select
          v-model="value"
          placeholder="请选择 NameSpace "
          @change="fetchRelease"
        >
          <el-option
            v-for="item in nsList"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-table
          :data="releaseList"
          height="100vh"
          style="width: 100%"
          :stripe="is_stripe"
          @expand-change="handleHistory"
        >
          <el-table-column type="expand">
            <template slot-scope="scope">
              <el-table :data="historyList">
                <el-table-column prop="revision" label="revision">
                </el-table-column>
                <el-table-column prop="description" label="description">
                </el-table-column>

                <el-table-column prop="status" label="status">
                </el-table-column>

                <el-table-column prop="updated" label="updated">
                  <template slot-scope="scope">
                    <el-date-picker
                      disabled
                      v-model="scope.row.updated"
                      type="datetime"
                      placeholder="暂无数据"
                    >
                    </el-date-picker>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column sortable prop="name" label="name"> </el-table-column>
          <el-table-column sortable prop="chart" label="chart">
          </el-table-column>
          <el-table-column sortable prop="app_version" label="app_version">
          </el-table-column>
          <el-table-column sortable prop="revision" label="revision">
          </el-table-column>
          <el-table-column sortable prop="status" label="status">
          </el-table-column>

          <el-table-column sortable prop="updated" label="updated">
            <template slot-scope="scope">
              <el-date-picker
                disabled
                v-model="scope.row.updated"
                type="datetime"
                placeholder="暂无数据"
              >
              </el-date-picker>
            </template>
          </el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="danger"
                @click="handleRollback(scope.row)"
                >回滚</el-button
              >

              <el-dialog
                :modal="is_modal"
                title="回滚信息"
                :visible.sync="dialogFormVisible"
              >
                <el-form :model="form">
                  <el-form-item label="cluster" :label-width="formLabelWidth">
                    <el-input v-model="form.cluster" disabled></el-input>
                  </el-form-item>
                  <el-form-item label="namespace" :label-width="formLabelWidth">
                    <el-input v-model="form.namespace" disabled></el-input>
                  </el-form-item>
                  <el-form-item label="service" :label-width="formLabelWidth">
                    <el-input v-model="form.service" disabled></el-input>
                  </el-form-item>
                  <el-form-item label="revision" :label-width="formLabelWidth">
                    <el-select v-model="form.revision" placeholder="请选择">
                      <el-option
                        v-for="item in historyFilter"
                        :key="item.revision"
                        :label="item.revision + ' | ' + item.status"
                        :value="item.revision"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="dialogFormVisible = false"
                    >取 消</el-button
                  >
                  <el-button type="primary" @click="postHandleRollback"
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
import * as release from "@/api/deploy/release";

export default {
  data() {
    return {
      clusterList: [],
      nsList: [],
      releaseList: [],
      historyList: [],
      historyFilter: [],
      is_stripe: true,
      is_modal: false,
      activeCluster: "",
      activeNamespace: "",
      value: "",
      formLabelWidth: "10%",
      dialogFormVisible: false,
      form: {
        service: "",
        revision: "",
        namespace: "",
        cluster: "",
      },
    };
  },
  created() {
    this.fetchCluster();
    // this.fetchNamespace();
  },
  methods: {
    fetchCluster() {
      clusters().then((response) => {
        this.clusterList = response.data.items;
      });
    },
    fetchNamespace(tab) {
      this.activeCluster = tab.name;
      namespaces(tab.name).then((response) => {
        response.data.items.forEach((item, index) => {
          this.nsList.push({
            value: item.metadata.name,
            value: item.metadata.name,
          });
        });
      });
    },
    fetchRelease(namespace) {
      this.activeNamespace = namespace;
      release
        .list({
          cluster: this.activeCluster,
          namespace: this.activeNamespace,
          type: "current",
        })
        .then((response) => {
          this.releaseList = response.data.items;
        });
    },
    handleHistory(row, expandedRows) {
      console.log(expandedRows.length);
      if (expandedRows.length) {
        release
          .list({
            cluster: this.activeCluster,
            namespace: this.activeNamespace,
            type: "history",
            service: row.name,
          })
          .then((response) => {
            this.historyList = response.data.items;
          });
      }
    },
    handleRollback(row) {
      this.form.service = row.name;
      this.form.cluster = this.activeCluster;
      this.form.namespace = this.activeNamespace;
      this.dialogFormVisible = !this.dialogFormVisible;
      release
        .list({
          cluster: this.activeCluster,
          namespace: this.activeNamespace,
          type: "history",
          service: row.name,
        })
        .then((response) => {
          this.historyFilter = response.data.items;
        });
    },
    postHandleRollback() {
      release.create(this.form).then((response) => {});
      this.dialogFormVisible = !this.dialogFormVisible;
    },
  },
};
</script>
