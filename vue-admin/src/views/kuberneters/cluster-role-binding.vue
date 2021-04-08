<template>
  <div class="app-container">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane
        v-for="cluster in clusterList"
        :label="cluster.displayname"
        :name="cluster.name"
        :key="cluster.name"
      >
        <el-table
          :data="nsList"
          height="100vh"
          style="width: 100%"
          :stripe="is_stripe"
        >
          <el-table-column
            sortable
            prop="metadata.name"
            label="name"
            align="center"
          >
            <template slot-scope="scope">
              {{ scope.row.metadata.name }}
            </template>
          </el-table-column>

          <el-table-column sortable prop="role_ref.name" label="role">
            <template slot-scope="scope">
              <el-tag>
                {{ scope.row.role_ref.kind }}: {{ scope.row.role_ref.name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="user">
            <template slot-scope="scope">
              <el-tag
                v-for="(subjec, index) in scope.row.subjects"
                type="danger"
                :key="index"
              >
                {{ subjec.kind }}: {{ subjec.name }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column sortable label="creation_timestamp">
            <template slot-scope="scope">
              <el-date-picker
                disabled
                v-model="scope.row.metadata.creation_timestamp"
                type="datetime"
                placeholder="暂无数据"
              >
              </el-date-picker>
            </template>
          </el-table-column>
          <el-table-column sortable label="yaml" width="100px">
            <template slot-scope="scope">
              <el-popover placement="bottom" width="100%" trigger="click">
                <div style="height: 100vh; padding: 20px; overflow: auto">
                  <json-view :data="scope.row" />
                </div>

                <el-button type="success" slot="reference">Yaml</el-button>
              </el-popover>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { clusters } from "@/api/k8s/cluster";
import { clusterRoleBindings } from "@/api/k8s/cluster-role-binding";
import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusterList: [],
      nsList: [],
      activeName: "",
      is_stripe: true,
    };
  },
  created() {
    this.fetchCluster();
  },
  methods: {
    fetchCluster() {
      clusters().then((response) => {
        this.clusterList = response.data.items;
      });
    },
    handleClick(tab, event) {
      var cluster_name = tab.name;
      clusterRoleBindings(cluster_name).then((response) => {
        this.nsList = response.data.items;
      });
    },
  },
};
</script>
