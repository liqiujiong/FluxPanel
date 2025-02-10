<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">

      <el-form-item label="mj_id" prop="mjId">
        <el-input v-model="queryParams.mjId" placeholder="请输入mj_id" clearable @keyup.enter="handleQuery" />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input v-model="queryParams.email" placeholder="请输入邮箱" clearable @keyup.enter="handleQuery" />
      </el-form-item>

      <el-form-item label="监控状态" prop="monitorStatus">
        <el-select v-model="queryParams.monitorStatus" placeholder="请选择监控状态" style="width: 180px" clearable>
          <el-option v-for="dict in mj_monitor_status" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="订阅计划" prop="plan">
        <el-select v-model="queryParams.plan" placeholder="请选择订阅计划" style="width: 180px" clearable>
          <el-option v-for="dict in mj_account_plan" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="订阅状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择订阅状态" style="width: 180px" clearable>
          <el-option v-for="dict in mj_account_status" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="开通时间" style="width: 308px">
        <el-date-picker v-model="daterangeSubscribeTime" value-format="YYYY-MM-DD" type="daterange" range-separator="-"
          start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['mj:account:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
          v-hasPermi="['mj:account:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
          v-hasPermi="['mj:account:remove']">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="Download" @click="handleExport"
          v-hasPermi="['mj:account:export']">导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="accountList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />



      <el-table-column label="mj_id" align="center" prop="mjId" />

      <el-table-column label="邮箱" align="center" prop="email" />

      <el-table-column label="开通时间" align="center" prop="subscribeTime" />

      <el-table-column label="订阅计划" align="center" prop="plan">
        <template #default="scope">
          <dict-tag :options="mj_account_plan" :value="scope.row.plan" />
        </template>
      </el-table-column>


      <el-table-column label="总出图数" align="center" prop="totalJobs" />


      <el-table-column label="监控状态" align="center" prop="monitorStatus">
        <template #default="scope">
          <dict-tag :options="mj_monitor_status" :value="scope.row.monitorStatus" />
        </template>
      </el-table-column>


      <el-table-column label="订阅状态" align="center" prop="status">
        <template #default="scope">
          <dict-tag :options="mj_account_status" :value="scope.row.status" />
        </template>
      </el-table-column>

      <el-table-column label="备注" align="center" prop="remark" />

      <el-table-column label="异常信息" align="center" prop="errorMsg" />
      <el-table-column label="监控时间" align="center" prop="lastMonitorTime" />


      <el-table-column label="更新时间" align="center" prop="updateTime" />

      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
            v-hasPermi="['mj:account:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
            v-hasPermi="['mj:account:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize" @pagination="getList" />

    <!-- 添加或修改mj账号对话框 -->
    <el-dialog :title="title" v-model="open" width="800px" append-to-body>
      <el-form ref="accountRef" :model="form" :rules="rules" label-width="80px">

        <el-form-item label="mj_id" prop="mjId">
          <el-input v-model="form.mjId" placeholder="请输入mj_id" />
        </el-form-item>

        <el-form-item label="Cookie" prop="cookie">
          <el-input v-model="form.cookie" type="textarea" placeholder="请输入内容" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="开通时间" prop="subscribeTime">
          <el-date-picker clearable v-model="form.subscribeTime" type="date" value-format="YYYY-MM-DD"
            placeholder="请选择开通时间">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="Token" prop="token">
          <el-input v-model="form.token" placeholder="请输入Token" />
        </el-form-item>

        <el-form-item label="总出图数" prop="totalJobs">
          <el-input v-model="form.totalJobs" placeholder="请输入总出图数" />
        </el-form-item>

        <el-form-item label="user_id" prop="userId">
          <el-input v-model="form.userId" placeholder="请输入user_id" />
        </el-form-item>

        <el-form-item label="监控时间" prop="lastMonitorTime">
          <el-date-picker clearable v-model="form.lastMonitorTime" type="date" value-format="YYYY-MM-DD"
            placeholder="请选择监控时间">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="订阅计划" prop="plan">
          <el-select v-model="form.plan" placeholder="请选择订阅计划">
            <el-option v-for="dict in mj_account_plan" :key="dict.value" :label="dict.label"
              :value="dict.value"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
        </el-form-item>

        <el-form-item label="订阅状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择订阅状态">
            <el-option v-for="dict in mj_account_status" :key="dict.value" :label="dict.label"
              :value="dict.value"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="监控状态" prop="monitorStatus">
          <el-select v-model="form.monitorStatus" placeholder="请选择监控状态">
            <el-option v-for="dict in mj_monitor_status" :key="dict.value" :label="dict.label"
              :value="dict.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="异常信息" prop="errorMsg">
          <el-input v-model="form.errorMsg" placeholder="请输入异常信息" />
        </el-form-item>


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

<script setup name="Account">
import { listAccount, getAccount, delAccount, addAccount, updateAccount } from "@/api/mj/account";

const { proxy } = getCurrentInstance();
const { mj_monitor_status, mj_account_plan, mj_account_status } = proxy.useDict('mj_monitor_status', 'mj_account_plan', 'mj_account_status');

const accountList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeSubscribeTime = ref([]);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    email: null,
    mjId: null,
    monitorStatus: null,
    plan: null,
    status: null,
    subscribeTime: null,
  },
  rules: {
    cookie: [
      { required: true, message: "Cookie不能为空", trigger: "blur" }
    ], createTime: [
      { required: true, message: "创建时间不能为空", trigger: "blur" }
    ], delFlag: [
      { required: true, message: "删除标志(0代表存在 2代表删除)不能为空", trigger: "blur" }
    ], mjId: [
      { required: true, message: "mj_id不能为空", trigger: "blur" }
    ], updateTime: [
      { required: true, message: "更新时间不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询mj账号列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (null != daterangeSubscribeTime && '' != daterangeSubscribeTime) {
    queryParams.value.params["beginSubscribeTime"] = daterangeSubscribeTime.value[0];
    queryParams.value.params["endSubscribeTime"] = daterangeSubscribeTime.value[1];
  }
  listAccount(queryParams.value).then(response => {
    accountList.value = response.rows;
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
    cookie: null, createTime: null, delFlag: null, email: null, errorMsg: null, expireTime: null, id: null, lastMonitorTime: null, mjId: null, monitorStatus: null, plan: null, remark: null, status: null, subscribeTime: null, token: null, totalJobs: null, updateTime: null, userId: null
  };
  proxy.resetForm("accountRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  daterangeSubscribeTime.value = [];
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
  title.value = "添加mj账号";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const mjAccountId = row.id || ids.value
  getAccount(mjAccountId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改mj账号";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["accountRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateAccount(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAccount(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除mj账号编号为"' + _ids + '"的数据项？').then(function () {
    return delAccount(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => { });
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('mj/account/export', {
    ...queryParams.value
  }, `account_${new Date().getTime()}.xlsx`)
}

getList();
</script>