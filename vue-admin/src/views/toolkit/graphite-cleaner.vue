<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">清理 Storage</el-button>

    <el-table
      :data="taskResultlist"
      height="85vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable prop="id" label="id" align="center">
      </el-table-column>
      <el-table-column sortable prop="task_id" label="task_id" align="center">
        <template slot-scope="scope">{{ scope.row.task_id }} </template>
      </el-table-column>
      <el-table-column sortable prop="user" label="user" align="center">
        <template slot-scope="scope"
          ><el-tag type="danger">{{ scope.row.user }}</el-tag>
        </template>
      </el-table-column>
      >

      <el-table-column sortable prop="status" label="status" align="center">
        <template slot-scope="scope">
          <el-tag type="warning">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>

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
      <el-table-column
        sortable
        prop="update_time"
        label="update_time"
        align="center"
      >
        <template slot-scope="scope">
          <el-date-picker
            disabled
            v-model="scope.row.update_time"
            type="datetime"
            placeholder="暂无数据"
          >
          </el-date-picker
        ></template>
      </el-table-column>
      >
    </el-table>
    <div>
      <pagination
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="fetchtask"
      />
    </div>
  </div>
</template>

<script>
import { list, create } from "@/api/toolkit/graphite-cleaner";
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination },
  data() {
    return {
      total: 0,
      listQuery: {
        page: 1,
        limit: 20,
      },
      taskResultlist: [],
      is_stripe: true,
    };
  },
  created() {
    this.fetchtask();
  },
  methods: {
    fetchtask() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      list({
        limit: this.listQuery.limit,
        offset,
      }).then((response) => {
        this.total = response.data.total;
        this.taskResultlist = response.data.items;
      });
    },
    handleCreate() {
      create(this.form).then((response) => {
        this.dialogFormVisible = !this.dialogFormVisible;
        this.fetchtask();
      });
    },
  },
};
</script>
