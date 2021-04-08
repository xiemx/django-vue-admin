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
          @change="fetchcronjob"
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
          :data="cronjobList"
          style="width: 100%"
          height="100vh"
          border
          :stripe="is_stripe"
        >
          <el-table-column
            sortable
            prop="metadata.name"
            label="name"
            align="left"
          >
          </el-table-column>
          <el-table-column
            sortable
            prop="spec.concurrency_policy"
            label="concurrency_policy"
          >
            <template slot-scope="scope"
              >{{ scope.row.spec.concurrency_policy }}
            </template>
          </el-table-column>

          <el-table-column label="schedule">
            <template slot-scope="scope">
              {{ scope.row.spec.schedule }}
            </template>
          </el-table-column>
          <el-table-column label="suspend" width="100px">
            <template slot-scope="scope">
              <el-switch
                v-model="scope.row.spec.suspend"
                active-color="#13ce66"
                inactive-color="#ff4949"
                disabled
              >
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column
            sortable
            prop="spec.failed_jobs_history_limit"
            label="failed_history_limit"
          >
          </el-table-column>
          <el-table-column
            sortable
            prop="spec.successful_jobs_history_limit"
            label="successful_history_limit"
          >
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
import { Pagination } from "@/components/Pagination";
import { clusters } from "@/api/k8s/cluster";
import { namespaces } from "@/api/k8s/namespace";
import { cronjobs } from "@/api/k8s/cronjob";

import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusterList: [],
      nsList: [],
      cronjobList: [],
      is_stripe: true,
      total: 500,
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
      clusters()
        .then((response) => {
          console.log(response);
          this.clusterList = response.data.items;
        })
        .catch((err) => {
          console.log(err);
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
    fetchcronjob(namespace) {
      this.activeNamespace = namespace;
      cronjobs(this.activeCluster, this.activeNamespace).then((response) => {
        this.cronjobList = response.data.items;
      });
    },
  },
};
</script>
