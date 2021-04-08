<template>
  <el-card style="margin-bottom: 20px">
    <div slot="header" class="clearfix">
      <span>About me</span>
    </div>

    <div class="user-profile">
      <div class="box-center">
        <pan-thumb
          :image="(user.profile && user.profile.avatar) || default_avatar"
          :height="'100px'"
          :width="'100px'"
          :hoverable="false"
        >
          <div>Hello, {{ user.username }}</div>
        </pan-thumb>
      </div>
      <div class="box-center">
        <div class="user-name text-center">{{ user.username }}</div>
        <div class="user-role text-center text-muted">
          {{ user.groups }}
        </div>
      </div>
    </div>

    <div class="user-bio">
      <div class="user-education user-bio-section">
        <!-- <div class="user-bio-section-header">
          <svg-icon icon-class="education" /><span>Education</span>
        </div>
        <div class="user-bio-section-body">
          <div class="text-muted">
            JS in Computer Science from the University of Technology
          </div>
        </div> -->
      </div>

      <div class="user-skills user-bio-section">
        <div class="user-bio-section-header">
          <svg-icon icon-class="skill" /><span>Info</span>
        </div>
        <div class="user-bio-section-body">
          <div class="progress-item">
            <span>手机号:</span>
            <el-input
              disabled
              v-if="user.profile"
              v-model="user.profile.phone"
            />
          </div>
          <div class="progress-item">
            <span>邮箱:</span>
            <el-input disabled v-model="user.email" />
          </div>
          <div class="progress-item">
            <span>阿里云 UID:</span>
            <el-input
              disabled
              v-if="user.profile"
              v-model="user.profile.alicloud"
            />
          </div>
          <div class="progress-item">
            <span>钉钉 ID:</span>
            <el-input
              disabled
              v-if="user.profile"
              v-model="user.profile.dingding"
            />
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import PanThumb from "@/components/PanThumb";

export default {
  components: { PanThumb },
  data() {
    return {
      default_avatar:
        "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
    };
  },
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          profile: { avatar: "" },
        };
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
    font-size: 14px;
  }

  .box-social {
    padding-top: 30px;

    .el-table {
      border-top: 1px solid #dfe6ec;
    }
  }

  .user-follow {
    padding-top: 20px;
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
</style>
