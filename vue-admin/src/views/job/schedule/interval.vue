<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">创建调度器</el-button>

    <el-dialog title="调度器信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="every" :label-width="formLabelWidth">
          <el-input-number v-model="form.every" :min="1"></el-input-number>
        </el-form-item>
        <el-form-item label="period" :label-width="formLabelWidth">
          <el-select v-model="form.period" clearable placeholder="请选择">
            <el-option
              v-for="item in period"
              :key="item.value"
              :label="item.label"
              :value="item.value"
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
      :data="intervalList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" prop="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>

      <el-table-column sortable label="every" prop="every" align="center">
        <template slot-scope="scope">
          {{ scope.row.every }}
        </template>
      </el-table-column>

      <el-table-column sortable label="period" prop="period" align="center">
        <template slot-scope="scope">
          {{ scope.row.period }}
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleUpdate(scope.row)"
            >编 辑</el-button
          >

          <el-dialog title="调度器信息" :visible.sync="updateDialogFormVisible">
            <el-form :model="form">
              <el-form-item label="id" :label-width="formLabelWidth">
                <el-input
                  v-model="form.id"
                  disabled
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="every" :label-width="formLabelWidth">
                <el-input-number
                  v-model="form.every"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="period" :label-width="formLabelWidth">
                <el-select v-model="form.period" clearable placeholder="请选择">
                  <el-option
                    v-for="item in period"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="postHandleUpdate"
                >确 定</el-button
              >
            </div>
          </el-dialog>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)"
            >删 除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, create, deleted, update } from "@/api/job/schedule/interval";
export default {
  data() {
    return {
      intervalList: [],
      is_stripe: true,
      dialogFormVisible: false,
      formLabelWidth: "10%",
      updateDialogFormVisible: false,
      period: [
        {
          label: "Days",
          value: "days",
        },
        {
          label: "Hours",
          value: "hours",
        },
        {
          label: "Minutes",
          value: "minutes",
        },
        {
          label: "Seconds",
          value: "seconds",
        },
      ],
      form: {
        every: 0,
        period: "",
      },
    };
  },
  created() {
    this.fetchinterval();
  },
  methods: {
    fetchinterval() {
      list().then((response) => {
        this.intervalList = response.data.items;
      });
    },
    handleCreate() {
      this.form = {};
      this.dialogFormVisible = true;
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.fetchinterval();
      });
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleUpdate(row) {
      this.form = row;
      this.updateDialogFormVisible = true;
    },
    postHandleUpdate() {
      update(this.form).then((response) => {});
      this.updateDialogFormVisible = false;
    },
    handleDelete(row) {
      deleted(row).then((response) => {
        this.fetchinterval();
      });
    },
  },
};
</script>
