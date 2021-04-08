<template>
  <div class="app-container">
    <el-button type="success" @click="handleClick">更新白名单</el-button>
    <el-table
      :data="examList"
      height="85vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>
      <el-table-column sortable prop="task_id" label="task_id" align="center">
        <template slot-scope="scope">{{ scope.row.task_id }} </template>
      </el-table-column>
      <el-table-column sortable prop="user" label="user" align="center">
        <template slot-scope="scope"
          ><el-tag type="danger">{{ scope.row.user }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column sortable prop="status" label="status" align="center">
        <template slot-scope="scope"
          ><el-tag type="warning">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column sortable label="creation_timestamp">
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
      <el-table-column sortable label="update_time" align="center">
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
    <pagination
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="fetchTask"
    />
  </div>
</template>

<script>
import { list, create } from "@/api/toolkit/ingress-whitelist";
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination },
  data() {
    return {
      examList: [],
      is_stripe: true,
      total: 0,
      listQuery: {
        page: 1,
        limit: 20,
      },
    };
  },
  created() {
    this.fetchTask();
  },
  methods: {
    fetchTask() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      list({
        limit: this.listQuery.limit,
        offset,
      }).then((response) => {
        this.total = response.data.total;
        this.examList = response.data.items;
      });
    },
    handleClick() {
      create().then((response) => {
        this.fetchTask();
      });
    },
  },
};
</script>
