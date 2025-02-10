<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">

            <el-form-item label="创建来源" prop="createSource">
              <el-select
                  v-model="queryParams.createSource"
                  placeholder="请选择创建来源"
                  style="width: 180px"
                  clearable>
                <el-option
                  v-for="dict in mj_job_create_source"
                  :key="dict.value"
                  :label="dict.label"
                  :value="dict.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="当前状态" prop="currentStatus">
              <el-select
                  v-model="queryParams.currentStatus"
                  placeholder="请选择当前状态"
                  style="width: 180px"
                  clearable>
                <el-option
                  v-for="dict in mj_job_status"
                  :key="dict.value"
                  :label="dict.label"
                  :value="dict.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="Discord URL" prop="discordUrl">
              <el-input
                v-model="queryParams.discordUrl"
                placeholder="请输入Discord URL"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>

            <el-form-item label="提交时间" style="width: 308px">
              <el-date-picker
                v-model="daterangeEnqueueTime"
                value-format="YYYY-MM-DD"
                type="daterange"
                range-separator="-"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </el-form-item>



            <el-form-item label="job_id" prop="jobId">
              <el-input
                v-model="queryParams.jobId"
                placeholder="请输入job_id"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>


            <el-form-item label="mj_id" prop="mjId">
              <el-input
                v-model="queryParams.mjId"
                placeholder="请输入mj_id"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>

            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="queryParams.username"
                placeholder="请输入用户名"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>

            <el-form-item label="mj_user_id" prop="userId">
              <el-input
                v-model="queryParams.userId"
                placeholder="请输入mj_user_id"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['mj:monitor:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['mj:monitor:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['mj:monitor:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['mj:monitor:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="monitorList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />


          <el-table-column label="创建来源" align="center" prop="createSource">
            <template #default="scope">
                <dict-tag :options="mj_job_create_source" :value="scope.row.createSource"/>
            </template>
          </el-table-column>


          <el-table-column label="当前状态" align="center" prop="currentStatus">
            <template #default="scope">
                <dict-tag :options="mj_job_status" :value="scope.row.currentStatus"/>
            </template>
          </el-table-column>


          <el-table-column label="Discord URL" align="center" prop="discordUrl" />

          <el-table-column label="提交时间" align="center" prop="enqueueTime" />

          <el-table-column label="事件类型" align="center" prop="eventType">
            <template #default="scope">
                <dict-tag :options="mj_job_event_type" :value="scope.row.eventType ? scope.row.eventType.split(',') : []"/>
            </template>
          </el-table-column>

          <el-table-column label="咒语" align="center" prop="fullCommand" />


          <el-table-column label="自增主键" align="center" prop="id" />

          <el-table-column label="job_id" align="center" prop="jobId" />

          <el-table-column label="job类型" align="center" prop="jobType">
            <template #default="scope">
                <dict-tag :options="mj_job_type" :value="scope.row.jobType ? scope.row.jobType.split(',') : []"/>
            </template>
          </el-table-column>



          <el-table-column label="mj_id" align="center" prop="mjId" />


          <el-table-column label="父事件job_id" align="center" prop="parentId" />




          <el-table-column label="更新时间" align="center" prop="updateTime" />

          <el-table-column label="用户名" align="center" prop="username" />


          <el-table-column label="mj_user_id" align="center" prop="userId" />

      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['mj:monitor:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['mj:monitor:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改mj监控任务列表对话框 -->
    <el-dialog :title="title" v-model="open" width="800px" append-to-body>
      <el-form ref="monitorRef" :model="form" :rules="rules" label-width="80px">

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Monitor">
import { listMonitor, getMonitor, delMonitor, addMonitor, updateMonitor } from "@/api/mj/monitor";

const { proxy } = getCurrentInstance();
const { mj_job_create_source, mj_job_status, mj_job_event_type, mj_job_type } = proxy.useDict('mj_job_create_source', 'mj_job_status', 'mj_job_event_type', 'mj_job_type');

const monitorList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
    const daterangeCreateTime = ref([]);
    const daterangeEnqueueTime = ref([]);
    const daterangeUpdateTime = ref([]);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    createSource: null,
    currentStatus: null,
    discordUrl: null,
    enqueueTime: null,
    eventType: null,
    fullCommand: null,
    jobId: null,
    jobType: null,
    mjId: null,
    username: null,
    userId: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询mj监控任务列表列表 */
function getList() {
  loading.value = true;
      queryParams.value.params = {};
      queryParams.value.params = {};
      queryParams.value.params = {};
      if (null != daterangeCreateTime && '' != daterangeCreateTime) {
        queryParams.value.params["beginCreateTime"] = daterangeCreateTime.value[0];
        queryParams.value.params["endCreateTime"] = daterangeCreateTime.value[1];
      }
      if (null != daterangeEnqueueTime && '' != daterangeEnqueueTime) {
        queryParams.value.params["beginEnqueueTime"] = daterangeEnqueueTime.value[0];
        queryParams.value.params["endEnqueueTime"] = daterangeEnqueueTime.value[1];
      }
      if (null != daterangeUpdateTime && '' != daterangeUpdateTime) {
        queryParams.value.params["beginUpdateTime"] = daterangeUpdateTime.value[0];
        queryParams.value.params["endUpdateTime"] = daterangeUpdateTime.value[1];
      }
  listMonitor(queryParams.value).then(response => {
    monitorList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
        batchSize: null,        createSource: null,        createTime: null,        currentStatus: null,        delFlag: null,        discordUrl: null,        enqueueTime: null,        eventType: [],        fullCommand: null,        height: null,        id: null,        jobId: null,        jobType: [],        likedByUser: null,        likedByUserInRoom: null,        mjId: null,        parentGrid: null,        parentId: null,        published: null,        rating: null,        shown: null,        updateTime: null,        username: null,        userHidden: null,        userId: null,        width: null  };
  proxy.resetForm("monitorRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
      daterangeCreateTime.value = [];
      daterangeEnqueueTime.value = [];
      daterangeUpdateTime.value = [];
  proxy.resetForm("queryRef");
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加mj监控任务列表";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const mjMonitorJobId = row.id || ids.value
  getMonitor(mjMonitorJobId).then(response => {
    form.value = response.data;
        form.value.eventType = form.value.eventType.split(",");
        form.value.jobType = form.value.jobType.split(",");
    open.value = true;
    title.value = "修改mj监控任务列表";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["monitorRef"].validate(valid => {
    if (valid) {
          form.value.eventType = form.value.eventType.join(",");
          form.value.jobType = form.value.jobType.join(",");
      if (form.value.id != null) {
        updateMonitor(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addMonitor(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除mj监控任务列表编号为"' + _ids + '"的数据项？').then(function() {
    return delMonitor(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('mj/monitor/export', {
    ...queryParams.value
  }, `monitor_${new Date().getTime()}.xlsx`)
}

getList();
</script>