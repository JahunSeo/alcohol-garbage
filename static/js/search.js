function submitSearch() {
  console.log("submit search");
  // 검색 조건 확인하기
  let search_text = $("#search-text").val().trim();
  let abv_array = [];
  for (let i = 1; i < 6; i++) {
    if ($(`#search-abv-${i}`).is(":checked")) {
      abv_array.push(i);
    }
  }
  let search_abv = abv_array.join(",");
  console.log(search_text, search_abv);
  // params 구성하기
  let params = {};
  if (search_text) params["text"] = search_text;
  if (search_abv) params["abv_lv"] = search_abv;
  console.log(params);
  params = new URLSearchParams(params).toString();
  console.log(params);
  window.location.href = `?${params}`;

  //   // params 만들기
  //   let params_array = [];
  //   if (search_text) params_array.push(`text=${search_text}`);
  //   if (search_abv) params_array.push(`text=${search_abv}`);
  //   if (params_array.length > 0) {
  //     params = "?" + params_array.join("&");
  //   }
}
