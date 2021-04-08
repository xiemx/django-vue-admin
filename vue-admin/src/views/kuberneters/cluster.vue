<template>
  <div class="app-container">
    <el-table :data="clusters" style="width: 100%">
      <el-table-column
        prop="name"
        sortable
        label="name"
        width="180"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="displayname"
        sortable
        label="displayname"
        width="180"
      >
      </el-table-column>
      <el-table-column prop="api_endpoint" sortable label="api_endpoint">
      </el-table-column>
      <el-table-column
        prop="description"
        sortable
        label="description"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="create_time"
        sortable
        label="create_time"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="update_time"
        sortable
        label="update_time"
        align="center"
      >
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
      <el-table-column
        prop="config"
        sortable
        label="config"
        width="180"
        align="center"
      >
        <template slot-scope="scope">
          <el-popover placement="left" width="70%" trigger="click">
            <json-view :data="scope.row.config" />

            <el-button type="success" slot="reference"
              >查看KubeConfing</el-button
            >
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { clusters } from "@/api/k8s/cluster";
import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusters: [],
    };
  },
  created() {
    this.fetchCluster();
  },
  methods: {
    fetchCluster() {
      clusters().then((response) => {
        this.clusters = response.data.items;
      });
    },
    resetDateFilter() {
      this.$refs.filterTable.clearFilter("date");
    },
    clearFilter() {
      this.$refs.filterTable.clearFilter();
    },
    formatter(row, column) {
      return row.address;
    },
    filterTag(value, row) {
      return row.tag === value;
    },
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
  },
};
</script>
