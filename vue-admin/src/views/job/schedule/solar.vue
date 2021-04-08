<template>
  <div class="app-container">
    <el-button type="success" @click="handleClick">创建调度器</el-button>
    <el-table
      :data="solarList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>

      <el-table-column sortable label="solared_time" align="center">
        <template slot-scope="scope">
          {{ scope.row }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success">编 辑</el-button>
          <el-button size="mini" type="danger">删 除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, create, deleted, update } from "@/api/job/schedule/solar";
export default {
  data() {
    return {
      solarList: [],
      is_stripe: true,
    };
  },
  created() {
    this.fetchsolar();
  },
  methods: {
    fetchsolar() {
      list().then((response) => {
        this.solarList = response.data.items;
      });
    },
    handleClick() {
      create().then((response) => {
        this.fetchsolar();
      });
    },
  },
};
</script>
