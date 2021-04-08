<template>
  <div class="app-container">
    <div style="width: 100%">
      <div class="filter">
        <span class="tips">Task_ID: </span>
        <el-input
          v-model="filter.task_id"
          clearable
          placeholder="请输入 task_id"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">Name: </span>
        <el-input
          v-model="filter.name"
          clearable
          placeholder="请输入 name"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">时间范围: </span>
        <el-date-picker
          v-model="filter.time_range"
          type="datetimerange"
          range-separator="至"
          start-placeholder="任务创建开始日期"
          end-placeholder="任务创建结束日期"
        >
        </el-date-picker>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch"
          >搜索</el-button
        >
        <el-button type="primary" style="margin-left: 1px" @click="handleRest"
          >重置查询条件</el-button
        >
      </div>
    </div>

    <el-table
      :data="taskResultList"
      height="85vh"
      style="width: 100%"
      :row-class-name="tableRowClassName"
      :cell-class-name="tableCellClassName"
    >
      <el-table-column type="expand">
        <template slot-scope="scope"> {{ scope.row }} </template>
      </el-table-column>
      <el-table-column sortable label="id" prop="id" align="center">
      </el-table-column>
      <el-table-column sortable label="task_id" prop="task_id" align="center">
      </el-table-column>
      <el-table-column
        sortable
        label="task_name"
        prop="task_name"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        label="task_args"
        prop="task_args"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        label="task_kwargs"
        prop="task_kwargs"
        align="center"
      >
      </el-table-column>
      <el-table-column sortable label="status" prop="status" align="center">
      </el-table-column>
      <el-table-column sortable label="worker" prop="worker" align="center">
      </el-table-column>
      <el-table-column sortable label="result" prop="result" align="center">
      </el-table-column>
      <el-table-column
        sortable
        label="date_created"
        prop="date_created"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        label="date_done"
        prop="date_done"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        label="traceback"
        prop="traceback"
        align="center"
      >
      </el-table-column>
      <el-table-column sortable label="meta" prop="meta" align="center">
      </el-table-column>
    </el-table>
    <pagination
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="fetchtaskResult"
    />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

import { list } from "@/api/job/task/result";
export default {
  components: { Pagination },

  data() {
    return {
      taskResultList: [],
      total: 0,
      filter: {
        name: null,
        task_id: null,
        time_range: [],
      },
      listQuery: {
        page: 1,
        limit: 20,
      },
    };
  },
  created() {
    this.fetchtaskResult();
  },
  methods: {
    fetchtaskResult() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;

      list({
        limit: this.listQuery.limit,
        offset,
        name: this.filter.name,
        task_id: this.filter.task_id,
        time_range: this.filter.time_range,
      }).then((response) => {
        this.total = response.data.total;
        this.taskResultList = response.data.items;
      });
    },
    handleSearch() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      list({
        limit: this.listQuery.limit,
        offset,
        name: this.filter.name,
        task_id: this.filter.task_id,
        time_range: this.filter.time_range,
      }).then((response) => {
        this.total = response.data.total;
        this.taskResultList = response.data.items;
      });
    },
    handleRest() {
      this.filter = {
        name: null,
        task_id: null,
        time_range: [],
      };
    },
    tableRowClassName({ row, rowindex }) {
      if (row.status === "SUCCESS") {
        return "success-row";
      }
      if (row.status === "FAILURE") {
        return "warning-row";
      }
    },
    tableCellClassName() {
      return "custom-cell";
    },
  },
};
</script>

<style>
.tips {
  color: #8492a6;
  font-size: 14px;
}
.filter {
  display: inline;
  margin-right: 10px;
}

.el-table .warning-row {
  background: oldlace;
}

/* .el-table .success-row {
  background: #f0f9eb;
} */
/* .cell {
} */
</style>