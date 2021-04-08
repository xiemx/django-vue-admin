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
          @change="fetchjob"
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
          :data="jobList"
          height="100vh"
          style="width: 100%"
          :stripe="is_stripe"
        >
          <el-table-column sortable prop="metadata.name" label="name">
          </el-table-column>

          <el-table-column label="labels">
            <template slot-scope="scope">
              <el-tag
                v-for="(label, key) in scope.row.metadata.labels"
                type="warning"
                :key="key"
                >{{ key }}: {{ label }}
              </el-tag>
            </template>
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
          <el-table-column width="100px" label="yaml">
            <template slot-scope="scope">
              <el-popover placement="bottom" width="70%" trigger="click">
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
import { namespaces } from "@/api/k8s/namespace";
import { jobs } from "@/api/k8s/job";

import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusterList: [],
      nsList: [],
      jobList: [],
      is_stripe: true,
      activeCluster: "",
      activeNamespace: "",
      value: "",
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
    fetchjob(namespace) {
      this.activeNamespace = namespace;
      jobs(this.activeCluster, this.activeNamespace).then((response) => {
        this.jobList = response.data.items;
      });
    },
  },
};
</script>
