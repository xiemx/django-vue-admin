<template>
  <div class="app-container">
    <el-button type="success" @click="handleClick">创建调度器</el-button>
    <el-dialog title="用户组信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="minute" :label-width="formLabelWidth">
          <el-input v-model="form.minute" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="hour" :label-width="formLabelWidth">
          <el-input v-model="form.hour" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="day_of_week" :label-width="formLabelWidth">
          <el-input v-model="form.day_of_week" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="day_of_month" :label-width="formLabelWidth">
          <el-input v-model="form.day_of_month" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="month_of_year" :label-width="formLabelWidth">
          <el-input v-model="form.month_of_year" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="timezone" :label-width="formLabelWidth">
          <el-select v-model="form.timezone" clearable placeholder="请选择时区">
            <el-option
              v-for="item in timezone"
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
        <el-button type="primary" @click="handleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table
      :data="crontabList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" prop="id" align="center">
        <template slot-scope="scope">{{ scope.row.id }} </template>
      </el-table-column>
      <el-table-column sortable label="minute" prop="minute" align="center">
        <template slot-scope="scope">{{ scope.row.minute }} </template>
      </el-table-column>
      <el-table-column sortable label="hour" prop="hour" align="center">
        <template slot-scope="scope">{{ scope.row.hour }} </template>
      </el-table-column>
      <el-table-column
        sortable
        label="day_of_week"
        prop="day_of_week"
        align="center"
      >
        <template slot-scope="scope">{{ scope.row.day_of_week }} </template>
      </el-table-column>
      <el-table-column
        sortable
        label="day_of_month"
        prop="day_of_month"
        align="center"
      >
        <template slot-scope="scope">{{ scope.row.day_of_month }} </template>
      </el-table-column>
      <el-table-column
        sortable
        label="month_of_year"
        prop="month_of_year"
        align="center"
      >
        <template slot-scope="scope">{{ scope.row.month_of_year }} </template>
      </el-table-column>
      <el-table-column sortable label="timezone" prop="timezone" align="center">
        <template slot-scope="scope">{{ scope.row.timezone }} </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleUpdate(scope.row)"
            >编 辑</el-button
          >
          <el-dialog title="更新调度器" :visible.sync="updateDialogFormVisible">
            <el-form :model="form">
              <el-form-item label="id" :label-width="formLabelWidth">
                <el-input
                  v-model="form.id"
                  disabled
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="minute" :label-width="formLabelWidth">
                <el-input v-model="form.minute" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="hour" :label-width="formLabelWidth">
                <el-input v-model="form.hour" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="day_of_week" :label-width="formLabelWidth">
                <el-input
                  v-model="form.day_of_week"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="day_of_month" :label-width="formLabelWidth">
                <el-input
                  v-model="form.day_of_month"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="month_of_year" :label-width="formLabelWidth">
                <el-input
                  v-model="form.month_of_year"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="timezone" :label-width="formLabelWidth">
                <el-select
                  v-model="form.timezone"
                  clearable
                  placeholder="请选择时区"
                >
                  <el-option
                    v-for="item in timezone"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
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
import { list, create, deleted, update } from "@/api/job/schedule/crontab";
export default {
  data() {
    return {
      timezone: [
        {
          value: "UTC",
          label: "UTC",
        },
        {
          value: "Asia/Shanghai",
          label: "Asia/Shanghai",
        },
      ],
      crontabList: [],
      is_stripe: true,
      dialogFormVisible: false,
      updateDialogFormVisible: false,
      formLabelWidth: "10%",
      form: {
        minute: "",
        hour: "",
        day_of_week: "",
        day_of_month: "",
        month_of_year: "",
        timezone: "",
      },
    };
  },
  created() {
    this.fetchcrontab();
  },
  methods: {
    fetchcrontab() {
      list().then((response) => {
        this.crontabList = response.data.items;
      });
    },
    handleClick() {
      this.form = {};
      this.dialogFormVisible = true;
    },
    handleCreate() {
      create(this.form).then((response) => {
        this.fetchcrontab();
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
        this.fetchcrontab();
      });
    },
  },
};
</script>
