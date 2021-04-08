import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'el-icon-monitor' }
    }]
  },

  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: 'Profile', icon: 'user', noCache: true }
      }
    ]
  },

  {
    path: '/deploy',
    component: Layout,
    meta: { title: '服务发布', icon: 'el-icon-bank-card' },
    children: [
      {
        path: 'current',
        name: 'current',
        component: () => import('@/views/deploy/current'),
        meta: { title: '当前版本', icon: 'el-icon-mobile' }
      },
      {
        path: 'release',
        name: 'release',
        component: () => import('@/views/deploy/release'),
        meta: { title: '部署记录', icon: 'el-icon-mobile' }
      },
      {
        path: 'service',
        name: 'service',
        component: () => import('@/views/deploy/service'),
        meta: { title: '服务清单', icon: 'el-icon-scissors' }
      }
    ]
  },

  {
    path: '/job',
    component: Layout,
    meta: { title: '计划任务', icon: 'el-icon-umbrella' },
    children: [
      {
        path: 'schedule',
        name: 'schedule',
        component: () => import('@/views/nested/index'),
        meta: { title: '调度器', icon: 'el-icon-cpu' },
        children: [
          {
            path: 'crontab',
            name: 'crontab',
            component: () => import('@/views/job/schedule/crontab'),
            meta: { title: 'Crontab', icon: 'el-icon-link' }
          },
          {
            path: 'clock',
            name: 'clock',
            component: () => import('@/views/job/schedule/clock'),
            meta: { title: 'clock', icon: 'el-icon-orange' }
          },
          {
            path: 'interval',
            name: 'interval',
            component: () => import('@/views/job/schedule/interval'),
            meta: { title: 'interval', icon: 'el-icon-stopwatch' }
          },
          {
            path: 'solar',
            name: 'solar',
            hidden: true,
            component: () => import('@/views/job/schedule/solar'),
            meta: { title: 'solar', icon: 'el-icon-watermelon' }
          },

        ]
      },

      {
        path: 'tasks',
        name: 'tasks',
        component: () => import('@/views/nested/index'),
        meta: { title: '任务', icon: 'el-icon-brush' },
        children: [
          {
            path: 'list',
            name: 'list',
            component: () => import('@/views/job/tasks/list'),
            meta: { title: '任务清单', icon: 'el-icon-orange' }
          }
        ]
      },

    ]
  },

  {
    path: '/kubernetes',
    component: Layout,
    name: 'kubernetes',
    meta: { title: 'K8S集群', icon: 'el-icon-mouse' },
    children: [
      {
        path: 'cluster',
        name: 'cluster',
        component: () => import('@/views/kuberneters/cluster'),
        meta: { title: 'cluster', icon: 'el-icon-coordinate', roles: ["admin", "devops"] }
      },
      {
        path: 'node',
        name: 'node',
        component: () => import('@/views/kuberneters/node'),
        meta: { title: 'Node', icon: 'el-icon-magic-stick' }
      },
      {
        path: 'namespace',
        name: 'namespace',
        component: () => import('@/views/kuberneters/namespace'),
        meta: { title: 'namespace', icon: 'el-icon-reading' }
      },
      {
        path: 'deployment',
        name: 'deployment',
        component: () => import('@/views/kuberneters/deployment'),
        meta: { title: 'deployment', icon: 'el-icon-data-line' }
      },
      {
        path: 'statefulset',
        name: 'statefulset',
        component: () => import('@/views/kuberneters/statefulset'),
        meta: { title: 'statefulSet', icon: 'el-icon-film' }
      },
      {
        path: 'daemonset',
        name: 'daemonset',
        component: () => import('@/views/kuberneters/daemonset'),
        meta: { title: 'daemonset', icon: 'el-icon-cpu' }
      },
      {
        path: 'pod',
        name: 'pod',
        component: () => import('@/views/kuberneters/pod'),
        meta: { title: 'pod', icon: 'el-icon-present' }
      },
      {
        path: 'job',
        name: 'job',
        component: () => import('@/views/kuberneters/job'),
        meta: { title: 'job', icon: 'el-icon-bangzhu' }
      },
      {
        path: 'cronjob',
        name: 'cronjob',
        component: () => import('@/views/kuberneters/cronjob'),
        meta: { title: 'cronJob', icon: 'el-icon-ship' }
      },
      {
        path: 'ingress',
        name: 'ingress',
        component: () => import('@/views/kuberneters/ingress'),
        meta: { title: 'ingress', icon: 'el-icon-basketball' }
      },
      {
        path: 'services',
        name: 'services',
        component: () => import('@/views/kuberneters/service'),
        meta: { title: 'services', icon: 'el-icon-wind-power' }
      },
      {
        path: 'configmap',
        name: 'configmap',
        component: () => import('@/views/kuberneters/configmap'),
        meta: { title: 'configMap', icon: 'el-icon-light-rain' }
      },
      {
        path: 'secret',
        name: 'secret',
        component: () => import('@/views/kuberneters/secret'),
        meta: { title: 'secret', icon: 'el-icon-lightning', roles: ['admin'] }
      },
      {
        path: 'role',
        name: 'role',
        component: () => import('@/views/kuberneters/role'),
        meta: { title: 'role', icon: 'el-icon-heavy-rain' }
      },
      {
        path: 'clusterrole',
        name: 'clusterrole',
        component: () => import('@/views/kuberneters/cluster-role'),
        meta: { title: 'clusterRole', icon: 'el-icon-knife-fork' }
      },
      {
        path: 'rolebinding',
        name: 'rolebinding',
        component: () => import('@/views/kuberneters/role-binding'),
        meta: { title: 'roleBinding', icon: 'el-icon-view' }
      },
      {
        path: 'clusterrolebinding',
        name: 'clusterrolebinding',
        component: () => import('@/views/kuberneters/cluster-role-binding'),
        meta: { title: 'clusterRoleBinding', icon: 'el-icon-video-play' }
      },
      {
        path: 'serviceaccount',
        name: 'serviceaccount',
        component: () => import('@/views/kuberneters/service-account'),
        meta: { title: 'serviceAccount', icon: 'el-icon-date' }
      }

    ]
  },
  {
    path: '/tools',
    component: Layout,
    meta: { title: '工具箱', icon: 'el-icon-school' },
    children: [
      {
        path: 'exam',
        name: 'exam',
        component: () => import('@/views/toolkit/exam'),
        meta: { title: '创建压测考试', icon: 'el-icon-toilet-paper' }
      },

      {
        path: 'ingress-whitelist',
        name: 'ingress-whitelist',
        component: () => import('@/views/toolkit/ingress-whitelist'),
        meta: { title: '更新白名单', icon: 'el-icon-printer' }
      },

      {
        path: 'k8s-cleaner',
        name: 'k8s-cleaner',
        component: () => import('@/views/toolkit/k8s-cleaner'),
        meta: { title: '清理驱逐 Pod', icon: 'el-icon-sell' }
      },
      {
        path: 'graphite-cleaner',
        name: 'graphite-cleaner',
        component: () => import('@/views/toolkit/graphite-cleaner'),
        meta: { title: 'Graphite 清理', icon: 'el-icon-sell' }
      },

      {
        path: 'autoscaling',
        name: 'autoscaling',
        component: () => import('@/views/toolkit/autoscaling'),
        meta: { title: '服务扩缩容', icon: 'el-icon-magic-stick' }
      },

    ]
  },

  {
    path: '/result',
    name: 'result',
    component: Layout,
    children: [{
      path: 'list',
      name: 'result_list',
      component: () => import('@/views/job/tasks/result'),
      meta: { title: '任务结果', icon: 'el-icon-monitor' }
    }]
  },

  {
    path: '/audit',
    name: 'audit',
    component: Layout,
    children: [{
      path: 'list',
      name: 'audit_list',
      component: () => import('@/views/audit/'),
      meta: { title: 'Audit 日志', roles: ['admin'], icon: 'el-icon-monitor' }
    }]
  },


  {
    path: '/account',
    component: Layout,
    name: 'account',
    meta: { title: '用户管理', icon: 'el-icon-s-help', roles: ['admin'] },
    children: [
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/account/user'),
        meta: { title: '用户管理', icon: 'el-icon-user', roles: ['admin'] }
      },
      {
        path: 'group',
        name: 'Group',
        component: () => import('@/views/account/group'),
        meta: { title: '组管理', icon: 'el-icon-refrigerator', roles: ['admin'] }
      },
      {
        path: 'permissions',
        name: 'permissions',
        component: () => import('@/views/account/permission'),
        meta: { title: '权限管理', icon: 'el-icon-odometer', roles: ['admin'] }
      },
      {
        path: 'k8s-rbac',
        name: 'k8s-rbac',
        component: () => import('@/views/account/rbac-k8s'),
        meta: { title: 'K8S授权', icon: 'el-icon-heavy-rain', roles: ['admin'] }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
