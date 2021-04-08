<template>
  <div class="app-container">
    <el-button type="success" @click="handleClick">创建考试</el-button>
    <el-table
      :data="examList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>
      <el-table-column sortable label="task_id" align="center">
        <template slot-scope="scope">{{ scope.row.task_id }} </template>
      </el-table-column>
      <el-table-column sortable label="user" align="center">
        <template slot-scope="scope"
          ><el-tag type="danger">{{ scope.row.user }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column sortable label="exam_id" align="center">
        <template slot-scope="scope">{{ scope.row.exam_id }} </template>
      </el-table-column>
      <el-table-column sortable label="exam_url" align="center">
        <template slot-scope="scope">{{ scope.row.exam_url }} </template>
      </el-table-column>
      <el-table-column sortable label="status" align="center">
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
  </div>
</template>

<script>
import { list, create } from "@/api/toolkit/exam";
export default {
  data() {
    return {
      examList: [],
      is_stripe: true,
    };
  },
  created() {
    this.fetchexam();
  },
  methods: {
    fetchexam() {
      list().then((response) => {
        this.examList = response.data.items;
      });
    },
    handleClick() {
      create().then((response) => {
        this.fetchexam();
      });
    },
  },
};
</script>
