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
          <el-table-column sortable prop="metadata.name" label="name">
            <template slot-scope="scope">
              {{ scope.row.metadata.name }}
            </template>
          </el-table-column>

          <el-table-column sortable label="annotations">
            <template slot-scope="scope">
              <el-tag
                v-for="(value, key) in scope.row.metadata.annotations"
                v-if="
                  ![
                    'cattle.io/status',
                    'kubectl.kubernetes.io/last-applied-configuration',
                  ].includes(key)
                "
                type="danger"
                :key="key"
              >
                {{ key }}: {{ value }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="labels">
            <template slot-scope="scope">
              <el-tag
                v-for="(label, key) in scope.row.metadata.labels"
                type="warning"
                :key="key"
              >
                {{ key }}: {{ label }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column
            sortable
            prop="metadata.creation_timestamp"
            label="creation_timestamp"
          >
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
          <el-table-column label="yaml" width="100px">
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
import { clusterRoles } from "@/api/k8s/cluster-role";
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
      clusterRoles(cluster_name).then((response) => {
        this.nsList = response.data.items;
      });
    },
  },
};
</script>
