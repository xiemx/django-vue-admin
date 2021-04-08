<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">扩容服务</el-button>

    <el-dialog title="任务信息" :visible.sync="dialogFormVisible">
      <el-form :model="form" label-position="right">
        <el-form-item label="product" :label-width="formLabelWidth">
          <el-input v-model="form.product" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="namespace" :label-width="formLabelWidth">
          <el-input v-model="form.namespace" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="service_name" :label-width="formLabelWidth">
          <el-input v-model="form.service" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="number" :label-width="formLabelWidth">
          <el-input-number
            v-model="form.number"
            :min="-100"
            :max="100"
            label="描述文字"
          ></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postHandleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table
      :data="scalingList"
      height="85vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable prop="id" label="id" align="center">
      </el-table-column>
      <el-table-column sortable label="task_id" prop="task_id" align="center">
        <template slot-scope="scope">{{ scope.row.task_id }} </template>
      </el-table-column>
      <el-table-column sortable prop="user" label="user" align="center">
        <template slot-scope="scope"
          ><el-tag type="danger">{{ scope.row.user }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column sortable prop="product" label="product" align="center">
        <template slot-scope="scope">
          {{ scope.row.product }}
        </template>
      </el-table-column>
      <el-table-column label="service_name" prop="service" align="center">
        <template slot-scope="scope">
          {{ scope.row.service }}
        </template>
      </el-table-column>
      <el-table-column label="number" prop="number" align="center">
        <template slot-scope="scope">
          {{ scope.row.number }}
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
        @pagination="fetchScaling"
      />
    </div>
  </div>
</template>

<script>
import { list, create } from "@/api/toolkit/autoscaling";
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
      scalingList: [],
      clusterList: [],
      dialogFormVisible: false,
      formLabelWidth: "10%",
      form: {
        product: null,
        number: null,
        service: null,
        namespace: null,
      },
      is_stripe: true,
    };
  },
  created() {
    this.fetchScaling();
  },
  methods: {
    fetchCluster() {
      clusters().then((response) => {
        this.clusterList = response.data.items;
      });
    },
    fetchScaling() {
      var offset = (this.listQuery.page - 1) * this.listQuery.limit;
      list({
        limit: this.listQuery.limit,
        offset,
      }).then((response) => {
        this.total = response.data.total;
        this.scalingList = response.data.items;
      });
    },
    handleCreate() {
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.dialogFormVisible = !this.dialogFormVisible;
        this.fetchScaling();
      });
    },
  },
};
</script>
