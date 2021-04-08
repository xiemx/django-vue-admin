<template>
  <div class="app-container">
    <div style="width: 100%">
      <div class="filter">
        <span class="tips">Service: </span>
        <el-input
          v-model="filter.service"
          clearable
          placeholder="请输入 service"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">user: </span>
        <el-input
          v-model="filter.user"
          clearable
          placeholder="请输入 username"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">cluster: </span>
        <el-input
          v-model="filter.cluster"
          clearable
          placeholder="请输入 cluster"
          style="width: 200px"
        ></el-input>
      </div>
      <div class="filter">
        <span class="tips">namespace: </span>
        <el-input
          v-model="filter.namespace"
          clearable
          placeholder="请输入 namespace"
          style="width: 200px"
        ></el-input>
      </div>
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
      :data="releaseList"
      height="85vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable prop="id" label="id"> </el-table-column>
      <el-table-column sortable prop="service" label="service">
      </el-table-column>

      <el-table-column sortable prop="user" label="user"> </el-table-column>
      <el-table-column sortable prop="cluster" label="cluster">
      </el-table-column>
      <el-table-column sortable prop="namespace" label="namespace">
      </el-table-column>
      <el-table-column prop="description" label="description">
      </el-table-column>
      <el-table-column sortable prop="revision" label="revision">
      </el-table-column>
      <el-table-column sortable prop="task_id" label="task_id">
      </el-table-column>
      <el-table-column sortable prop="status" label="status"> </el-table-column>

      <el-table-column prop="log" label="log"> </el-table-column>

      <el-table-column sortable prop="create_time" label="create_time">
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
      <el-table-column sortable prop="update_time" label="update_time">
        <template slot-scope="scope">
          <el-date-picker
            disabled
            v-model="scope.row.update_time"
            type="datetime"
            placeholder="暂无数据"
          >
          </el-date-picker>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="fetchRelease"
    />
  </div>
</template>

<script>
import * as release from "@/api/deploy/release";
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination },
  data() {
    return {
      releaseList: [],
      is_stripe: true,
      filter: {
        service: null,
        user: null,
        cluster: null,
        namespace: null,
        task_id: null,
        time_range: [],
      },
      listQuery: {
        page: 1,
        limit: 20,
      },
      total: 0,
    };
  },
  created() {
    this.fetchRelease();
  },
  methods: {
    fetchRelease() {
      console.log("filter params", this.filter);
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      release
        .list({
          limit: this.listQuery.limit,
          offset,
          service: this.filter.service,
          user: this.filter.user,
          cluster: this.filter.cluster,
          namespace: this.filter.namespace,
          task_id: this.filter.task_id,
          time_range: this.filter.time_range,
        })
        .then((response) => {
          console.log(response);
          this.total = response.data.total;
          this.releaseList = response.data.items;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleRest() {
      this.filter = {
        service: null,
        user: null,
        cluster: null,
        namespace: null,
        type: null,
        task_id: null,
        time_range: [],
      };
    },
    handleSearch() {
      console.log("filter params", this.filter);
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      release
        .list({
          limit: this.listQuery.limit,
          offset,
          service: this.filter.service,
          user: this.filter.user,
          cluster: this.filter.cluster,
          namespace: this.filter.namespace,
          task_id: this.filter.task_id,
          time_range: this.filter.time_range,
        })
        .then((response) => {
          this.total = response.data.total;
          this.releaseList = response.data.items;
        });
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