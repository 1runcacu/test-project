<template>
  <el-button plain @click="addShow" class="my-5"> Add User </el-button>
  <div class="w-[80vw]">
    <el-table :data="tableData" class="w-full" key="id">
      <el-table-column prop="id" label="id" width="180" />
      <el-table-column prop="name" label="name" />
      <el-table-column prop="gender" label="gender" />
      <el-table-column fixed="right" label="Operations" width="120">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="editShow(row)"
            >Edit</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-pagination
    background
    layout="prev, pager, next"
    :total="total"
    class="mt-6"
  />
  <el-dialog v-model="dialogFormVisible" :title="title" width="500">
    <el-form :model="form">
      <el-form-item label="name" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="gender" :label-width="formLabelWidth">
        <el-select v-model="form.gender" placeholder="Please select a zone">
          <el-option label="male" value="male" />
          <el-option label="female" value="female" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handle">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";
import { add_user, edit_user, get_user_list } from "../api";

enum ModeType {
  add = 0,
  edit = 1,
}

interface SubType {
  id?: string;
  name: string;
  gender: string;
}

const dialogFormVisible = ref(false);
const formLabelWidth = "140px";

const form = reactive({
  id: "",
  name: "",
  gender: "",
});

const tableData = ref([]);
const total = ref(0);
const title = ref("Add User");
const mode = ref(ModeType.add);

async function get_list(page = 1) {
  const data = await get_user_list(page);
  tableData.value = data?.list ?? [];
  total.value = data?.total ?? 0;
}

const addShow = () => {
  mode.value = ModeType.add;
  form.name = "";
  form.gender = "";
  title.value = "Add User";
  dialogFormVisible.value = true;
};

const editShow = (row: SubType) => {
  mode.value = ModeType.edit;
  form.id = row.id!;
  form.name = row.name;
  form.gender = row.gender;
  title.value = "Edit User";
  dialogFormVisible.value = true;
};

const handle = async () => {
  if (mode.value === ModeType.add) {
    await add_user({
      name: form.name,
      gender: form.gender,
    });
  } else {
    await edit_user(form.id, {
      name: form.name,
      gender: form.gender,
    });
  }
  dialogFormVisible.value = false;
  get_list();
};

onMounted(() => {
  get_list();
});
</script>
