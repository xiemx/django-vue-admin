<template>
  <div class="app-container">
    <el-button type="success" @click="handleCreate">创建任务</el-button>

    <el-dialog title="任务信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-divider><i class="el-icon-mobile-phone">任务信息</i></el-divider>
        <br />
        <br />
        <el-form-item label="Name" :label-width="formLabelWidth">
          <el-input v-model="form.name" placeholder="请输入内容"></el-input>
        </el-form-item>
        <el-form-item label="description" :label-width="formLabelWidth">
          <el-input
            v-model="form.description"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 4 }"
            placeholder="请输入内容"
          ></el-input>
        </el-form-item>

        <el-form-item label="Task" :label-width="formLabelWidth">
          <el-input
            v-model="form.task"
            placeholder="The Name of the Celery Task that Should be Run. Example: proj.tasks.import_contacts"
          ></el-input>
        </el-form-item>
        <el-form-item label="Enabled" :label-width="formLabelWidth">
          <el-switch
            v-model="form.enabled"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </el-form-item>
        <el-divider><i class="el-icon-mobile-phone">调度器信息</i></el-divider>
        <br />
        <br />
        <el-form-item label="start_time" :label-width="formLabelWidth">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择日期时间"
          >
          </el-date-picker>
        </el-form-item>

        <el-form-item label="interval" :label-width="formLabelWidth">
          <el-select
            v-if="choicedSchedule"
            disabled
            v-model="form.interval"
            placeholder="请选择"
            @change="handleScheduleInput('interval')"
          >
            <el-option
              v-for="item in intervalList"
              :key="item.id"
              :label="item.id + ' | ' + item.every + ' ' + item.period"
              :value="item.id"
            >
            </el-option>
          </el-select>
          <el-select
            v-else
            clearable
            v-model="form.interval"
            placeholder="请选择"
            @change="handleScheduleInput('interval')"
          >
            <el-option
              v-for="item in intervalList"
              :key="item.id"
              :label="item.id + ' | ' + item.every + ' ' + item.period"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="crontab" :label-width="formLabelWidth">
          <el-select
            v-if="choicedSchedule"
            disabled
            v-model="form.crontab"
            placeholder="请选择"
            @change="handleScheduleInput('crontab')"
          >
            <el-option
              v-for="item in crontabList"
              :key="item.id"
              :label="
                item.id +
                ' | ' +
                item.minute +
                item.hour +
                item.day_of_week +
                item.day_of_month +
                item.month_of_year +
                ' | ' +
                item.timezone
              "
              :value="item.id"
            >
            </el-option>
          </el-select>
          <el-select
            v-else
            clearable
            v-model="form.crontab"
            placeholder="请选择"
            @change="handleScheduleInput('crontab')"
          >
            <el-option
              v-for="item in crontabList"
              :key="item.id"
              :label="
                item.id +
                ' | ' +
                item.minute +
                item.hour +
                item.day_of_week +
                item.day_of_month +
                item.month_of_year +
                ' | ' +
                item.timezone
              "
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="clocked" :label-width="formLabelWidth">
          <el-select
            v-if="choicedSchedule"
            v-model="form.clocked"
            clearable
            disabled
            placeholder="请选择"
            @change="handleScheduleInput('clocked')"
          >
            <el-option
              v-for="item in clockList"
              :key="item.id"
              :label="item.id + ' | ' + item.clocked_time"
              :value="item.id"
            >
            </el-option>
          </el-select>
          <el-select
            v-else
            v-model="form.clocked"
            clearable
            placeholder="请选择"
            @change="handleScheduleInput('clocked')"
          >
            <el-option
              v-for="item in clockList"
              :key="item.id"
              :label="item.id + ' | ' + item.clocked_time"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="one_off" :label-width="formLabelWidth">
          <el-switch
            v-if="form.clocked"
            disabled
            v-model="form.one_off"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
          <el-switch
            v-else
            v-model="form.one_off"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </el-form-item>

        <el-button
          @click="handleScheduleInput"
          size="mini"
          type="success"
          style="align: center"
        >
          重置调度器
        </el-button>

        <el-divider><i class="el-icon-mobile-phone">Arguments</i></el-divider>
        <br />
        <br />
        <el-form-item label="args" :label-width="formLabelWidth">
          <el-input
            v-model="form.args"
            type="textarea"
            :autosize="{ minRows: 5, maxRows: 5 }"
            placeholder='JSON encoded positional arguments (Example: ["arg1", "arg2"])'
          ></el-input>
        </el-form-item>
        <el-form-item label="kwargs" :label-width="formLabelWidth">
          <el-input
            v-model="form.kwargs"
            type="textarea"
            :autosize="{ minRows: 5, maxRows: 5 }"
            placeholder='JSON encoded keyword arguments (Example: {"argument": "value"})'
          ></el-input>
        </el-form-item>

        <!-- 
        <el-divider
          ><i class="el-icon-mobile-phone">Execution Options</i></el-divider
        >
        <br />
        <br />

        <el-form-item label="expires" :label-width="formLabelWidth">
          <el-date-picker
            v-model="form.expires"
            type="datetime"
            placeholder="选择日期时间"
          >
          </el-date-picker>
          <i class="tips">
            Datetime after which the schedule will no longer trigger the task to
            run
          </i>
        </el-form-item>

        <el-form-item label="expire_seconds" :label-width="formLabelWidth">
          <el-input-number
            size="mini"
            v-model="form.expire_seconds"
            controls-position="right"
          >
          </el-input-number>

          <i class="tips">
            Timedelta with seconds which the schedule will no longer trigger the
            task to run
          </i>
        </el-form-item>

        <el-form-item label="queue" :label-width="formLabelWidth">
          <el-input
            v-model="form.queue"
            placeholder="Queue defined in CELERY_TASK_QUEUES. Leave None for default queuing."
          ></el-input>
        </el-form-item>
        <el-form-item label="exchange" :label-width="formLabelWidth">
          <el-input
            v-model="form.exchange"
            placeholder="Override Exchange for low-level AMQP routing
"
          ></el-input>
        </el-form-item>
        <el-form-item label="routing_key" :label-width="formLabelWidth">
          <el-input
            v-model="form.routing_key"
            placeholder="Override Routing Key for low-level AMQP routing"
          ></el-input>
        </el-form-item>

        <el-form-item label="priority" :label-width="formLabelWidth">
          <el-input
            v-model="form.priority"
            placeholder="Datetime after which the schedule will no longer trigger the task to
            run"
          ></el-input>
        </el-form-item>

        <el-form-item label="headers" :label-width="formLabelWidth">
          <el-input
            v-model="form.headers"
            type="textarea"
            :autosize="{ minRows: 5, maxRows: 5 }"
            placeholder="JSON encoded message headers for the AMQP message."
          ></el-input>
        </el-form-item> -->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="postHandleCreate">确 定</el-button>
      </div>
    </el-dialog>

    <el-table
      :data="taskList"
      height="100vh"
      style="width: 100%"
      :stripe="is_stripe"
    >
      <el-table-column sortable label="id" prop="id" align="center">
      </el-table-column>
      <el-table-column sortable label="name" prop="name" align="center">
      </el-table-column>

      <el-table-column sortable label="task" prop="task" align="center">
      </el-table-column>
      <el-table-column label="args" prop="args" align="center">
        <template slot-scope="scope">
          {{ scope.row.args }}
        </template>
      </el-table-column>
      <el-table-column label="kwargs" align="center">
        <template slot-scope="scope">
          {{ scope.row.kwargs }}
        </template>
      </el-table-column>

      <el-table-column
        sortable
        prop="start_time"
        label="start_time"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.start_time }}
        </template>
      </el-table-column>
      <el-table-column label="enabled" align="center">
        <template slot-scope="scope">
          {{ scope.row.enabled }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        label="last_run_at"
        prop="last_run_at"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.last_run_at }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        label="total_run_count"
        prop="total_run_count"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.total_run_count }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        label="date_changed"
        prop="date_changed"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.date_changed }}
        </template>
      </el-table-column>
      <el-table-column label="description" align="center">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>
      <el-table-column label="interval" sortable prop="interval" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.interval" type="success">
            {{ scope.row.interval }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="crontab" sortable prop="crontab" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.crontab" type="success">
            {{ scope.row.crontab }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="clocked" sortable prop="clocked" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.clocked" type="success">
            {{ scope.row.clocked }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleUpdate(scope.row)"
            >编 辑</el-button
          >
          <el-dialog title="任务信息" :visible.sync="updateDialogFormVisible">
            <el-form :model="form">
              <el-divider
                ><i class="el-icon-mobile-phone">任务信息</i></el-divider
              >
              <br />
              <br />
              <el-form-item label="Name" :label-width="formLabelWidth">
                <el-input
                  v-model="form.name"
                  disabled
                  placeholder="请输入内容"
                ></el-input>
              </el-form-item>
              <el-form-item label="description" :label-width="formLabelWidth">
                <el-input
                  v-model="form.description"
                  type="textarea"
                  :autosize="{ minRows: 3, maxRows: 4 }"
                  placeholder="请输入内容"
                ></el-input>
              </el-form-item>

              <el-form-item label="Task" :label-width="formLabelWidth">
                <el-input
                  v-model="form.task"
                  placeholder="The Name of the Celery Task that Should be Run. Example: proj.tasks.import_contacts"
                ></el-input>
              </el-form-item>
              <el-form-item label="Enabled" :label-width="formLabelWidth">
                <el-switch
                  v-model="form.enabled"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
              </el-form-item>
              <el-divider
                ><i class="el-icon-mobile-phone">调度器信息</i></el-divider
              >
              <br />
              <br />
              <el-form-item label="start_time" :label-width="formLabelWidth">
                <el-date-picker
                  v-model="form.start_time"
                  type="datetime"
                  placeholder="选择日期时间"
                >
                </el-date-picker>
              </el-form-item>

              <el-form-item label="interval" :label-width="formLabelWidth">
                <el-select
                  v-if="choicedSchedule"
                  disabled
                  v-model="form.interval"
                  placeholder="请选择"
                  @change="handleScheduleInput('interval')"
                >
                  <el-option
                    v-for="item in intervalList"
                    :key="item.id"
                    :label="item.id + ' | ' + item.every + ' ' + item.period"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
                <el-select
                  v-else
                  clearable
                  v-model="form.interval"
                  placeholder="请选择"
                  @change="handleScheduleInput('interval')"
                >
                  <el-option
                    v-for="item in intervalList"
                    :key="item.id"
                    :label="item.id + ' | ' + item.every + ' ' + item.period"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="crontab" :label-width="formLabelWidth">
                <el-select
                  v-if="choicedSchedule"
                  disabled
                  v-model="form.crontab"
                  placeholder="请选择"
                  @change="handleScheduleInput('crontab')"
                >
                  <el-option
                    v-for="item in crontabList"
                    :key="item.id"
                    :label="
                      item.id +
                      ' | ' +
                      item.minute +
                      item.hour +
                      item.day_of_week +
                      item.day_of_month +
                      item.month_of_year +
                      ' | ' +
                      item.timezone
                    "
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
                <el-select
                  v-else
                  clearable
                  v-model="form.crontab"
                  placeholder="请选择"
                  @change="handleScheduleInput('crontab')"
                >
                  <el-option
                    v-for="item in crontabList"
                    :key="item.id"
                    :label="
                      item.id +
                      ' | ' +
                      item.minute +
                      item.hour +
                      item.day_of_week +
                      item.day_of_month +
                      item.month_of_year +
                      ' | ' +
                      item.timezone
                    "
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="clocked" :label-width="formLabelWidth">
                <el-select
                  v-if="choicedSchedule"
                  v-model="form.clocked"
                  clearable
                  disabled
                  placeholder="请选择"
                  @change="handleScheduleInput('clocked')"
                >
                  <el-option
                    v-for="item in clockList"
                    :key="item.id"
                    :label="item.id + ' | ' + item.clocked_time"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
                <el-select
                  v-else
                  v-model="form.clocked"
                  clearable
                  placeholder="请选择"
                  @change="handleScheduleInput('clocked')"
                >
                  <el-option
                    v-for="item in clockList"
                    :key="item.id"
                    :label="item.id + ' | ' + item.clocked_time"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="one_off" :label-width="formLabelWidth">
                <el-switch
                  v-if="form.clocked"
                  disabled
                  v-model="form.one_off"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
                <el-switch
                  v-else
                  v-model="form.one_off"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
              </el-form-item>

              <el-button
                @click="handleScheduleInput"
                size="mini"
                type="success"
                style="align: center"
              >
                重置调度器
              </el-button>

              <el-divider
                ><i class="el-icon-mobile-phone">Arguments</i></el-divider
              >
              <br />
              <br />
              <el-form-item label="args" :label-width="formLabelWidth">
                <el-input
                  v-model="form.args"
                  type="textarea"
                  :autosize="{ minRows: 5, maxRows: 5 }"
                  placeholder='JSON encoded positional arguments (Example: ["arg1", "arg2"])'
                ></el-input>
              </el-form-item>
              <el-form-item label="kwargs" :label-width="formLabelWidth">
                <el-input
                  v-model="form.kwargs"
                  type="textarea"
                  :autosize="{ minRows: 5, maxRows: 5 }"
                  placeholder='JSON encoded keyword arguments (Example: {"argument": "value"})'
                ></el-input>
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
import { list, create, deleted, update } from "@/api/job/task/task";
import * as crontab_api from "@/api/job/schedule/crontab";
import * as clocked_api from "@/api/job/schedule/clock";
import * as interval_api from "@/api/job/schedule/interval";

export default {
  data() {
    return {
      choicedSchedule: false,
      taskList: [],
      clockList: [],
      crontabList: [],
      intervalList: [],
      is_stripe: true,
      is_one_off: false,
      dialogFormVisible: false,
      updateDialogFormVisible: false,
      formLabelWidth: "10%",
      form: {
        name: "",
        description: "",
        task: "",
        enabled: true,
        start_time: "",
        interval: "",
        clocked: "",
        crontab: "",
        solar: "",
        one_off: false,
        args: "[]",
        kwargs: "{}",
        // expires: "",
        // expire_seconds: null,
        // queue: "",
        // exchange: "",
        // routing_key: "",
        // priority: "",
        // headers: "{}",
      },
    };
  },
  created() {
    this.fetchtask();
  },
  methods: {
    fetchtask() {
      list().then((response) => {
        this.taskList = response.data.items;
      });
    },
    fetchSchedule() {
      clocked_api.list().then((response) => {
        this.clockList = response.data.items;
      });
      interval_api.list().then((response) => {
        this.intervalList = response.data.items;
      });
      crontab_api.list().then((response) => {
        this.crontabList = response.data.items;
      });
    },
    handleCreate() {
      this.dialogFormVisible = true;
      this.fetchSchedule();
    },
    postHandleCreate() {
      create(this.form).then((response) => {
        this.fetchclock();
      });
      this.dialogFormVisible = !this.dialogFormVisible;
      this.fetchtask();
    },
    handleUpdate(row) {
      this.form = row;
      this.updateDialogFormVisible = true;
      this.fetchSchedule();
    },
    postHandleUpdate() {
      update(this.form).then((response) => {});
      this.updateDialogFormVisible = false;
    },
    handleDelete(row) {
      deleted(row).then((response) => {
        this.fetchtask();
      });
    },
    handleScheduleInput(type) {
      this.choicedSchedule = !this.choicedSchedule;
      if (type === "clocked") {
        this.form.one_off = true;
      }
      if (!this.choicedSchedule) {
        this.form.interval = "";
        this.form.clocked = "";
        this.form.crontab = "";
        this.form.one_off = false;
      }
    },
  },
};
</script>
<style>
.tips {
  color: rgb(156, 156, 156);
}
</style>