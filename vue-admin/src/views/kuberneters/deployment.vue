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
          @change="fetchDeployment"
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
          :data="deploymentList"
          height="100vh"
          border
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
          <!-- <el-table-column sortable prop="metadata.namespace" label="namespace">
            <template slot-scope="scope">
              {{ scope.row.metadata.namespace }}
            </template>
          </el-table-column> -->

          <el-table-column
            sortable
            prop="spec.replicas"
            label="replicas"
            width="100"
          >
            <template slot-scope="scope">
              {{ scope.row.spec.replicas }}
            </template>
          </el-table-column>

          <el-table-column label="containers" width="180">
            <template slot-scope="scope">
              <el-tag
                v-for="container in scope.row.spec.template.spec.containers"
                type="danger"
                :key="container.name"
              >
                {{ container.name }}
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
          <el-table-column label="annotations">
            <template slot-scope="scope">
              <el-tag
                v-for="(value, key) in scope.row.metadata.annotations"
                v-if="key !== 'cattle.io/status'"
                type="danger"
                :key="key"
              >
                {{ key }}: {{ value }}
              </el-tag></template
            >
          </el-table-column>
          <el-table-column
            sortable
            prop="metadata.creation_timestamp"
            label="creation_timestamp"
            align="center"
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
          <el-table-column sortable label="yaml" width="100px">
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
import { deployments } from "@/api/k8s/deployment";

import jsonView from "vue-json-views";
export default {
  components: {
    jsonView,
  },
  data() {
    return {
      clusterList: [],
      nsList: [],
      deploymentList: [],
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
    fetchDeployment(namespace) {
      this.activeNamespace = namespace;
      deployments(this.activeCluster, this.activeNamespace).then((response) => {
        this.deploymentList = response.data.items;
      });
    },
  },
};
</script>
