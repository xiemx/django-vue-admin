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
          :data="nodeList"
          height="100vh"
          style="width: 100%"
          :default-sort="{
            prop: 'metadata.name',
            order: 'descending',
          }"
          ref="filterTable"
          :stripe="is_stripe"
        >
          <el-table-column
            sortable
            prop="metadata.name"
            label="name"
            align="center"
          >
          </el-table-column>

          <el-table-column
            sortable
            prop="status.capacity.cpu"
            label="CPU"
            width="60px"
          >
          </el-table-column>

          <el-table-column
            sortable
            prop="status.capacity.memory"
            label="Memory"
            width="180"
          >
          </el-table-column>

          <el-table-column label="annotations">
            <template slot-scope="scope">
              <el-tag
                v-for="(value, key) in scope.row.metadata.annotations"
                v-if="key !== 'cattle.io/status'"
                type="danger"
                :key="key"
                >{{ key }}: {{ value }}
              </el-tag></template
            >
          </el-table-column>

          <el-table-column
            :filters="label_filters"
            :filter-method="filterHandler"
            label="labels"
          >
            <template slot-scope="scope">
              <el-tag
                v-for="(label, key) in scope.row.metadata.labels"
                type="warning"
                :key="key"
                >{{ key }}: {{ label }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="node_info">
            <template slot-scope="scope">
              <el-tag
                v-for="(label, key) in scope.row.status.node_info"
                type="warning"
                :key="key"
                >{{ key }}: {{ label }}
              </el-tag>
            </template> </el-table-column
          >>

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
          <el-table-column label="yaml" width="100px" align="center">
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
import { nodes } from "@/api/k8s/node";
import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusterList: [],
      nodeList: [],
      activeName: "",
      is_stripe: true,
      label_filters: [],
      node_filters: [],
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
      this.label_filters = [];
      var cluster_name = tab.name;
      nodes(cluster_name).then((response) => {
        this.nodeList = response.data.items;
        var tmp = new Set();
        this.nodeList.forEach((node) => {
          if (node.metadata.labels["nodetype"]) {
            tmp.add(node.metadata.labels["nodetype"]);
          }
        });
        tmp.forEach((item) => {
          this.label_filters.push({
            text: item,
            value: item,
          });
        });
      });
    },
    filterHandler(value, row, column) {
      return row.metadata.labels["nodetype"] === value;
    },
  },
};
</script>
