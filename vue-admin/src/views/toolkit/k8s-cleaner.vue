<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">清理POD</el-button>

    <el-dialog title="任务信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="cluster" :label-width="formLabelWidth">
          <el-select v-model="form.cluster" placeholder="请选择 Cluster ">
            <el-option
              v-for="item in clusterList"
              :key="item.id"
              :label="item.name"
              :value="item.name"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postHandleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table
      :data="examList"
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
      <el-table-column sortable prop="cluster" label="cluster" align="center">
        <template slot-scope="scope">
          {{ scope.row.cluster }}
        </template>
      </el-table-column>
      <el-table-column label="pods" align="center">
        <template slot-scope="scope">
          {{ scope.row.pods }}
        </template>
      </el-table-column>

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
        @pagination="fetchexam"
      />
    </div>
  </div>
</template>

<script>
import { list, create } from "@/api/toolkit/k8s-cleaner";
import { clusters } from "@/api/k8s/cluster";
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
      examList: [],
      clusterList: [],
      dialogFormVisible: false,
      formLabelWidth: "50%",
      form: {
        cluster: null,
      },
      is_stripe: true,
    };
  },
  created() {
    this.fetchexam();
  },
  methods: {
    fetchCluster() {
      clusters().then((response) => {
        this.clusterList = response.data.items;
      });
    },
    fetchexam() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      list({
        limit: this.listQuery.limit,
        offset,
      }).then((response) => {
        this.total = response.data.total;
        this.examList = response.data.items;
      });
    },
    handleCreate() {
      this.dialogFormVisible = !this.dialogFormVisible;
      this.fetchCluster();
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.dialogFormVisible = !this.dialogFormVisible;
        this.fetchexam();
      });
    },
  },
};
</script>
