<template>
  <div class="dashboard-editor-container">
    <panel-group />

    <el-row style="background: #fff; padding: 16px 16px 0; margin-bottom: 32px">
      <line-chart :chart-data="lineChartData" />
    </el-row>

    <el-row :gutter="32">
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 12 }"
        :md="{ span: 12 }"
        :lg="{ span: 4 }"
        :xl="{ span: 4 }"
        style="margin-bottom: 30px"
      >
        <div>
          <h3>常用组件快捷入口</h3>
          <el-button
            class="tip-button"
            type="success"
            :key="item.name"
            v-for="item in ex_linker"
            @click="handleClick(item.address)"
            >{{ item.name }}</el-button
          >
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="10">
        <div class="chart-wrapper">
          <raddar-chart />
        </div>
      </el-col>

      <el-col :xs="24" :sm="24" :lg="10">
        <div class="chart-wrapper">
          <pie-chart />
        </div>
      </el-col>
      <!-- <el-col :xs="24" :sm="24" :lg="7">
        <div class="chart-wrapper">
          <bar-chart />
        </div>
      </el-col> -->
    </el-row>

    <el-row :gutter="8">
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 24 }"
        :lg="{ span: 10 }"
        :xl="{ span: 12 }"
        style="padding-right: 8px; margin-bottom: 30px"
      >
        <transaction-table :list="taskResultlist.slice(0, 16)" />
      </el-col>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 12 }"
        :md="{ span: 12 }"
        :lg="{ span: 12 }"
        :xl="{ span: 12 }"
        style="margin-bottom: 30px"
      >
        <div>
          <!-- <todo-list /> -->
          <timeline :activities="auditOperationList" :reverse="reverse" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from "./components/PanelGroup";
import LineChart from "./components/LineChart";
import RaddarChart from "./components/RaddarChart";
import PieChart from "./components/PieChart";
import BarChart from "./components/BarChart";
import TransactionTable from "./components/TransactionTable";
// import TodoList from "./components/TodoList";
import Timeline from "@/components/Timeline";

import * as result from "@/api/job/task/result";
import * as audit from "@/api/audit";

export default {
  name: "DashboardAdmin",
  components: {
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart,
    TransactionTable,
    // TodoList,
    Timeline,
  },
  created() {
    // 获取最近7天的数据
    var start_day = new Date();
    var end_day = new Date();
    start_day.setTime(start_day.getTime() - 7 * 24 * 3600 * 1000);

    this.fetchtaskResult({
      time_range: [start_day.toISOString(), end_day.toISOString()],
    });
    this.fetchAudit();
  },
  data() {
    return {
      ex_linker: [
        {
          name: "Grafana",
          address: "https://grafana.xiemx.com/",
        },
        {
          name: "Gitlab",
          address: "https://gitlab.com/",
        },
        {
          name: "APM",
          address: "https://apm.xiemx.xyz/",
        },
        {
          name: "Teambition",
          address: "https://www.teambition.com/",
        },
        {
          name: "Thoughts",
          address: "https://thoughts.teambition.com/",
        },
      ],
      lineChartData: {
        actualData: [120, 82, 91, 154, 162, 140, 130],
      },
      taskResultlist: [],
      reverse: false,
      auditOperationList: [],
    };
  },
  methods: {
    handleClick(address) {
      window.open(address, "_blank");
    },

    fetchtaskResult(kwargs) {
      result.list(kwargs).then((response) => {
        this.taskResultlist = response.data.items;
        // this.taskResultlist.forEach((item) => {
        //   console.log(kwargs, item.date_done);
        // });
      });
    },
    fetchAudit() {
      audit
        .list({
          limit: 5,
        })
        .then((response) => {
          this.auditOperationList = response.data.items;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.tip-button {
  margin-bottom: 10px;
  position: relative;
}
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
