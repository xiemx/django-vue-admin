<template>
  <el-table :data="list" style="width: 100%; padding-top: 15px">
    <el-table-column label="id" width="100">
      <template slot-scope="scope">
        {{ scope.row.id }}
      </template>
    </el-table-column>
    <el-table-column label="task_id">
      <template slot-scope="scope">
        {{ scope.row.task_id }}
      </template>
    </el-table-column>
    <el-table-column label="task_name" align="center">
      <template slot-scope="scope">
        {{ scope.row.task_name }}
      </template>
    </el-table-column>
    <el-table-column label="status" align="center">
      <template slot-scope="{ row }">
        <el-tag :type="row.status | statusFilter">
          {{ row.status }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  props: {
    list: {
      required: true,
      type: Array,
      default: () => {
        return [];
      },
    },
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        SUCCESS: "success",
        FAILURE: "danger",
      };
      return statusMap[status];
    },
  },
  data() {
    return {};
  },
};
</script>
