<template>
  <div class="block">
    <el-timeline :reverse="reverse">
      <el-timeline-item
        v-for="(activity, index) in activities"
        :key="index"
        :timestamp="activity.create_time"
      >
        <el-card>
          <h3>{{ activity.operation }}</h3>
          <p class="el-card-p1">
            {{ activity.user }} {{ activity.operation }}
            {{ activity.resource }}
          </p>
          <p v-if="activity.operation === 'partial_update'">
            before : {{ activity.before }}
          </p>
          <p v-if="activity.content != null">content: {{ activity.content }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
export default {
  name: "Timeline",
  props: {
    reverse: {
      required: true,
      type: Boolean,
      default: true,
    },
    activities: {
      required: true,
      type: Array,
      default: () => {
        return [];
      },
    },
  },
  methods: {},
};
</script>

<style>
.el-card-p1 {
  color: brown;
}
</style>