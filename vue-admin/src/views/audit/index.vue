<template>
  <div class="app-container">
    <div style="width: 100%">
      <div class="filter">
        <span class="tips">User: </span>
        <el-input
          v-model="filter.username"
          clearable
          placeholder="请输入 username"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">Operation: </span>
        <el-input
          v-model="filter.operation"
          clearable
          placeholder="请输入 operation"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">Resource: </span>
        <el-input
          v-model="filter.resource"
          clearable
          placeholder="请输入 resource"
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

    <div class="radio">
      排序：
      <el-radio-group v-model="reverse">
        <el-radio :label="true">倒序</el-radio>
        <el-radio :label="false">正序</el-radio>
      </el-radio-group>
    </div>

    <Timeline :activities="auditOperationList" :reverse="reverse" />

    <!-- <el-table
      :data="auditOperationList"
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
      <el-table-column sortable label="user" prop="user" align="center">
      </el-table-column>
      <el-table-column
        sortable
        label="operation"
        prop="operation"
        align="center"
      >
      </el-table-column>
      <el-table-column sortable label="resource" prop="resource" align="center">
      </el-table-column>
      <el-table-column sortable label="content" prop="content" align="center">
        <template slot-scope="scope">
          {{ scope.row.content }}
        </template>
      </el-table-column>
      <el-table-column sortable label="before" prop="before" align="center">
        <template slot-scope="scope">
          {{ scope.row.before }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        label="create_time"
        prop="create_time"
        align="center"
      >
        <template slot-scope="scope">
          <el-date-picker
            disabled
            v-model="scope.row.create_time"
            type="datetime"
            placeholder="暂无数据"
          >
          </el-date-picker>
        </template>
      </el-table-column>
      >
    </el-table> -->
    <pagination
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="fetchAudit"
    />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import Timeline from "@/components/Timeline";

import { list } from "@/api/audit";
export default {
  components: { Pagination, Timeline },

  data() {
    return {
      auditOperationList: [],
      total: 0,
      reverse: false,
      filter: {
        username: null,
        operation: null,
        resource: null,
        time_range: [],
      },
      listQuery: {
        page: 1,
        limit: 20,
      },
    };
  },
  created() {
    this.fetchAudit();
  },
  methods: {
    fetchAudit() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;

      list({
        limit: this.listQuery.limit,
        offset,
        username: this.filter.username,
        operation: this.filter.operation,
        resource: this.filter.resource,
        time_range: this.filter.time_range,
      }).then((response) => {
        this.total = response.data.total;
        this.auditOperationList = response.data.items;
      });
    },
    handleSearch() {
      this.fetchAudit();
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

.radio {
  margin-top: 10px;
  margin-bottom: 10px;
}

/* .el-table .success-row {
  background: #f0f9eb;
} */
/* .cell {
} */
</style>