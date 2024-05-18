import axios from "axios";

export const handle = axios.create({
  baseURL: "http://api.localhost.com/",
});

export const get_user_list = async (page = 1) => {
  const { data } = await handle.get("/get_user_list", {
    params: {
      page,
    },
  });
  return data;
};

export const add_user = async (pack: { name: string; gender: string }) => {
  const { data } = await handle.post("/add_user", pack);
  return data;
};

export const edit_user = async (
  id: any,
  pack: { name: string; gender: string }
) => {
  const { data } = await handle.post(`/edit_user/${id}`, pack);
  return data;
};
