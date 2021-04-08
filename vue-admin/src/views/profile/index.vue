<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">
        <el-col :span="6" :xs="24">
          <user-card :user="user" />
        </el-col>

        <el-col :span="18" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="Timeline" name="timeline">
                <timeline :activities="auditOperationList" :reverse="reverse" />
              </el-tab-pane>
              <el-tab-pane label="Account" name="account">
                <account :user="user" />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import UserCard from "./components/UserCard";
import Timeline from "@/components/Timeline";
import Account from "./components/Account";
import * as audit from "@/api/audit";
import { getInfo } from "@/api/user";
import { getToken } from "@/utils/auth";

export default {
  name: "Profile",
  components: { UserCard, Timeline, Account },
  data() {
    return {
      user: {},
      activeTab: "timeline",
      auditOperationList: [],
      reverse: false,
    };
  },
  computed: {
    ...mapGetters(["name", "avatar", "roles"]),
  },

  created() {
    this.getUser();
    this.fetchAudit();
  },

  methods: {
    fetchAudit() {
      audit
        .list({
          limit: 10,
          username: this.name,
        })
        .then((response) => {
          this.auditOperationList = response.data.items;
        });
    },
    getUser() {
      const token = getToken();
      getInfo(token).then((response) => {
        this.user = response.data;
      });
    },
  },
};
</script>
