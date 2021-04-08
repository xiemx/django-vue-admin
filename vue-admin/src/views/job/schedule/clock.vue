<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">创建调度器</el-button>

    <el-dialog title="调度器信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="clocked_time" :label-width="formLabelWidth">
          <el-date-picker
            v-model="form.clocked_time"
            type="datetime"
            placeholder="选择日期时间"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postHandleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table
      :data="clockList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>

      <el-table-column sortable label="clocked_time" align="center">
        <template slot-scope="scope">
          <el-date-picker
            disabled
            v-model="scope.row.clocked_time"
            type="datetime"
            placeholder="暂无数据"
          >
          </el-date-picker>
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
              <el-form-item label="clocked_time" :label-width="formLabelWidth">
                <el-date-picker
                  v-model="form.clocked_time"
                  type="datetime"
                  placeholder="选择日期时间"
                >
                </el-date-picker>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="updateDialogFormVisible = false"
                >取 消</el-button
              >
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
import { list, create, deleted, update } from "@/api/job/schedule/clock";
export default {
  data() {
    return {
      clockList: [],
      is_stripe: true,
      dialogFormVisible: false,
      formLabelWidth: "10%",
      form: {
        clocked_time: "",
      },
      updateDialogFormVisible: false,
    };
  },
  created() {
    this.fetchclock();
  },
  methods: {
    fetchclock() {
      list().then((response) => {
        this.clockList = response.data.items;
      });
    },
    handleCreate() {
      this.dialogFormVisible = true;
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.fetchclock();
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
        this.fetchclock();
      });
    },
  },
};
</script>
