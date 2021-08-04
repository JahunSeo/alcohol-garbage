function submitSearch() {
  // 검색 조건 확인하기
  let search_text = $("#search-text").val().trim();
  let abv_array = [];
  for (let i = 1; i < 6; i++) {
    if ($(`#search-abv-${i}`).is(":checked")) {
      abv_array.push(i);
    }
  }
  let search_abv = abv_array.join(",");
  // params 구성하기
  let params = {};
  if (search_text) params["text"] = search_text;
  if (search_abv) params["abv_lv"] = search_abv;
  params = new URLSearchParams(params).toString();
  window.location.href = `?${params}`;
}
