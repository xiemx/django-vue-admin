<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">注册服务</el-button>
    <el-dialog title="服务信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="description" :label-width="formLabelWidth">
          <el-input
            v-model="form.description"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 4 }"
            placeholder="请输入内容"
          ></el-input>
        </el-form-item>
        <el-form-item label="repo" :label-width="formLabelWidth">
          <el-input v-model="form.repo" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="chart_dir" :label-width="formLabelWidth">
          <el-input v-model="form.chart_dir" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="value_file" :label-width="formLabelWidth">
          <el-input v-model="form.value_file" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="enabled" :label-width="formLabelWidth">
          <el-switch
            v-model="form.enabled"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postHandleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table :data="serviceList" style="width: 100%">
      <el-table-column prop="id" sortable label="id" align="center">
      </el-table-column>
      <el-table-column prop="name" sortable label="name" align="center">
      </el-table-column>
      <el-table-column prop="repo" sortable label="repo" align="center">
      </el-table-column>
      <el-table-column prop="chart_dir" label="chart_dir" align="center">
      </el-table-column>
      <el-table-column
        prop="description"
        sortable
        label="description"
        align="center"
      >
      </el-table-column>
      <el-table-column prop="enabled" label="enabled" align="center">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enabled"
            active-color="#13ce66"
            inactive-color="#ff4949"
            disabled
          >
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        prop="create_time"
        sortable
        label="create_time"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="update_time"
        sortable
        label="update_time"
        align="center"
      >
      </el-table-column>

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleUpdate(scope.row)"
            >更新</el-button
          >
          <el-dialog title="服务信息" :visible.sync="updateDialogFormVisible">
            <el-form :model="form">
              <el-form-item label="name" :label-width="formLabelWidth">
                <el-input v-model="form.name" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="description" :label-width="formLabelWidth">
                <el-input
                  v-model="form.description"
                  type="textarea"
                  :autosize="{ minRows: 3, maxRows: 4 }"
                  placeholder="请输入内容"
                ></el-input>
              </el-form-item>
              <el-form-item label="repo" :label-width="formLabelWidth">
                <el-input v-model="form.repo" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="chart_dir" :label-width="formLabelWidth">
                <el-input
                  v-model="form.chart_dir"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="value_file" :label-width="formLabelWidth">
                <el-input
                  v-model="form.value_file"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="enabled" :label-width="formLabelWidth">
                <el-switch
                  v-model="form.enabled"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="postHandleUpdate(scope.row)"
                >确 定</el-button
              >
            </div>
          </el-dialog>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, create, deleted, update } from "@/api/deploy/service";
export default {
  data() {
    return {
      serviceList: [],
      form: {
        name: "",
        repo: "",
        chart_dir: "",
        value_file: "",
        enabled: true,
        description: "",
      },
      dialogFormVisible: false,
      updateDialogFormVisible: false,
      formLabelWidth: "10%",
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    fetchServices() {
      list().then((response) => {
        this.serviceList = response.data.items;
      });
    },
    handleCreate() {
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.fetchServices();
      });
      this.dialogFormVisible = !this.dialogFormVisible;
    },
    handleUpdate(row) {
      this.form = row;
      this.updateDialogFormVisible = true;
    },
    postHandleUpdate() {
      update(this.form).then((response) => {
        this.fetchServices();
      });
      this.updateDialogFormVisible = false;
    },
    handleDelete(row) {
      deleted(row).then((response) => {
        this.fetchServices();
      });
    },
  },
};
</script>
